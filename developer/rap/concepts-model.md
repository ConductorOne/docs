# Access Model Concepts

ConductorOne's model for representing access: resources, entitlements, grants.

## Resources

Things that exist in the target system. Users, groups, projects, repositories.

```go
resource, err := rs.NewUserResource(
    "alice@example.com",    // Display name
    userResourceType,       // Resource type
    "user-123",             // Unique ID
    []rs.UserTraitOption{
        rs.WithEmail("alice@example.com", true),
    },
)
```

## Resource Types

Define what kinds of resources your connector syncs.

```go
var userResourceType = &v2.ResourceType{
    Id:          "user",
    DisplayName: "User",
    Traits:      []v2.ResourceType_Trait{v2.ResourceType_TRAIT_USER},
}

var groupResourceType = &v2.ResourceType{
    Id:          "group",
    DisplayName: "Group",
    Traits:      []v2.ResourceType_Trait{v2.ResourceType_TRAIT_GROUP},
}
```

## Traits

Markers that tell ConductorOne what a resource represents.

| Trait | Meaning | Builder |
|-------|---------|---------|
| `TRAIT_USER` | A principal that receives access | `rs.NewUserResource` |
| `TRAIT_GROUP` | Contains members | `rs.NewGroupResource` |
| `TRAIT_ROLE` | Can be assigned to users | `rs.NewRoleResource` |
| `TRAIT_APP` | An application | `rs.NewAppResource` |

Resources with traits must use the specific builder function.

## Entitlements

What access exists on a resource. "Admin on this group" or "Member of this team".

```go
ent := entitlement.NewAssignmentEntitlement(
    groupResource,
    "member",
    entitlement.WithGrantableTo(userResourceType),
    entitlement.WithDisplayName("Member"),
)
```

Key properties:
- `grantableTo`: Which resource types can receive this entitlement
- Usually `member` for groups, `assigned` for roles

## Grants

Who currently has what access. Connects a principal to an entitlement.

```go
grant := gt.NewGrant(
    groupResource,           // Resource with the entitlement
    "member",                // Entitlement slug
    userResource.Id,         // Principal who has access
)
```

## Flow

1. Sync resources (users, groups, roles)
2. For each resource, list its entitlements
3. For each entitlement, list grants (who has it)

## Common Patterns

**Groups with members:**
- Group has `TRAIT_GROUP`
- Group has `member` entitlement with `grantableTo: [user]`
- Grants connect users to group membership

**Roles assigned to users:**
- Role has `TRAIT_ROLE`
- Role has `assigned` entitlement with `grantableTo: [user]`
- Grants connect users to role assignment

**Per-resource permissions:**
- Resource (e.g., repository) has entitlements like `read`, `write`, `admin`
- Each entitlement has `grantableTo: [user]`
- Grants connect users to specific permissions
