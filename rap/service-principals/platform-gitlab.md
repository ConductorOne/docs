# GitLab CI Integration

Use GitLab's built-in `id_tokens` with curl token exchange.

## Prerequisites

- Service principal with GitLab CI federation trust (use GitLab CI/CD preset)
- Trust's client ID (e.g., `bright-eagle-55012@yourcompany.conductor.one/wfe`)

## Pipeline Setup

```yaml
deploy:
  id_tokens:
    C1_TOKEN:
      aud: yourcompany.conductor.one
  script:
    - >
      C1_ACCESS_TOKEN=$(curl -s -X POST
      "https://yourcompany.conductor.one/auth/v1/token"
      -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange"
      -d "subject_token=$C1_TOKEN"
      -d "subject_token_type=urn:ietf:params:oauth:token-type:jwt"
      -d "client_id=bright-eagle-55012@yourcompany.conductor.one/wfe"
      | jq -r '.access_token')
    - >
      curl -s "https://yourcompany.conductor.one/api/v1/apps"
      -H "Authorization: Bearer $C1_ACCESS_TOKEN"
```

The `id_tokens` block generates signed JWT with tenant domain as audience. Token available as `C1_TOKEN` environment variable.

## CEL Expressions

### Restrict to project
```
claims.project_path == "acme/infra"
```

### Restrict to protected refs only
```
claims.project_path == "acme/infra" && claims.ref_protected == "true"
```

### Restrict to specific branch
```
claims.project_path == "acme/infra" && claims.ref == "main" && claims.ref_protected == "true"
```

## GitLab OIDC Claims

| Claim | Example | Description |
|-------|---------|-------------|
| `project_path` | `acme/infra` | Full project path |
| `project_id` | `12345` | Numeric project ID |
| `namespace_path` | `acme` | Group or user namespace |
| `ref` | `main` | Branch or tag name |
| `ref_protected` | `true` | Whether ref is protected |
| `ref_type` | `branch` | `branch` or `tag` |
| `pipeline_source` | `push` | Pipeline trigger |
| `environment` | `production` | Environment name |
| `environment_protected` | `true` | Whether environment is protected |

## Security

Keep `claims.ref_protected == "true"` to ensure only protected branches/tags authenticate. For high-privilege access, also bind to specific ref value.
