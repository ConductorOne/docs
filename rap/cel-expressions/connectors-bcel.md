# CEL in Baton Connectors

Baton connectors (baton-http, baton-sql) use CEL for data transformation - mapping external data to Baton's resource model. This is different from policy CEL.

## Key Differences from Policy CEL

| Aspect | Policy CEL | Connector CEL |
|--------|------------|---------------|
| Purpose | Authorization decisions | Data transformation |
| Variables | `subject`, `entitlement`, `task` | `item`/`cols`, `response`, `resource` |
| Return types | `bool`, `User`, `list<User>` | Any (strings, maps, lists) |
| Functions | `c1.directory.*`, `c1.user.*` | `Slugify`, `ToLower`, `json_path` |
| Configuration | UI, Terraform | YAML config files |

---

## baton-http

Maps HTTP API responses to Baton resources.

### Variables

| Variable | Description |
|----------|-------------|
| `item` | Current item from API response array |
| `response` | Full HTTP response body |
| `headers` | HTTP response headers |
| `resource` | Current Baton resource context |

### Expression Prefix

```yaml
id: cel:item.id              # CEL expression
url: tmpl:/users/{{.id}}     # Go template
name: "literal value"        # Literal string
```

### Example Configuration

```yaml
resource_types:
  user:
    list:
      request:
        url: /api/users
      response:
        items_path: data.users
        resource_mapping:
          id: cel:item.id
          display_name: cel:item.firstName + " " + item.lastName
          traits:
            user:
              status: cel:item.active == true ? "enabled" : "disabled"
              emails:
                - cel:item.email
```

### Common Patterns

```yaml
# Conditional value
status: cel:item.status == "active" ? "enabled" : "disabled"

# Null-safe with has()
manager_id: cel:has(item.manager_id) ? item.manager_id : ""

# Type conversion
id: cel:string(item.numeric_id)
```

---

## baton-sql

Maps SQL query results to Baton resources.

### Variables

| Variable | Description |
|----------|-------------|
| `cols` | Map of column names to values from current row |
| `resource` | Current Baton resource context |
| `principal` | User/entity for provisioning |
| `entitlement` | Entitlement for provisioning |

### Example Configuration

```yaml
resource_types:
  user:
    list:
      query: |
        SELECT id, username, email, is_active
        FROM users WHERE deleted_at IS NULL
      mapping:
        id: cel:cols.id
        display_name: cel:cols.username
        traits:
          user:
            status: cel:cols.is_active == 1 ? "enabled" : "disabled"
```

### SQL-Specific Functions

| Function | Description |
|----------|-------------|
| `Slugify(string)` | Convert to URL-safe slug |
| `ToLower(string)` | Lowercase |
| `ToUpper(string)` | Uppercase |
| `TitleCase(string)` | Title case |
| `PHPDeserializeStringArray(string)` | Parse PHP serialized arrays |

---

## Null Handling

API/database responses often contain null values. The `has()` macro returns `true` for fields that exist but are null:

```cel
// has() returns true for null fields
has(item.manager_id)  // true even if manager_id is null

// Value will be empty string after coercion
item.manager_id  // null -> ""
```

For connector CEL, null values are coerced to empty strings automatically.
