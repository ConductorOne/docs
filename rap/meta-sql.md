# meta-sql

SQL database integration via YAML configuration.

---

## Supported Databases

- PostgreSQL (`postgres`)
- MySQL (`mysql`)
- SQL Server (`sqlserver`)
- Oracle (`oracle`)
- SAP HANA (`hana`)
- SQLite (`sqlite`)

## Connection

```yaml
connect:
  scheme: "postgres"
  host: "${DB_HOST}"
  port: "5432"
  database: "${DB_NAME}"
  user: "${DB_USER}"
  password: "${DB_PASS}"
  params:
    sslmode: "require"
```

Alternative DSN format:
```yaml
connect:
  dsn: "postgres://${DB_HOST}:5432/${DB_NAME}?sslmode=require"
  user: "${DB_USER}"
  password: "${DB_PASS}"
```

## Listing Resources

```yaml
resource_types:
  user:
    name: "User"
    list:
      query: |
        SELECT id, username, email, status, department
        FROM users
        WHERE active = true
        AND id > ?<Cursor>
        ORDER BY id ASC
        LIMIT ?<Limit>
      pagination:
        strategy: "cursor"
        primary_key: "id"
      map:
        id: ".id"
        display_name: ".username"
        traits:
          user:
            emails:
              - ".email"
            status: ".status == 'active' ? 'enabled' : 'disabled'"
```

## Query Placeholders

- `?<Cursor>` - Current pagination cursor
- `?<Limit>` - Page size
- `?<Offset>` - Offset for offset-based pagination
- `?<resource_id>` - Current resource ID in grants query
- `?<var_name>` - Named variable from `vars` block

## Grants Discovery

```yaml
grants:
  - query: |
      SELECT user_id, group_id
      FROM group_members
      WHERE group_id = ?<group_id>
    map:
      - principal_id: ".user_id"
        principal_type: "user"
        entitlement_id: "member"
        skip_if: ".user_type == 'system'"  # Optional filter
```

## Provisioning

```yaml
static_entitlements:
  - id: "member"
    display_name: "'Member'"
    purpose: "assignment"
    grantable_to:
      - "user"
    provisioning:
      vars:
        user_id: "principal.ID"
        group_id: "resource.ID"
      grant:
        queries:
          - |
            INSERT INTO group_members (user_id, group_id)
            VALUES (?<user_id>, ?<group_id>)
            ON CONFLICT DO NOTHING
      revoke:
        queries:
          - |
            DELETE FROM group_members
            WHERE user_id = ?<user_id> AND group_id = ?<group_id>
```

## Account Creation

```yaml
account_provisioning:
  schema:
    - name: "username"
      type: "string"
      required: true
    - name: "email"
      type: "string"
      required: true

  credentials:
    random_password:
      min_length: 16
      max_length: 32
      preferred: true

  create:
    vars:
      username: "input.username"
      email: "input.email"
      password: "password"
    queries:
      - |
        INSERT INTO users (username, email, password_hash)
        VALUES (?<username>, ?<email>, crypt(?<password>, gen_salt('bf')))
```

## Running

```bash
# Validate
baton-sql --config-path ./config.yaml --validate-config-only

# Sync
baton-sql --config-path ./config.yaml -f sync.c1z

# With provisioning
baton-sql --config-path ./config.yaml \
  --client-id "$C1_CLIENT_ID" \
  --client-secret "$C1_CLIENT_SECRET" \
  --provisioning
```
