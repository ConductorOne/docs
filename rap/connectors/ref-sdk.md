# ref-sdk

SDK interface reference for baton-sdk. Interfaces your connector implements.

---

## Core interfaces

### ConnectorBuilder (entry point)

```go
type ConnectorBuilder interface {
    MetadataProvider
    ValidateProvider
    ResourceSyncers(ctx context.Context) []ResourceSyncer
}

type ConnectorBuilderV2 interface {  // Preferred
    MetadataProvider
    ValidateProvider
    ResourceSyncers(ctx context.Context) []ResourceSyncerV2
}

type MetadataProvider interface {
    Metadata(ctx context.Context) (*v2.ConnectorMetadata, error)
}

type ValidateProvider interface {
    Validate(ctx context.Context) (annotations.Annotations, error)
}
```

---

### ResourceSyncer (sync data)

```go
// V1 (legacy)
type ResourceSyncer interface {
    ResourceType(ctx context.Context) *v2.ResourceType
    List(ctx context.Context, parentResourceID *v2.ResourceId,
         pToken *pagination.Token) ([]*v2.Resource, string, annotations.Annotations, error)
    Entitlements(ctx context.Context, resource *v2.Resource,
                 pToken *pagination.Token) ([]*v2.Entitlement, string, annotations.Annotations, error)
    Grants(ctx context.Context, resource *v2.Resource,
           pToken *pagination.Token) ([]*v2.Grant, string, annotations.Annotations, error)
}

// V2 (preferred)
type ResourceSyncerV2 interface {
    ResourceType(ctx context.Context) *v2.ResourceType
    List(ctx context.Context, parentResourceID *v2.ResourceId,
         opts resource.SyncOpAttrs) ([]*v2.Resource, *resource.SyncOpResults, error)
    Entitlements(ctx context.Context, resource *v2.Resource,
                 opts resource.SyncOpAttrs) ([]*v2.Entitlement, *resource.SyncOpResults, error)
    Grants(ctx context.Context, resource *v2.Resource,
           opts resource.SyncOpAttrs) ([]*v2.Grant, *resource.SyncOpResults, error)
}
```

V2 differences: receives `SyncOpAttrs` with session store, returns structured `SyncOpResults`.

---

### ResourceProvisioner (grant/revoke)

```go
// V2 (preferred)
type ResourceProvisionerV2 interface {
    ResourceSyncer
    Grant(ctx context.Context, resource *v2.Resource,
          entitlement *v2.Entitlement) ([]*v2.Grant, annotations.Annotations, error)
    Revoke(ctx context.Context, grant *v2.Grant) (annotations.Annotations, error)
}
```

Enables `CAPABILITY_PROVISION`.

---

### AccountManager (user provisioning)

```go
type AccountManager interface {
    ResourceSyncer
    CreateAccount(ctx context.Context,
        accountInfo *v2.AccountInfo,
        credentialOptions *v2.LocalCredentialOptions,
    ) (CreateAccountResponse, []*v2.PlaintextData, annotations.Annotations, error)
    CreateAccountCapabilityDetails(ctx context.Context,
    ) (*v2.CredentialDetailsAccountProvisioning, annotations.Annotations, error)
}
```

Enables `CAPABILITY_ACCOUNT_PROVISIONING`.

---

### ResourceManager (create/delete)

```go
type ResourceManagerV2 interface {
    ResourceSyncer
    Create(ctx context.Context, resource *v2.Resource) (*v2.Resource, annotations.Annotations, error)
    Delete(ctx context.Context, resourceId *v2.ResourceId,
           parentResourceID *v2.ResourceId) (annotations.Annotations, error)
}
```

Enables `CAPABILITY_RESOURCE_CREATE`, `CAPABILITY_RESOURCE_DELETE`.

---

## Pagination

### Token (simple cursor)

```go
type Token struct {
    Token string  // Opaque cursor, empty for first page
    Size  int     // Requested page size
}
```

Usage in List():
```go
resp, _ := client.ListUsers(ctx, pToken.Token, 100)
return resources, resp.NextCursor, nil, nil  // Return next cursor
```

### Bag (nested pagination)

```go
bag := &pagination.Bag{}
bag.Push(pagination.PageState{Token: "cursor", ResourceID: "parent-123"})
state := bag.Pop()

// Encode for return
nextToken, _ := bag.Marshal()
```

Use when paginating within nested resources.

---

## Resource helpers

```go
// Create user resource
resource.NewUserResource(name, resourceType, id,
    resource.WithEmail(email, isPrimary),
    resource.WithUserLogin(login),
    resource.WithStatus(v2.UserTrait_Status_STATUS_ENABLED),
)

// Create group resource
resource.NewGroupResource(name, resourceType, id,
    resource.WithGroupProfile(description),
)

// Create generic resource
resource.NewResource(name, resourceType, id,
    resource.WithParentResourceID(parentID),
    resource.WithAnnotation(&v2.ChildResourceType{ResourceTypeId: "child-type"}),
)
```

---

## Entitlement helpers

```go
// Permission on a resource
entitlement.NewPermissionEntitlement(resource, "admin",
    entitlement.WithDisplayName("Administrator"),
    entitlement.WithGrantableTo(userResourceType),
)

// Membership in a group
entitlement.NewAssignmentEntitlement(groupResource, "member",
    entitlement.WithDisplayName("Member"),
)
```

---

## Grant helpers

```go
grant.NewGrant(
    resource,       // Resource the entitlement belongs to
    "permission",   // Entitlement slug
    principalID,    // Who has the grant (*v2.ResourceId)
)
```

---

## Capabilities

| Capability | Interface Required |
|------------|-------------------|
| `CAPABILITY_PROVISION` | ResourceProvisioner |
| `CAPABILITY_ACCOUNT_PROVISIONING` | AccountManager |
| `CAPABILITY_RESOURCE_CREATE` | ResourceManager |
| `CAPABILITY_RESOURCE_DELETE` | ResourceManager |
| `CAPABILITY_TARGETED_SYNC` | ResourceTargetedSyncer |
| `CAPABILITY_CREDENTIAL_ROTATION` | CredentialManager |
| `CAPABILITY_ACTIONS` | CustomActionManager |

Capabilities declared in connector metadata, enabled by implementing interfaces.
