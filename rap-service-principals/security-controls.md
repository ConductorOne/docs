# Security Controls

Security features for service principals and workload federation.

## Scoped Roles

Every credential and trust can be limited to a subset of service principal's roles.

Effective permissions = intersection of:
1. Roles assigned to service principal
2. Scoped roles on credential or trust

If no scoped roles selected ("Full permissions"), inherits all service principal's roles.

| Role | Description | Use case |
|------|-------------|----------|
| Full permissions | All assigned roles | General automation |
| Basic User | Standard user permissions | Access requests |
| Read-Only Administrator | Read-only all features | Monitoring, dashboards |
| Read-Only to System Logs | View system logs only | SIEM integration |

## IP Allowlists

Credentials and trusts support IP restrictions.

- Up to 32 IP ranges per credential/trust
- Empty = allow all IPs
- Supports IPv4 and IPv6 (e.g., `192.168.1.0/24`, `2001:db8::/32`)

**Note**: IP allowlists work best with self-hosted runners or fixed egress IPs. GitHub-hosted runners use thousands of frequently-changing IPs.

## Credential Expiration

| Duration | Use case |
|----------|----------|
| 30 days | Temporary automation |
| 60 days | Medium-term |
| 90 days | Recommended default |
| 180 days | Maximum allowed |

Expiration cannot be extended. Create new credential and revoke old one.

## DPoP (Demonstrating Proof-of-Possession)

RFC 9449. Binds tokens to cryptographic key. Even if token intercepted, can't be used without private key.

When enabled:
- Client must include `DPoP` proof header with every token request
- Issued tokens are type `DPoP` instead of `Bearer`
- API requests require token and fresh DPoP proof

Advanced feature for high-security environments.

## Token Freshness

Federation trusts require tokens issued within last 10 minutes. Prevents replay of old tokens.

## Audit Logging

All activity recorded in system log. See `security-audit.md` for event details.
