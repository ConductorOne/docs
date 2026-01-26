# Resource Checklist

Verify resource types, entitlements, and grants before shipping.

## Resource Types

- [ ] At least one resource with `TRAIT_USER`
- [ ] Each resource type has unique ID (lowercase: `user`, `group`, `project`)
- [ ] Resources with `TRAIT_GROUP` have a `member` entitlement
- [ ] Resources with `TRAIT_ROLE` have an `assigned` entitlement

## Entitlements

- [ ] Every entitlement specifies `grantableTo`
- [ ] `grantableTo` references existing resource types
- [ ] Entitlements have display names
- [ ] User resources do NOT have entitlements (users receive access, not grant it)

## Grants

- [ ] Resources with entitlements implement `Grants()`
- [ ] `Grants()` returns grants for ALL entitlement types on the resource
- [ ] Grant principals match `grantableTo` types

## Quick Verification

| Check | Command |
|-------|---------|
| Resources sync | `./baton-myservice && baton resources` |
| Entitlements exist | `baton entitlements` |
| Grants populated | `baton grants` |
| No orphan grants | Grants reference existing resources |

## Common Mistakes

**Modeling backwards:**
Users receive entitlements on groups/roles. If you're adding entitlements to user resources, reconsider.

**Missing grants:**
Defining entitlements but not implementing `Grants()` means ConductorOne sees what access exists but not who has it.

**Wrong grantableTo:**
If entitlement says `grantableTo: [user]`, grants must reference user resources, not groups.
