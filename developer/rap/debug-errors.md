# Error Reference

Common error messages and how to fix them.

## VerifyStructFields failed

```
VerifyStructFields failed: field my-field in confschema does not have
a corresponding struct tag in the configuration struct
```

**Cause:** Config struct missing `mapstructure` tag.

**Fix:** Add tag matching the field name:
```go
type Config struct {
    MyField string `mapstructure:"my-field"`
}
```

## does not contain package

```
module github.com/conductorone/baton-sdk@latest found (v0.7.1),
but does not contain package github.com/conductorone/baton-sdk/pkg/entitlement
```

**Cause:** Wrong import path.

**Fix:** Add `/types/` to path:
```go
import "github.com/conductorone/baton-sdk/pkg/types/entitlement"
```

## cannot use cfg as field.Configurable

```
cannot use cfg (variable of type *Config) as field.Configurable value
```

**Cause:** Config struct doesn't implement Configurable interface.

**Fix:** Add getter methods:
```go
func (c *Config) GetString(key string) string { ... }
func (c *Config) GetBool(key string) bool { return false }
func (c *Config) GetInt(key string) int { return 0 }
func (c *Config) GetStringSlice(key string) []string { return nil }
func (c *Config) GetStringMap(key string) map[string]any { return nil }
```

## missing expected trait

```
resource was missing expected trait AppTrait
```

**Cause:** Used generic `NewResource` for traited resource type.

**Fix:** Use specific builder:
```go
// For TRAIT_USER
rs.NewUserResource(name, rt, id, userOpts)

// For TRAIT_GROUP
rs.NewGroupResource(name, rt, id, groupOpts)

// For TRAIT_ROLE
rs.NewRoleResource(name, rt, id, roleOpts)

// For TRAIT_APP
rs.NewAppResource(name, rt, id, appOpts)
```

## missing go.sum entry

```
missing go.sum entry for module providing package ...
```

**Cause:** go.sum not generated.

**Fix:**
```bash
go mod tidy
```

## rate limit exceeded

```
429 Too Many Requests
```

**Cause:** Using raw http.Client without rate limiting.

**Fix:** Use uhttp:
```go
httpClient, _ := uhttp.NewClient(ctx,
    uhttp.WithLogger(true, ctxzap.Extract(ctx)),
)
```

## provisioning failed: resource not found

**Cause:** ExternalId not set on resource.

**Fix:**
```go
resource, _ := rs.NewResource(name, rt, id,
    rs.WithExternalID(&v2.ExternalId{Id: nativeID}),
)
```

## validation succeeded but sync fails

**Cause:** Validate() doesn't actually test the connection.

**Fix:** Make Validate() call the API:
```go
func (c *Connector) Validate(ctx context.Context) error {
    _, err := c.client.GetCurrentUser(ctx)
    return err
}
```
