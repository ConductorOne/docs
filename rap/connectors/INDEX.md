# Baton Connector Documentation Index

Documentation for building ConductorOne Baton connectors. Request relevant sections based on user's question.

## How to Use

1. Read user's question
2. Identify relevant sections (up to 3-4)
3. Request those files
4. Answer using retrieved content

## Available Sections

### Conceptual

| Section | File | Covers |
|---------|------|--------|
| What connectors do | `concepts-overview.md` | Problem solved, sync vs provision, reconciliation loop |
| Resource model | `concepts-resources.md` | Resources, entitlements, grants, traits |
| Sync lifecycle | `concepts-sync.md` | Four stages, pagination |
| ID correlation | `concepts-ids.md` | RawId, external_id, matching across syncs |

### Building Connectors

| Section | File | Covers |
|---------|------|--------|
| Project setup | `build-setup.md` | Directory structure, go.mod, main.go |
| ResourceSyncer | `build-syncer.md` | ResourceType(), List(), Entitlements(), Grants() |
| Pagination | `build-pagination.md` | Token vs Bag, cursor vs offset, nested |

### Provisioning

| Section | File | Covers |
|---------|------|--------|
| Grant and Revoke | `provision-grant.md` | ResourceProvisionerV2, Grant/Revoke |

### Recipes (Cookbook)

| Section | File | Covers |
|---------|------|--------|
| Authentication | `recipes-auth.md` | API key, OAuth2, JWT, LDAP, basic auth |
| Error handling | `recipes-errors.md` | Retryable vs fatal, context cancellation |
| Resource modeling | `recipes-modeling.md` | Hierarchies, traits, entitlements, grants |
| Testing | `recipes-testing.md` | Configurable base URL, mock servers, unit tests |
| Caching | `recipes-caching.md` | sync.Map, LRU, daemon mode, anti-patterns |

### Meta-Connectors

| Section | File | Covers |
|---------|------|--------|
| baton-http | `meta-http.md` | REST API via YAML config |
| baton-sql | `meta-sql.md` | Database via YAML config |
| CEL expressions | `meta-cel.md` | Data transformation |

### Operations

| Section | File | Covers |
|---------|------|--------|
| Run modes | `ops-modes.md` | One-shot vs daemon |

### Troubleshooting

| Section | File | Covers |
|---------|------|--------|
| Debugging workflow | `debug-workflow.md` | Step-by-step process |
| Common errors | `debug-errors.md` | Pagination loops, auth, rate limits |
| Key patterns | `patterns.md` | Entity sources, HTTP handling, pagination, idempotency |

### Reference

| Section | File | Covers |
|---------|------|--------|
| SDK interfaces | `ref-sdk.md` | ConnectorBuilder, ResourceSyncer, Provisioner |
| Configuration | `ref-config.md` | Flags, env vars, field types |
| C1 API | `ref-c1api.md` | Task types, lifecycle, heartbeat |
| FAQ | `ref-faq.md` | Common questions |
| Glossary | `ref-glossary.md` | Term definitions |

### Publishing & Community

| Section | File | Covers |
|---------|------|--------|
| Publishing | `publish-submit.md` | Registry, versioning, signing |
| Community | `community.md` | Getting help, contributing, reporting |

---

## Selection Guidelines

**"How do I..."**
- Build a connector -> `build-setup.md`, `build-syncer.md`
- Add pagination -> `build-pagination.md`
- Support provisioning -> `provision-grant.md`
- Connect REST API -> `meta-http.md`
- Connect database -> `meta-sql.md`
- Authenticate -> `recipes-auth.md`
- Handle errors -> `recipes-errors.md`
- Model resources -> `recipes-modeling.md`
- Test my connector -> `recipes-testing.md`
- Cache data -> `recipes-caching.md`
- Debug a problem -> `debug-workflow.md`, `debug-errors.md`
- Run in production -> `ops-modes.md`
- Publish my connector -> `publish-submit.md`
- Contribute -> `community.md`

**"What is..."**
- A connector -> `concepts-overview.md`
- An entitlement/grant -> `concepts-resources.md`
- The sync lifecycle -> `concepts-sync.md`
- RawId -> `concepts-ids.md`
- CEL -> `meta-cel.md`
- daemon mode -> `ops-modes.md`
- c1z file -> `ref-faq.md`

**Code with errors**
- Error message -> `debug-errors.md`
- Interface issue -> `build-syncer.md`, `ref-sdk.md`
- Pagination issue -> `build-pagination.md`, `patterns.md`
- Auth failure -> `recipes-auth.md`, `debug-errors.md`
- Cache problems -> `recipes-caching.md`
- Grant/Revoke -> `patterns.md`
- HTTP responses -> `patterns.md`

**Configuration**
- CLI flags -> `ref-config.md`
- Environment variables -> `ref-config.md`
- Config files -> `ref-config.md`

**Architecture**
- SDK interfaces -> `ref-sdk.md`
- C1 communication -> `ref-c1api.md`

---

## Usage Examples

User: "How do I implement pagination?"
Retrieve: `build-pagination.md`

User: "Pagination loop error"
Retrieve: `debug-errors.md`, `build-pagination.md`

User: "Connect REST API without Go"
Retrieve: `meta-http.md`, `meta-cel.md`

User: "OAuth2 authentication"
Retrieve: `recipes-auth.md`

User: "Cache users between List and Grants"
Retrieve: `recipes-caching.md`

User: "What SDK interfaces do I implement?"
Retrieve: `ref-sdk.md`

User: "How does daemon mode work?"
Retrieve: `ops-modes.md`, `ref-c1api.md`
