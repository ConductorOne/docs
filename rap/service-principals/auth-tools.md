# Terraform and Cone CLI

Configure ConductorOne tools with service principal credentials.

## Terraform Provider

Server URL derived automatically from client ID.

### Provider Block

```hcl
provider "conductorone" {
  client_id     = "clever-fox-42195@yourcompany.conductor.one/spc"
  client_secret = var.conductorone_client_secret
}
```

### Environment Variables

```bash
export CONDUCTORONE_CLIENT_ID="clever-fox-42195@yourcompany.conductor.one/spc"
export CONDUCTORONE_CLIENT_SECRET="secret-token:YOUR_SECRET_HERE"

terraform plan
```

### With Workload Federation

For HCP Terraform, set `TFC_WORKLOAD_IDENTITY_AUDIENCE` in workspace. Provider auto-detects the token:

```hcl
provider "conductorone" {
  client_id = "clever-fox@yourcompany.conductor.one/wfe"
}
```

## Cone CLI

Set environment variables:

```bash
export CONDUCTORONE_CLIENT_ID="clever-fox-42195@yourcompany.conductor.one/spc"
export CONDUCTORONE_CLIENT_SECRET="secret-token:YOUR_SECRET_HERE"

cone whoami
```

Or with pre-exchanged token:

```bash
export CONDUCTORONE_ACCESS_TOKEN="eyJhbGciOiJFZERTQSIs..."

cone whoami
```

## Security

Never commit client secrets to source control. Use:
- CI/CD platform secret management
- Environment variables
- Vault or secrets manager
