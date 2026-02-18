# Audit Events

All service principal and workload federation activity recorded in ConductorOne system log.

## Authentication Events

Token operations logged as OCSF Authentication events (class 3002). Activity name corresponds to OAuth grant type.

| Event | Activity name | Description |
|-------|---------------|-------------|
| Client credential grant | `client_credentials` | Service principal authenticated with client ID + secret or assertion |
| Token exchange | `token_exchange` | Workload federation token exchange (success or failure) |

Each event includes:
- **Outcome**: Success or Failure
- **Status detail**: Failure reason (e.g., `trust_not_found`, `issuer_mismatch`, `invalid_jwt_format`, `cel_condition_not_met`, `token_too_old`, `sp_disabled`)
- **Client IP**: Source IP address
- **Client ID**: Credential or trust client ID

## API Activity Events

CRUD operations logged as OCSF API Activity events.

| Event | API operation |
|-------|---------------|
| SP created | `ServicePrincipalService/Create` |
| SP deleted | `ServicePrincipalService/Delete` |
| Credential created | `ServicePrincipalService/CreateCredential` |
| Credential revoked | `ServicePrincipalService/RevokeCredential` |
| Provider created | `WorkloadFederationService/CreateProvider` |
| Provider deleted | `WorkloadFederationService/DeleteProvider` |
| Trust created | `WorkloadFederationService/CreateTrust` |
| Trust deleted | `WorkloadFederationService/DeleteTrust` |

## Common Failure Reasons

| Status detail | Cause |
|---------------|-------|
| `trust_not_found` | No matching trust for client ID |
| `issuer_mismatch` | JWT issuer doesn't match provider |
| `invalid_jwt_format` | Malformed JWT |
| `cel_condition_not_met` | CEL expression returned false |
| `token_too_old` | JWT issued more than 10 minutes ago |
| `sp_disabled` | Service principal is disabled |
| `ip_not_allowed` | Source IP not in allowlist |

## Viewing Events

Navigate to system log in ConductorOne admin console.
