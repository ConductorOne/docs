# API Usage Gotchas

API client and external system integration issues.

## Use uhttp instead of http.Client

The SDK provides `uhttp` with automatic retries and rate limiting.

**Wrong:**
```go
httpClient := &http.Client{Timeout: 30 * time.Second}
resp, err := httpClient.Do(req)
```

**Correct:**
```go
import "github.com/conductorone/baton-sdk/pkg/uhttp"

httpClient, err := uhttp.NewClient(ctx,
    uhttp.WithLogger(true, ctxzap.Extract(ctx)),
    uhttp.WithUserAgent("baton-myservice/1.0.0"),
)
```

uhttp provides:
- Automatic retries on 429, 503
- Rate limit header parsing
- Exponential backoff
- Request/response logging

## ExternalId required for provisioning

Resources must have ExternalId set for Grant/Revoke to work.

**Wrong:**
```go
resource, err := rs.NewResource(name, resourceType, id)
// No ExternalId - provisioning can't find the resource
```

**Correct:**
```go
resource, err := rs.NewResource(name, resourceType, id,
    rs.WithExternalID(&v2.ExternalId{Id: nativeID}),
)
```

Use the native system's identifier - the ID the target API expects.

## Error messages should include connector name

Prefix errors for easier log debugging.

**Okay:**
```go
return nil, fmt.Errorf("failed to list users: %w", err)
```

**Better:**
```go
return nil, fmt.Errorf("baton-myservice: failed to list users: %w", err)
```

## go mod tidy required

Writing go.mod manually doesn't create go.sum.

**Error:**
```
missing go.sum entry for module providing package ...
```

**Fix:**
```bash
go mod tidy
```

## Insecure TLS for testing only

For local mocks with self-signed certs:

```go
uhttp.NewClient(ctx,
    uhttp.WithLogger(true, l),
    uhttp.WithTLSClientConfig(&tls.Config{
        InsecureSkipVerify: true,  // ONLY for testing
    }),
)
```

Never use in production.

## Resource IDs must support grants queries

Design IDs to contain data needed for grants lookups.

**Problem:**
```yaml
# ID is just name
id: "my-repo"

# But grants query needs owner AND name
query: query($owner: String!, $name: String!) { ... }
```

**Solution - composite ID:**
```yaml
id: "{{ .owner.login }}/{{ .name }}"  # "myorg/my-repo"

# Parse when needed
owner: "{{ index (split \"/\" .resource_id) 0 }}"
name: "{{ index (split \"/\" .resource_id) 1 }}"
```
