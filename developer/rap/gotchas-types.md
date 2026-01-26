# Type System Gotchas

Type-related issues in connector development.

## Import paths under pkg/types

Resource helpers are under `pkg/types/`, not `pkg/`.

**Error:**
```
module github.com/conductorone/baton-sdk@latest found (v0.7.1),
but does not contain package github.com/conductorone/baton-sdk/pkg/entitlement
```

**Wrong:**
```go
import "github.com/conductorone/baton-sdk/pkg/entitlement"
```

**Correct:**
```go
import "github.com/conductorone/baton-sdk/pkg/types/entitlement"
```

All three helpers follow this pattern:
```go
import (
    "github.com/conductorone/baton-sdk/pkg/types/entitlement"
    "github.com/conductorone/baton-sdk/pkg/types/grant"
    "github.com/conductorone/baton-sdk/pkg/types/resource"
)
```

## Trait requires specific builder

Resources with traits must use the matching builder function.

**Error:**
```
resource was missing expected trait AppTrait
```

**Wrong:**
```go
// Using generic NewResource for a USER trait
return rs.NewResource(name, userResourceType, id)
```

**Correct:**
```go
switch trait {
case v2.ResourceType_TRAIT_USER:
    return rs.NewUserResource(name, resourceType, id, userOpts)
case v2.ResourceType_TRAIT_GROUP:
    return rs.NewGroupResource(name, resourceType, id, groupOpts)
case v2.ResourceType_TRAIT_ROLE:
    return rs.NewRoleResource(name, resourceType, id, roleOpts)
case v2.ResourceType_TRAIT_APP:
    return rs.NewAppResource(name, resourceType, id, appOpts)
default:
    return rs.NewResource(name, resourceType, id)
}
```

## WithGrantableTo expects pointer

`WithGrantableTo` takes `*v2.ResourceType`, not string.

**Wrong:**
```go
entitlement.WithGrantableTo("user")
```

**Correct:**
```go
var userResourceType = &v2.ResourceType{
    Id:          "user",
    DisplayName: "User",
    Traits:      []v2.ResourceType_Trait{v2.ResourceType_TRAIT_USER},
}

entitlement.WithGrantableTo(userResourceType)
```

## NewConnector wrapper required

Your connector must be wrapped with `connectorbuilder.NewConnector`.

**Wrong:**
```go
func getConnector(ctx context.Context, cfg *Config) (types.ConnectorServer, error) {
    return connector.New(ctx, cfg)  // Returns unwrapped
}
```

**Correct:**
```go
func getConnector(ctx context.Context, cfg *Config) (types.ConnectorServer, error) {
    cb, err := connector.New(ctx, cfg)
    if err != nil {
        return nil, err
    }
    return connectorbuilder.NewConnector(ctx, cb)
}
```

## SDK any fields need type assertions

Some SDK types use `any` for flexible JSON. Use type assertions.

**Wrong:**
```go
props := tool.InputSchema.Properties  // any has no field Properties
```

**Correct:**
```go
schemaMap, ok := inputSchema.(map[string]any)
if !ok {
    return nil
}
props, ok := schemaMap["properties"].(map[string]any)
```
