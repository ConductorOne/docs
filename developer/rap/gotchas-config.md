# Config Gotchas

Configuration-related issues in connector development.

## mapstructure tags required

Every Config struct field must have a `mapstructure` tag matching the field name used in `DefineConfiguration`.

**Error:**
```
VerifyStructFields failed: field my-field in confschema does not have
a corresponding struct tag in the configuration struct
```

**Wrong:**
```go
type Config struct {
    APIKey string  // Missing tag
}
```

**Correct:**
```go
type Config struct {
    APIKey string `mapstructure:"api-key"`
}
```

## Configurable interface required

Config struct must implement getter methods.

**Error:**
```
cannot use cfg (variable of type *Config) as field.Configurable value
```

**Required methods:**
```go
func (c *Config) GetString(key string) string {
    switch key {
    case "api-key":
        return c.APIKey
    case "base-url":
        return c.BaseURL
    }
    return ""
}

func (c *Config) GetBool(key string) bool             { return false }
func (c *Config) GetInt(key string) int               { return 0 }
func (c *Config) GetStringSlice(key string) []string  { return nil }
func (c *Config) GetStringMap(key string) map[string]any { return nil }
```

## Field name must match tag

The string passed to `field.StringField` must exactly match the `mapstructure` tag.

**Wrong:**
```go
field.StringField("apiKey", ...)  // camelCase

type Config struct {
    APIKey string `mapstructure:"api-key"`  // kebab-case
}
```

**Correct:**
```go
field.StringField("api-key", ...)  // Same as tag

type Config struct {
    APIKey string `mapstructure:"api-key"`
}
```

## DefineConfiguration before NewCmd

`DefineConfiguration` must be called before `cli.NewCmd`.

**Wrong:**
```go
cmd, err := cli.NewCmd(ctx, "baton-myservice", cfg, getConnector)
// DefineConfiguration never called - no CLI flags
```

**Correct:**
```go
_, cmd, err := configSdk.DefineConfiguration(ctx, cfg,
    field.StringField("api-key", field.WithRequired(true)),
)
// Now cfg is wired to CLI flags
cmd, err = cli.NewCmd(ctx, "baton-myservice", cfg, getConnector)
```
