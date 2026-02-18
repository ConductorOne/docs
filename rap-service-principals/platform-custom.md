# Custom OIDC Integration

Generic token exchange for any OIDC-compliant provider.

## Provider Requirements

OIDC provider must:
1. Serve `/.well-known/openid-configuration` at issuer URL
2. Have publicly accessible JWKS endpoint
3. Issue JWTs with standard claims: `iss`, `aud`, `exp`, `iat`

## Prerequisites

- Service principal with Custom OIDC federation trust (use Custom OIDC preset, enter provider's issuer URL)
- Trust's client ID (e.g., `quiet-bear-88456@yourcompany.conductor.one/wfe`)

## Token Exchange

```bash
curl -s -X POST "https://yourcompany.conductor.one/auth/v1/token" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=$YOUR_JWT" \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:jwt" \
  -d "client_id=quiet-bear-88456@yourcompany.conductor.one/wfe"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJFZERTQSIs...",
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "token_type": "Bearer",
  "expires_in": 1800
}
```

## Token Requirements

| Requirement | Detail |
|-------------|--------|
| Issuer (`iss`) | Must match provider's issuer URL exactly |
| Audience (`aud`) | Must contain tenant domain |
| Expiration (`exp`) | Must not be expired |
| Issued at (`iat`) | Must be within last 10 minutes |
| Signature | Must be verifiable via JWKS |

## CEL Expressions

Validate `sub` claim and additional claims:

```
claims.sub == "expected-subject" && claims.custom_claim == "expected-value"
```

### Tips

- Always validate `sub` or equivalent unique identifier
- Use additional claims for defense-in-depth
- String functions available: `contains()`, `startsWith()`, `endsWith()`, `matches()`, `size()`
- Namespaced claims: `claims["https://example.com/"].field`
- Max expression size: 1,024 bytes

## Using with Tools

Set environment variables:

```bash
export CONDUCTORONE_ACCESS_TOKEN=$(curl -s -X POST ... | jq -r '.access_token')

cone whoami
terraform apply
```

Or set `CONDUCTORONE_OIDC_TOKEN` with raw JWT and `CONDUCTORONE_CLIENT_ID` - tools handle exchange internally.

## Security

Always validate `sub` claim. Use additional claims for defense-in-depth. A CEL expression checking only one claim may be too permissive.
