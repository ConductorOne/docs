# Connector Development RAP Index

Agent-optimized documentation for building ConductorOne connectors.

## Available Sections

| Section | File | Covers |
|---------|------|--------|
| Getting started | `build-setup.md` | Project structure, SDK setup, first connector |
| Access model concepts | `concepts-model.md` | Resources, entitlements, grants, traits |
| Config gotchas | `gotchas-config.md` | mapstructure tags, Configurable interface |
| Type system gotchas | `gotchas-types.md` | Import paths, resource builders, traits |
| API usage gotchas | `gotchas-api.md` | uhttp client, ExternalId, error messages |
| Resource checklist | `checklist-resources.md` | Resource types, entitlements, grants |
| Provisioning checklist | `checklist-provisioning.md` | Grant/Revoke, ExternalId, Validate |
| Error reference | `debug-errors.md` | Common error messages and fixes |

## Selection Guidelines

**User asks "how do I..."**
- Start a new connector -> `build-setup.md`
- Understand resources/entitlements -> `concepts-model.md`
- Fix a specific error -> `debug-errors.md`
- Ship my connector -> `checklist-resources.md`, `checklist-provisioning.md`

**User shows code with errors**
- `VerifyStructFields failed` -> `gotchas-config.md`
- `does not contain package` -> `gotchas-types.md`
- `cannot use cfg as field.Configurable` -> `gotchas-config.md`
- `missing expected trait` -> `gotchas-types.md`

**User asks about concepts**
- What is an entitlement -> `concepts-model.md`
- What is grantableTo -> `concepts-model.md`
- How do traits work -> `concepts-model.md`

**User wants to verify completeness**
- Before shipping -> `checklist-resources.md` + `checklist-provisioning.md`
- What am I missing -> `checklist-resources.md`
