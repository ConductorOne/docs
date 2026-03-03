# meta-cel

Data transformation with Common Expression Language in meta-connectors.

---

## What is CEL

CEL (Common Expression Language) is used in baton-http and baton-sql for:
- Field mapping from API/SQL responses
- Conditional logic
- String transformation
- Type conversion

Think of it as a safer alternative to embedding code in config.

## Basic Syntax

```yaml
map:
  # Direct field access
  id: ".id"

  # String concatenation
  display_name: ".first_name + ' ' + .last_name"

  # Ternary conditional
  status: ".is_active ? 'enabled' : 'disabled'"

  # Null handling
  last_login: ".last_login != null ? string(.last_login) : ''"
```

## Available Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `lowercase()` | To lowercase | `lowercase(.email)` |
| `uppercase()` | To uppercase | `uppercase(.code)` |
| `titlecase()` | Title case | `titlecase(.name)` |
| `trim()` | Remove whitespace | `trim(.value)` |
| `match()` | Regex match | `match(.email, ".*@corp\\.com")` |
| `extract()` | Regex extract | `extract(.urn, "user-([0-9]+)")` |
| `replace()` | String replace | `replace(.name, {"old": "_", "new": "-"})` |
| `get()` | Get with default | `get(.optional, "default")` |
| `has()` | Check field exists | `has(input.employee_id)` |
| `parse_json()` | Parse JSON string | `parse_json(.metadata).type` |
| `json_path()` | Extract from JSON | `json_path(.data, "user.name")` |
| `string()` | Convert to string | `string(.numeric_id)` |

## Context Variables

| Variable | Available In | Description |
|----------|--------------|-------------|
| `.column` or `item` | List, Grants | Current row/item |
| `resource` | Grants, Provisioning | Current resource |
| `principal` | Provisioning | User being modified |
| `entitlement` | Provisioning | Entitlement being modified |
| `input` | Account creation | User-provided values |
| `password` | Account creation | Generated password |

## Common Patterns

**Account type from field:**
```yaml
account_type: ".type == 'employee' ? 'human' : 'service'"
```

**Email from multiple possible fields:**
```yaml
emails:
  - "has(.primary_email) ? .primary_email : .email"
```

**Status normalization:**
```yaml
status: ".status == 'active' || .status == 'enabled' ? 'enabled' : 'disabled'"
```

**Skip system accounts in grants:**
```yaml
grants:
  - query: "SELECT * FROM role_members WHERE role_id = ?<role_id>"
    map:
      - skip_if: ".account_type == 'system'"
        principal_id: ".user_id"
        principal_type: "user"
        entitlement_id: "member"
```

**Build display name:**
```yaml
display_name: "titlecase(.first_name) + ' ' + titlecase(.last_name)"
```

**Handle optional nested field:**
```yaml
department: "has(.profile) && has(.profile.department) ? .profile.department : 'Unknown'"
```

## Provisioning Variables

```yaml
provisioning:
  vars:
    user_id: "principal.ID"           # Principal's resource ID
    group_id: "resource.ID"           # Target resource ID
    email: "principal.DisplayName"    # Can access other fields
    timestamp: "now()"                # Current timestamp
  grant:
    queries:
      - "INSERT INTO members VALUES (?<user_id>, ?<group_id>, ?<timestamp>)"
```

## Type Coercion

CEL is type-aware. Convert explicitly when needed:

```yaml
# Integer to string
id: "string(.numeric_id)"

# String to bool (if needed)
active: ".status == 'active'"

# Handle null
value: ".field != null ? .field : ''"
```
