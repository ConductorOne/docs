# Lifecycle Management

View, edit, disable, and delete service principals.

## Viewing

**Settings > Developers > Service principals** - all service principals in tenant. Click any to view details, credentials, trusts.

**Directory > Users** - service principals appear with robot avatar. Use Origin filter > Local to find them (Local origin distinguishes from directory-synced users).

## Editing

On service principal detail page:
- Click display name to edit inline
- Use Enable/Disable toggle to activate/deactivate
- Click Delete to permanently remove (removes all credentials and trusts)

**Disabling blocks all API access** - both new token issuance and existing tokens. Takes effect within ~90 seconds due to caching.

## Editing Credentials

Click credential in Credentials tab to open drawer. Can update:
- Display name
- IP allowlist
- Scoped roles
- DPoP requirement

**Cannot change**: Expiration (create new credential instead)

## Editing Federation Trusts

Click trust in Federation tab to open drawer. Click Edit to modify:
- Display name
- CEL condition (AI assistance available)
- IP allowlist
- Scoped roles

Use Enable/Disable toggle in drawer header to activate/deactivate without deleting.

## Editing Providers

Click provider in Settings > Developers > Workload federation. Click pencil icon to rename.

**Cannot change**: Issuer URL (existing trusts depend on it)

Use Enable/Disable toggle to activate/deactivate.

## Deleting

### Service Principal
Click Delete on detail page. Permanently removes service principal and all credentials/trusts.

### Federation Trust
1. Open trust detail drawer
2. Click Delete
3. Confirm

### Credential
Revoke instead of delete. See `manage-credentials.md`.
