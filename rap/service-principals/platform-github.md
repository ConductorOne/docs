# GitHub Actions Integration

Use `conductorone/oidc-token-action` for one-step secretless authentication.

## Prerequisites

- Service principal with GitHub Actions federation trust
- Trust's client ID (e.g., `swift-otter-19384@yourcompany.conductor.one/wfe`)

## Workflow Setup

Requires `id-token: write` permission:

```yaml
name: Deploy with ConductorOne

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: conductorone/oidc-token-action@v1
        with:
          audience: yourcompany.conductor.one
          client_id: swift-otter-19384@yourcompany.conductor.one/wfe

      # CONDUCTORONE_ACCESS_TOKEN now available
```

The action:
1. Requests GitHub OIDC token with tenant as audience
2. Exchanges for ConductorOne access token
3. Exports `CONDUCTORONE_ACCESS_TOKEN` and `CONDUCTORONE_CLIENT_ID`
4. Masks token in logs
5. Cleans up when job finishes

## Usage Examples

### Cone CLI
```yaml
- uses: conductorone/oidc-token-action@v1
  with:
    audience: yourcompany.conductor.one
    client_id: swift-otter-19384@yourcompany.conductor.one/wfe
- run: cone whoami
```

### Terraform
```yaml
- uses: conductorone/oidc-token-action@v1
  with:
    audience: yourcompany.conductor.one
    client_id: swift-otter-19384@yourcompany.conductor.one/wfe
- uses: hashicorp/setup-terraform@v3
- run: terraform apply
```

### Direct API
```yaml
- run: |
    curl -s "https://yourcompany.conductor.one/api/v1/apps" \
      -H "Authorization: Bearer $CONDUCTORONE_ACCESS_TOKEN"
```

## CEL Expressions

### Restrict to repository
```
claims.repository == "acme/infra"
```

### Restrict to repository and branch
```
claims.repository == "acme/infra" && claims.ref == "refs/heads/main"
```

### Restrict to repository and environment
```
claims.repository == "acme/infra" && claims.environment == "production"
```

### Pin to specific workflow
```
claims.job_workflow_ref == "acme/infra/.github/workflows/deploy.yml@refs/heads/main"
```

## GitHub OIDC Claims

| Claim | Example | Description |
|-------|---------|-------------|
| `repository` | `acme/infra` | Owner and repo name |
| `repository_owner` | `acme` | Organization or user |
| `ref` | `refs/heads/main` | Git ref |
| `environment` | `production` | GitHub Environment |
| `job_workflow_ref` | `acme/infra/.github/workflows/deploy.yml@refs/heads/main` | Full workflow reference |
| `actor` | `octocat` | User who triggered |
| `event_name` | `push` | Trigger event |

## Security

Enable GitHub Environments and add environment constraint to CEL for production. This prevents any branch/workflow from authenticating - only jobs in specified environment can.
