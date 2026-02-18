# build-syncer

Implementing ResourceType(), List(), Entitlements(), Grants() methods.

---

## The ResourceSyncer Interface

```go
type ResourceSyncer interface {
    ResourceType(ctx context.Context) *v2.ResourceType
    List(ctx context.Context, parentResourceID *v2.ResourceId, token *pagination.Token) (
        []*v2.Resource, string, annotations.Annotations, error)
    Entitlements(ctx context.Context, resource *v2.Resource, token *pagination.Token) (
        []*v2.Entitlement, string, annotations.Annotations, error)
    Grants(ctx context.Context, resource *v2.Resource, token *pagination.Token) (
        []*v2.Grant, string, annotations.Annotations, error)
}
```

## Complete User Builder Example

```go
package connector

import (
    "context"

    v2 "github.com/conductorone/baton-sdk/pb/c1/connector/v2"
    "github.com/conductorone/baton-sdk/pkg/annotations"
    "github.com/conductorone/baton-sdk/pkg/pagination"
    rs "github.com/conductorone/baton-sdk/pkg/types/resource"
)

var userResourceType = &v2.ResourceType{
    Id:          "user",
    DisplayName: "User",
    Traits:      []v2.ResourceType_Trait{v2.ResourceType_TRAIT_USER},
}

type userBuilder struct {
    client *MyServiceClient
}

func newUserBuilder(client *MyServiceClient) *userBuilder {
    return &userBuilder{client: client}
}

func (b *userBuilder) ResourceType(ctx context.Context) *v2.ResourceType {
    return userResourceType
}

func (b *userBuilder) List(
    ctx context.Context,
    parentResourceID *v2.ResourceId,
    token *pagination.Token,
) ([]*v2.Resource, string, annotations.Annotations, error) {
    // Parse page token
    pageToken := ""
    if token != nil && token.Token != "" {
        pageToken = token.Token
    }

    // Fetch from API
    users, nextToken, err := b.client.ListUsers(ctx, pageToken, 100)
    if err != nil {
        return nil, "", nil, err
    }

    // Convert to resources
    var resources []*v2.Resource
    for _, user := range users {
        resource, err := rs.NewUserResource(
            user.Name,
            userResourceType,
            user.ID,
            []rs.UserTraitOption{
                rs.WithEmail(user.Email, true),
                rs.WithStatus(v2.UserTrait_Status_STATUS_ENABLED),
                rs.WithUserLogin(user.Username),
            },
        )
        if err != nil {
            return nil, "", nil, err
        }
        resources = append(resources, resource)
    }

    return resources, nextToken, nil, nil
}

func (b *userBuilder) Entitlements(
    ctx context.Context,
    resource *v2.Resource,
    token *pagination.Token,
) ([]*v2.Entitlement, string, annotations.Annotations, error) {
    // Users typically don't offer entitlements
    return nil, "", nil, nil
}

func (b *userBuilder) Grants(
    ctx context.Context,
    resource *v2.Resource,
    token *pagination.Token,
) ([]*v2.Grant, string, annotations.Annotations, error) {
    // Users typically don't have grants on them
    return nil, "", nil, nil
}
```

## Group Builder (With Entitlements and Grants)

```go
var groupResourceType = &v2.ResourceType{
    Id:          "group",
    DisplayName: "Group",
    Traits:      []v2.ResourceType_Trait{v2.ResourceType_TRAIT_GROUP},
}

type groupBuilder struct {
    client *MyServiceClient
}

func (b *groupBuilder) ResourceType(ctx context.Context) *v2.ResourceType {
    return groupResourceType
}

func (b *groupBuilder) List(
    ctx context.Context,
    parentResourceID *v2.ResourceId,
    token *pagination.Token,
) ([]*v2.Resource, string, annotations.Annotations, error) {
    groups, nextToken, err := b.client.ListGroups(ctx, token.Token, 100)
    if err != nil {
        return nil, "", nil, err
    }

    var resources []*v2.Resource
    for _, group := range groups {
        resource, err := rs.NewGroupResource(
            group.Name,
            groupResourceType,
            group.ID,
            []rs.GroupTraitOption{},
        )
        if err != nil {
            return nil, "", nil, err
        }
        resources = append(resources, resource)
    }

    return resources, nextToken, nil, nil
}

func (b *groupBuilder) Entitlements(
    ctx context.Context,
    resource *v2.Resource,
    token *pagination.Token,
) ([]*v2.Entitlement, string, annotations.Annotations, error) {
    // Groups offer membership
    entitlement := &v2.Entitlement{
        Id:          "member",
        DisplayName: "Member",
        Description: "Member of " + resource.DisplayName,
        Resource:    resource,
        GrantableTo: []*v2.ResourceType{userResourceType},
        Purpose:     v2.Entitlement_PURPOSE_VALUE_ASSIGNMENT,
        Slug:        "member",
    }

    return []*v2.Entitlement{entitlement}, "", nil, nil
}

func (b *groupBuilder) Grants(
    ctx context.Context,
    resource *v2.Resource,
    token *pagination.Token,
) ([]*v2.Grant, string, annotations.Annotations, error) {
    groupID := resource.Id.Resource

    members, nextToken, err := b.client.GetGroupMembers(ctx, groupID, token.Token)
    if err != nil {
        return nil, "", nil, err
    }

    var grants []*v2.Grant
    for _, member := range members {
        grant := &v2.Grant{
            Entitlement: &v2.Entitlement{
                Id:       "member",
                Resource: resource,
            },
            Principal: &v2.Resource{
                Id: &v2.ResourceId{
                    ResourceType: "user",
                    Resource:     member.UserID,
                },
            },
        }
        grants = append(grants, grant)
    }

    return grants, nextToken, nil, nil
}
```

## Key Points

- **ResourceType()**: Called once per sync to learn resource type metadata
- **List()**: May be called multiple times for pagination
- **Entitlements()**: Called once per resource instance
- **Grants()**: Called once per resource instance, may paginate

Return empty string for nextToken when done paginating.
