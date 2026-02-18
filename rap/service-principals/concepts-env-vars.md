# Environment Variables

All ConductorOne client tools recognize these environment variables.

## Variables

| Variable | Purpose |
|----------|---------|
| `CONDUCTORONE_CLIENT_ID` | Client ID for authentication |
| `CONDUCTORONE_CLIENT_SECRET` | Ed25519 private key for client credentials |
| `CONDUCTORONE_ACCESS_TOKEN` | Pre-exchanged bearer token (highest priority) |
| `CONDUCTORONE_OIDC_TOKEN` | Raw OIDC JWT for workload federation |
| `CONDUCTORONE_TENANT_DOMAIN` | Tenant domain override |
| `CONDUCTORONE_SERVER_URL` | Full server URL override |

## Priority Order

When multiple variables are set:

1. `CONDUCTORONE_ACCESS_TOKEN` - static bearer token, no exchange needed
2. `CONDUCTORONE_OIDC_TOKEN` - token exchange using `CONDUCTORONE_CLIENT_ID`
3. `CONDUCTORONE_CLIENT_ID` + `CONDUCTORONE_CLIENT_SECRET` - Ed25519 JWT assertion

## Supported Tools

- Go SDK
- Terraform provider
- Cone CLI
- oidc-token-action (GitHub Action)

All tools auto-detect these variables. No explicit configuration needed if variables are set.

## Client ID Format

Client IDs encode the tenant domain:
- Credentials: `clever-fox-42195@yourcompany.conductor.one/spc`
- Federation trusts: `swift-otter-19384@yourcompany.conductor.one/wfe`

Server URL is derived automatically from the client ID.
