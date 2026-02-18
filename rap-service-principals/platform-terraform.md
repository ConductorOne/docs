# HCP Terraform Integration

ConductorOne Terraform provider auto-detects HCP Terraform workload identity tokens.

## Prerequisites

- Service principal with HCP Terraform federation trust (use HCP Terraform preset)
- Trust's client ID (e.g., `clever-fox@yourcompany.conductor.one/wfe`)

## Step 1: Configure Workspace

Set environment variable in HCP Terraform workspace:

| Variable | Value |
|----------|-------|
| `TFC_WORKLOAD_IDENTITY_AUDIENCE` | `yourcompany.conductor.one` |

HCP Terraform auto-generates `TFC_WORKLOAD_IDENTITY_TOKEN` for each run.

## Step 2: Configure Provider

Provider auto-detects the token:

```hcl
provider "conductorone" {
  client_id = "clever-fox@yourcompany.conductor.one/wfe"
}
```

When `terraform plan` or `terraform apply` runs, provider exchanges workload identity token automatically.

### Explicit Configuration

For multiple audiences, use Terraform variable:

```hcl
variable "tfc_conductorone_token" {
  type      = string
  sensitive = true
  default   = ""
}

provider "conductorone" {
  oidc_token = var.tfc_conductorone_token
  client_id  = "clever-fox@yourcompany.conductor.one/wfe"
}
```

Set `TFC_WORKLOAD_IDENTITY_AUDIENCE_CONDUCTORONE` to generate `TFC_WORKLOAD_IDENTITY_TOKEN_CONDUCTORONE`.

## Provider Auth Priority

1. `CONDUCTORONE_ACCESS_TOKEN` (static bearer token)
2. `oidc_token` attribute, then `CONDUCTORONE_OIDC_TOKEN`, then `TFC_WORKLOAD_IDENTITY_TOKEN`
3. `client_id` + `client_secret` attributes or env vars

## CEL Expressions

### Restrict to organization and workspace
```
claims.terraform_organization == "acme" && claims.terraform_workspace_name == "infra-prod"
```

### Restrict to apply phase only
```
claims.terraform_organization == "acme" && claims.terraform_workspace_name == "infra-prod" && claims.terraform_run_phase == "apply"
```

## HCP Terraform OIDC Claims

| Claim | Example | Description |
|-------|---------|-------------|
| `terraform_organization` | `acme` | Organization name |
| `terraform_workspace_name` | `infra-prod` | Workspace name |
| `terraform_workspace_id` | `ws-abc123` | Workspace ID |
| `terraform_run_phase` | `apply` | `plan` or `apply` |
| `terraform_run_id` | `run-xyz789` | Unique run ID |
| `terraform_project_name` | `infrastructure` | Project name |

## Security

Restrict to "apply only" to prevent plan-phase runs from obtaining credentials. For separate plan/apply permissions, create two trusts with different scoped roles.
