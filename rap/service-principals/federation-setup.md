# Setting Up Federation

Create a provider and trust using the ConductorOne wizard.

## Prerequisites

A service principal. If you don't have one, create it first (Settings > Developers > Service principals). You don't need a credential - federation replaces credentials with OIDC tokens.

## Create a Federation Trust

1. On service principal detail page, select Federation tab
2. Click Set up federation
3. Choose a provider (select existing or create new)
4. Configure the trust:
   - Wizard generates CEL expression from your inputs
   - Switch to manual mode for custom CEL
   - Optional: Add IP restrictions and scoped roles
5. Click Create
6. Copy the client ID

## Test Your Token

Before deploying, validate the trust:

1. Click trust in Federation tab to open detail drawer
2. Click Test
3. Paste sample JWT or provide claims as JSON
4. Test runner validates each step:

| Step | What it checks |
|------|---------------|
| JWT decode | Valid JWT format |
| Issuer match | Matches provider |
| Signature validation | Valid via JWKS |
| Audience validation | Matches tenant |
| Token freshness | Issued within 10 minutes |
| CEL evaluation | Condition returns true |
| IP address check | In allowlist (if configured) |

## Test CEL Tool

Settings > Workload Federation has a Test CEL tool. Test expressions against sample claims without a real JWT. Useful for iterating before creating a trust.

## Platform Guides

After creating trust, follow platform-specific integration:
- GitHub Actions: `platform-github.md`
- GitLab CI: `platform-gitlab.md`
- HCP Terraform: `platform-terraform.md`
- Custom OIDC: `platform-custom.md`
