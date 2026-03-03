# ref-config

Configuration system reference for baton connectors.

---

## Precedence

1. CLI flags (`--domain example.com`)
2. Environment variables (`BATON_DOMAIN=example.com`)
3. Config files (YAML)

CLI wins over env, env wins over file.

---

## Standard flags (all connectors)

### Output & logging

| Flag | Default | Description |
|------|---------|-------------|
| `--file`, `-f` | `sync.c1z` | Output file path |
| `--log-level` | `info` | `debug`, `info`, `warn`, `error` |
| `--log-format` | auto | `json` or `console` |

### Daemon mode

| Flag | Description |
|------|-------------|
| `--client-id` | C1 OAuth client ID (enables daemon mode) |
| `--client-secret` | C1 OAuth client secret |
| `--skip-full-sync` | Disable full sync in daemon mode |

### Provisioning

| Flag | Description |
|------|-------------|
| `--provisioning` | Enable provisioning mode |
| `--grant-entitlement` | Entitlement ID to grant |
| `--grant-principal` | Resource ID receiving grant |
| `--revoke-grant` | Grant ID to revoke |

### Account management

| Flag | Description |
|------|-------------|
| `--create-account-login` | Login for new account |
| `--create-account-email` | Email for new account |
| `--delete-resource` | Resource ID to delete |
| `--rotate-credentials` | Resource ID for rotation |

### Targeted sync

| Flag | Description |
|------|-------------|
| `--sync-resources` | Specific resource IDs to sync |
| `--sync-resource-types` | Resource types to sync |
| `--skip-entitlements-and-grants` | Skip E&G during sync |

---

## Environment variables

All flags map to `BATON_` prefixed env vars:

```bash
--domain        -> BATON_DOMAIN
--api-key       -> BATON_API_KEY
--base-dn       -> BATON_BASE_DN
--client-id     -> BATON_CLIENT_ID
```

Rules:
- Prefix: `BATON_`
- Dashes become underscores
- Case insensitive

---

## Config file

```yaml
# ~/.baton/config.yaml
domain: example.okta.com
api-token: "00abc123..."
log-level: debug

# Arrays
skip-groups:
  - "Test Group"
  - "Temp Users"
```

Checked in order:
1. `--config` flag path
2. `./baton.yaml`
3. `~/.baton/config.yaml`

---

## Field types (for connector authors)

### StringField

```go
field.StringField("domain",
    field.WithRequired(true),
    field.WithDescription("Your Okta domain"),
)
```

### BoolField

```go
field.BoolField("ldaps",
    field.WithDefaultValue(false),
)
```

### IntField

```go
field.IntField("port",
    field.WithDefaultValue(389),
)
```

### StringSliceField

```go
field.StringSliceField("skip-groups",
    field.WithDescription("Groups to exclude"),
)
```

CLI: `--skip-groups "Group1" --skip-groups "Group2"`
Env: `BATON_SKIP_GROUPS="Group1,Group2"`

### SelectField (enum)

```go
field.SelectField("auth-type", []string{"token", "oauth", "basic"},
    field.WithDefaultValue("token"),
)
```

---

## Field options

| Option | Purpose |
|--------|---------|
| `WithRequired(true)` | Must be provided |
| `WithIsSecret(true)` | Masked in logs/UI |
| `WithDefaultValue(v)` | Default if not set |
| `WithHidden(true)` | Hidden from help |
| `WithPlaceholder(s)` | GUI placeholder text |
| `WithDescription(s)` | Help text |

---

## Defining custom fields

```go
func main() {
    ctx := context.Background()

    fields := []field.SchemaField{
        field.StringField("domain",
            field.WithRequired(true),
            field.WithDescription("Okta domain (e.g., example.okta.com)"),
        ),
        field.StringField("api-token",
            field.WithRequired(true),
            field.WithIsSecret(true),
            field.WithDescription("Okta API token"),
        ),
        field.StringSliceField("skip-groups"),
    }

    cfg := &Config{}
    c, err := cli.NewCobra(ctx, "baton-okta", cfg,
        cli.WithSchema(fields...),
    )
    // ...
}

type Config struct {
    Domain    string   `mapstructure:"domain"`
    APIToken  string   `mapstructure:"api-token"`
    SkipGroups []string `mapstructure:"skip-groups"`
}
```

Access in connector:
```go
func NewConnector(ctx context.Context, cfg *Config) (*Connector, error) {
    client := NewClient(cfg.Domain, cfg.APIToken)
    return &Connector{client: client, skipGroups: cfg.SkipGroups}, nil
}
```
