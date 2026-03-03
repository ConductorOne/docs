# recipes-modeling

Resource modeling patterns for connectors.

---

## Parent-child hierarchies

Model resources within other resources (repos in orgs, projects in accounts):

```go
// Parent type declares children
var orgResourceType = &v2.ResourceType{
    Id:          "organization",
    DisplayName: "Organization",
    Traits:      []v2.ResourceType_Trait{v2.ResourceType_TRAIT_GROUP},
}

var projectResourceType = &v2.ResourceType{
    Id:          "project",
    DisplayName: "Project",
    Traits:      []v2.ResourceType_Trait{v2.ResourceType_TRAIT_GROUP},
}

// Org List() declares child relationship
func (o *orgBuilder) List(ctx context.Context, _ *v2.ResourceId,
    pToken *pagination.Token) ([]*v2.Resource, string, annotations.Annotations, error) {

    orgs, _ := o.client.ListOrgs(ctx)
    var resources []*v2.Resource
    for _, org := range orgs {
        r, _ := resource.NewResource(org.Name, orgResourceType, org.ID,
            resource.WithAnnotation(&v2.ChildResourceType{
                ResourceTypeId: projectResourceType.Id,
            }),
        )
        resources = append(resources, r)
    }
    return resources, "", nil, nil
}

// Project List() receives parent ID
func (p *projectBuilder) List(ctx context.Context, parentID *v2.ResourceId,
    pToken *pagination.Token) ([]*v2.Resource, string, annotations.Annotations, error) {

    if parentID == nil {
        return nil, "", nil, nil  // Projects only exist within orgs
    }
    projects, _ := p.client.ListProjects(ctx, parentID.Resource)
    var resources []*v2.Resource
    for _, proj := range projects {
        r, _ := resource.NewResource(proj.Name, projectResourceType, proj.ID,
            resource.WithParentResourceID(parentID),
        )
        resources = append(resources, r)
    }
    return resources, "", nil, nil
}
```

SDK calls child `List()` once per parent, passing `parentID`.

---

## Deep hierarchies (3+ levels)

AWS example: Account -> Region -> Resource

```go
// Each level declares its children
accountType  // WithAnnotation(&v2.ChildResourceType{ResourceTypeId: "region"})
regionType   // WithAnnotation(&v2.ChildResourceType{ResourceTypeId: "ec2_instance"})
instanceType // Leaf node, no children
```

SDK traverses depth-first. Each level receives parent context.

---

## User traits

```go
r, _ := resource.NewUserResource(
    user.DisplayName,
    userResourceType,
    user.ID,
    resource.WithEmail(user.Email, true),  // true = primary
    resource.WithUserLogin(user.Username),
    resource.WithStatus(v2.UserTrait_Status_STATUS_ENABLED),
    resource.WithAccountType(v2.UserTrait_ACCOUNT_TYPE_HUMAN),
)
```

Common traits:
- `WithEmail(email, isPrimary)` - User's email
- `WithUserLogin(login)` - Username/login ID
- `WithStatus(status)` - ENABLED, DISABLED, DELETED
- `WithAccountType(type)` - HUMAN, SERVICE, SYSTEM

---

## Group traits

```go
r, _ := resource.NewGroupResource(
    group.Name,
    groupResourceType,
    group.ID,
    resource.WithGroupProfile(group.Description),
)
```

---

## Role traits

```go
r, _ := resource.NewRoleResource(
    role.Name,
    roleResourceType,
    role.ID,
    resource.WithRoleProfile(role.Description),
)
```

---

## Custom resource types

For resources that aren't users, groups, or roles:

```go
var repositoryResourceType = &v2.ResourceType{
    Id:          "repository",
    DisplayName: "Repository",
    Traits:      []v2.ResourceType_Trait{},  // No standard trait
}

r, _ := resource.NewResource(
    repo.Name,
    repositoryResourceType,
    repo.ID,
    // Add custom annotations as needed
)
```

---

## Entitlement patterns

**Permission entitlements** (on a single resource):
```go
entitlement.NewPermissionEntitlement(
    resource,           // The resource this permission applies to
    "admin",            // Permission slug
    entitlement.WithDisplayName("Administrator"),
    entitlement.WithDescription("Full administrative access"),
    entitlement.WithGrantableTo(userResourceType),
)
```

**Membership entitlements** (belonging to a group):
```go
entitlement.NewAssignmentEntitlement(
    groupResource,
    "member",
    entitlement.WithDisplayName("Member"),
    entitlement.WithGrantableTo(userResourceType),
)
```

---

## Grant patterns

```go
grant.NewGrant(
    resource,      // Resource the entitlement belongs to
    "admin",       // Entitlement slug
    principalID,   // Who has the grant (usually user resource ID)
)
```

Principal is typically a `*v2.ResourceId` from a user resource.
