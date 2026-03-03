# Credential Management

Rotate and revoke service principal credentials.

## Credential Rotation

Zero-downtime rotation procedure:

1. Create new credential on same service principal
2. Update automation to use new client ID and secret
3. Verify new credential works
4. Revoke old credential

Service principals can have multiple active credentials simultaneously.

## Revoking Credentials

1. On service principal detail page, select Credentials tab
2. Click credential to open drawer
3. Click Revoke and confirm

Revoking immediately prevents credential from issuing new tokens.

## Expiration

Credentials expire after set duration (30, 60, 90, or 180 days).

Expired credentials can't issue new tokens. Tokens issued before expiry remain valid until natural expiration (typically 1 hour).

**Expiration cannot be extended.** Create new credential before old one expires.

## Best Practices

- Set calendar reminder before expiration
- Rotate credentials before expiry, not after
- Keep old credential active until new one verified
- Use 90-day expiration as default
- Document which systems use which credentials

## Troubleshooting

**Token request fails after rotation**
- Verify using new client ID and secret
- Check secret includes `secret-token:` prefix

**Credential expired**
- Create new credential
- Update all systems using old credential
- Cannot restore expired credential

**Multiple credentials**
- Each credential has unique client ID
- Track which systems use which credential
- Revoke unused credentials
