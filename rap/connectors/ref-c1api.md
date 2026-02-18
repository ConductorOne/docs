# ref-c1api

How connectors communicate with ConductorOne platform. SDK handles this; understanding helps debugging.

---

## Architecture

```
ConductorOne Platform                     Connector (Daemon Mode)
+---------------------+                   +------------------------+
|  Task Queue         |<--- gRPC ---------| BatonServiceClient     |
|  (Sync, Grant, etc) |--- Task --------->| Task Handler           |
|  Upload Service     |<--- c1z upload ---| ConnectorBuilderV2     |
|  Heartbeat          |<--- keepalive ----| HeartbeatLoop          |
+---------------------+                   +------------------------+
```

- Connectors poll for tasks (pull model)
- Results upload via streaming gRPC (512KB chunks)
- Heartbeats keep tasks alive during long operations

---

## BatonServiceClient interface

```go
type BatonServiceClient interface {
    Hello(ctx, req) (*HelloResponse, error)      // Initial handshake
    GetTask(ctx, req) (*GetTaskResponse, error)  // Poll for work
    Heartbeat(ctx, req) (*HeartbeatResponse, error)  // Keep task alive
    FinishTask(ctx, req) (*FinishTaskResponse, error)  // Report completion
    Upload(ctx, task, reader) error              // Upload c1z file
}
```

---

## Task types

### SyncTask

```go
type SyncTask struct {
    SyncId           string    // Unique identifier
    ResourceTypes    []string  // Types to sync (empty = all)
    ResourceIds      []string  // Specific resources (targeted)
    SkipEntitlements bool
    SkipGrants       bool
}
```

Produces: c1z file uploaded to C1

### GrantTask

```go
type GrantTask struct {
    Entitlement *v2.Entitlement  // What to grant
    Principal   *v2.Resource     // Who receives it
}
```

Calls: Your `Grant()` implementation

### RevokeTask

```go
type RevokeTask struct {
    Grant *v2.Grant  // Grant to revoke
}
```

Calls: Your `Revoke()` implementation

### CreateAccountTask

```go
type CreateAccountTask struct {
    AccountInfo       *v2.AccountInfo
    CredentialOptions *v2.LocalCredentialOptions
}
```

Calls: Your `CreateAccount()` implementation

### DeleteResourceTask

```go
type DeleteResourceTask struct {
    ResourceId       *v2.ResourceId
    ParentResourceId *v2.ResourceId
}
```

Calls: Your `Delete()` implementation

### RotateCredentialTask

```go
type RotateCredentialTask struct {
    ResourceId        *v2.ResourceId
    CredentialOptions *v2.LocalCredentialOptions
}
```

Calls: Your `Rotate()` implementation

---

## Task lifecycle

```
Connector                                C1 Platform
    |--- Hello (identify) -------------->|
    |<-- HelloResponse (config) ---------|
    |                                    |
    |--- GetTask (poll) ---------------->|
    |<-- Task or NoTask -----------------|
    |                                    |
    [If task]                            |
    |--- Heartbeat (every 30s) --------->|
    |                                    |
    [Process task]                       |
    |                                    |
    |--- FinishTask (result) ----------->|
```

---

## Heartbeat

Tasks have 60-second default timeout. Connector sends heartbeats every 30 seconds during processing.

```go
// SDK handles automatically
go func() {
    ticker := time.NewTicker(30 * time.Second)
    for range ticker.C {
        client.Heartbeat(ctx, &HeartbeatRequest{TaskId: task.Id})
    }
}()
```

Missing heartbeats = task considered failed, may be reassigned.

---

## c1z upload

Sync results upload via streaming:

```go
// SDK handles chunking (512KB)
err := client.Upload(ctx, task, c1zFileReader)
```

Large syncs may take several minutes to upload. Heartbeats continue during upload.

---

## Authentication

Daemon mode uses OAuth2 client credentials:

```bash
./baton-example --client-id $CLIENT_ID --client-secret $CLIENT_SECRET
```

SDK exchanges credentials for access token, refreshes automatically.

---

## Error handling

| Error | SDK Behavior |
|-------|--------------|
| Network timeout | Retry with backoff |
| 401 Unauthorized | Refresh token, retry |
| 429 Rate limited | Backoff, retry |
| Task timeout | Task marked failed |
| Upload failure | Retry upload |

Connector code should return errors; SDK handles retry logic.
