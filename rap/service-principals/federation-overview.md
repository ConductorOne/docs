# Workload Federation Overview

Secretless authentication using OIDC tokens from CI/CD platforms.

## How It Works

1. CI/CD platform issues signed JWT for current workflow run
2. Workflow sends JWT to ConductorOne token exchange endpoint
3. ConductorOne validates: issuer, signature, audience, freshness, CEL conditions
4. ConductorOne issues short-lived access token scoped to service principal's roles

No secrets stored. OIDC token valid only for single CI/CD run.

## Two Building Blocks

### Providers

An OIDC token issuer (e.g., GitHub Actions, HCP Terraform). Created once at tenant level, shared across service principals.

Each provider has:
- Issuer URL (e.g., `https://token.actions.githubusercontent.com`)
- Public JWKS endpoint for signature verification

Built-in presets:
| Provider | Issuer URL |
|----------|-----------|
| GitHub Actions | `https://token.actions.githubusercontent.com` |
| GitLab CI/CD | `https://gitlab.com` (or self-managed) |
| HCP Terraform | `https://app.terraform.io` (or custom) |
| AWS IAM Outbound | Account-specific |
| Custom OIDC | Any HTTPS issuer |

### Trusts

Binds a provider to a service principal with conditions. Controls which tokens are accepted and what permissions they receive.

Each trust has:
- Client ID (e.g., `swift-otter-19384@yourcompany.conductor.one/wfe`)
- CEL condition expression (evaluated against JWT claims)
- Optional IP restrictions and scoped roles

## Token Exchange

Endpoint: `https://{tenant}.conductor.one/auth/v1/token`

Grant type: `urn:ietf:params:oauth:grant-type:token-exchange`

```bash
curl -s -X POST "https://yourcompany.conductor.one/auth/v1/token" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=$OIDC_JWT" \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:jwt" \
  -d "client_id=swift-otter-19384@yourcompany.conductor.one/wfe"
```

## Provider Requirements

Any OIDC-compliant provider that:
1. Serves `/.well-known/openid-configuration` at issuer URL
2. Has publicly accessible JWKS endpoint
3. Issues JWTs with standard claims (`iss`, `aud`, `exp`, `iat`)
