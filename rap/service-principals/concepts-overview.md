# Service Principals Overview

Machine identities for ConductorOne API automation.

## What Service Principals Are

A service principal is a non-human identity for scripts, CI/CD pipelines, Terraform runs, and API integrations. It appears in the user directory with a robot avatar but is purpose-built for automation.

Each service principal has:
- Display name and unique ID
- Assigned ConductorOne roles (same as human users)
- One or more owners who manage it
- Multiple credentials or federation trusts

## When to Use

**Use service principals for:**
- Shared automation (CI/CD, Terraform, scheduled scripts)
- Production workloads where identity shouldn't be tied to a person
- Multi-credential scenarios (rotation, different environments)

**Don't need service principals for:**
- Personal API use (use Profile > API Keys instead)
- One-off scripts tied to your identity

## Two Authentication Methods

| Aspect | Client Credentials | Workload Federation |
|--------|-------------------|---------------------|
| How | Client ID + secret to token endpoint | External OIDC token exchanged for ConductorOne token |
| Secrets | Must store and rotate client secret | No secrets - uses CI/CD platform's OIDC |
| Best for | Local dev, scripts, cron jobs | GitHub Actions, GitLab CI, HCP Terraform |
| Lifetime | Max 180 days, must rotate | No credentials to manage |
| Security | Secret can leak | No secret to leak |
| Grant type | `client_credentials` | `urn:ietf:params:oauth:grant-type:token-exchange` |

A single service principal can use both methods simultaneously.

## Choosing the Method

**Client credentials** - Straightforward setup. Use for scripts, local development, environments where storing a secret is acceptable.

**Workload federation** - Production CI/CD. No secrets to rotate, tokens tied to individual workflow runs.

## Requirements

- Feature must be enabled (contact ConductorOne account team during early access)
- Super Admin role required to create service principals

## Limits

| Limit | Value |
|-------|-------|
| Maximum credential lifetime | 180 days |
| CEL expression size | 1,024 bytes |
| IP ranges per credential/trust | 32 |
| JWKS endpoint | Must be publicly accessible |
