# provision-grant

GrantProvisionerV2 and RevokeProvisioner interfaces for Grant and Revoke operations.

---

## The Interfaces

```go
// V2 interface (recommended for new connectors)
type GrantProvisionerV2 interface {
    Grant(ctx context.Context, principal *v2.Resource, entitlement *v2.Entitlement) ([]*v2.Grant, annotations.Annotations, error)
}

type RevokeProvisioner interface {
    Revoke(ctx context.Context, grant *v2.Grant) (annotations.Annotations, error)
}
```

## Implementation Pattern

Add provisioning to your resource builder:

```go
type groupBuilder struct {
    client *MyServiceClient
}

// Implement ResourceSyncer methods...

func (b *groupBuilder) Grant(
    ctx context.Context,
    principal *v2.Resource,
    entitlement *v2.Entitlement,
) ([]*v2.Grant, annotations.Annotations, error) {
    groupID := entitlement.Resource.Id.Resource
    userID := principal.Id.Resource

    err := b.client.AddGroupMember(ctx, groupID, userID)
    if err != nil {
        if isAlreadyExistsError(err) {
            return nil, nil, nil  // Idempotent success
        }
        return nil, nil, fmt.Errorf("failed to add member: %w", err)
    }

    // Return created grant
    grant := sdkGrant.NewGrant(entitlement.Resource, entitlement.Slug, principal.Id)
    return []*v2.Grant{grant}, nil, nil
}

func (b *groupBuilder) Revoke(
    ctx context.Context,
    grant *v2.Grant,
) (annotations.Annotations, error) {
    groupID := grant.Entitlement.Resource.Id.Resource
    userID := grant.Principal.Id.Resource

    err := b.client.RemoveGroupMember(ctx, groupID, userID)
    if err != nil {
        if isNotFoundError(err) {
            return nil, nil  // Already revoked
        }
        return nil, fmt.Errorf("failed to remove member: %w", err)
    }

    return nil, nil
}
```

## Registering Provisioning

In your connector's constructor:

```go
func (c *Connector) ResourceSyncers(ctx context.Context) []connectorbuilder.ResourceSyncer {
    return []connectorbuilder.ResourceSyncer{
        newUserBuilder(c.client),
        newGroupBuilder(c.client), // Implements ResourceProvisionerV2
    }
}
```

The SDK detects if your builder implements `ResourceProvisionerV2` and enables provisioning automatically.

## Multiple Entitlements

Handle different entitlement types in a single resource:

```go
func (b *groupBuilder) Grant(
    ctx context.Context,
    principal *v2.Resource,
    entitlement *v2.Entitlement,
) ([]*v2.Grant, annotations.Annotations, error) {
    groupID := entitlement.Resource.Id.Resource
    userID := principal.Id.Resource

    switch entitlement.Slug {
    case "member":
        err := b.client.AddMember(ctx, groupID, userID)
        // ...
    case "admin":
        err := b.client.AddAdmin(ctx, groupID, userID)
        // ...
    default:
        return nil, nil, fmt.Errorf("unknown entitlement: %s", entitlement.Slug)
    }

    grant := sdkGrant.NewGrant(entitlement.Resource, entitlement.Slug, principal.Id)
    return []*v2.Grant{grant}, nil, nil
}
```

## Idempotency

Provisioning operations should be idempotent:

```go
// Good: handles already-exists gracefully
err := b.client.AddGroupMember(ctx, groupID, userID)
if err != nil && !isAlreadyMemberError(err) {
    return nil, err
}
return nil, nil

// Good: handles not-found gracefully
err := b.client.RemoveGroupMember(ctx, groupID, userID)
if err != nil && !isNotFoundError(err) {
    return nil, err
}
return nil, nil
```

## Running with Provisioning

The connector must be started with `--provisioning` flag:

```bash
./baton-myservice \
  --api-token "$TOKEN" \
  --client-id "$C1_CLIENT_ID" \
  --client-secret "$C1_CLIENT_SECRET" \
  --provisioning
```
