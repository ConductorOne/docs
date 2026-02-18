# meta-http

REST API integration via YAML configuration, no Go code required.

---

## When to Use

- Target system has REST/HTTP endpoints
- Access model is straightforward
- You want ops teams to maintain the integration
- Quick integration matters more than flexibility

## Basic Structure

```yaml
version: "1"
app_name: "My SaaS App"
app_description: "Syncs users and roles"

connect:
  base_url: "https://api.example.com/v1"
  auth:
    type: "bearer"
    token: "${API_KEY}"

resource_types:
  user:
    name: "User"
    list:
      request:
        url: "/users"
        method: "GET"
      response:
        items_path: "data.users"
      map:
        id: ".id"
        display_name: ".name"
        traits:
          user:
            emails:
              - ".email"
```

## Authentication Types

```yaml
# Bearer token
auth:
  type: "bearer"
  token: "${API_KEY}"

# API key in header
auth:
  type: "api_key"
  header: "X-API-Key"
  key: "${API_KEY}"

# Basic auth
auth:
  type: "basic"
  username: "${USERNAME}"
  password: "${PASSWORD}"

# OAuth2 client credentials
auth:
  type: "oauth2_client_credentials"
  client_id: "${CLIENT_ID}"
  client_secret: "${CLIENT_SECRET}"
  token_url: "https://auth.example.com/oauth/token"
```

## Request Configuration

```yaml
list:
  request:
    url: "/users"
    method: "GET"
    headers:
      Accept: "application/json"
    query_params:
      status: "active"
  response:
    items_path: "data.users"    # JSONPath to array
```

## URL Templates

Dynamic URLs using Go templates:

```yaml
grants:
  - request:
      url: "tmpl:/groups/{{.resource.id}}/members"
      method: "GET"
```

Available variables:
- `.resource` - Current resource
- `.principal` - User for provisioning
- `.item` - Current item in iteration

## Pagination

```yaml
pagination:
  strategy: "offset"
  limit_param: "per_page"
  offset_param: "page"
  page_size: 100
  total_path: "meta.total"    # Optional
```

Or cursor-based:
```yaml
pagination:
  strategy: "cursor"
  cursor_param: "cursor"
  cursor_path: "meta.next_cursor"
```

## Response Mapping

```yaml
map:
  id: ".id"
  display_name: ".attributes.name"
  traits:
    user:
      emails:
        - ".attributes.email"
      status: ".attributes.active ? 'enabled' : 'disabled'"
```

## Running

```bash
# Validate first
baton-http --config-path ./config.yaml --validate-config-only

# One-shot sync
baton-http --config-path ./config.yaml -f sync.c1z

# Inspect results
baton resources -f sync.c1z
```
