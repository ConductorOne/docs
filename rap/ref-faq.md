# ref-faq

Common questions about baton connectors.

---

## SDK tools

**Q: What is baton-sdk vs cone vs conductorone-sdk-go?**

| Tool | Purpose | User |
|------|---------|------|
| baton-sdk | Go SDK for building connectors | Connector developers |
| cone | CLI for C1 platform ops | End users (requests, approvals) |
| conductorone-sdk-go | Go SDK for C1 API | App integrators |

Building a connector? Use baton-sdk.

---

## Capabilities

**Q: Do all connectors support provisioning?**

No. Many are sync-only. Check specific connector's capability manifest.

**Q: Where is the authoritative source for capabilities?**

| Source | Purpose |
|--------|---------|
| Docs capabilities index | Human discovery |
| Connector binary + manifests | Runtime contract |

---

## Run modes

**Q: What are the run modes?**

| Mode | Trigger | Behavior |
|------|---------|----------|
| One-shot | No `--client-id` | Runs once, produces c1z, exits |
| Daemon | `--client-id` provided | Continuous task processing |

**Q: What is "service mode"?**

Overloaded term:
1. Daemon mode (SDK feature)
2. OS service (deployment concern)
3. Marketing ("runs continuously")

**Q: How to determine mode?**

```
--client-id provided?
  No  --> One-shot
  Yes --> Daemon
```

---

## Data

**Q: What is a .c1z file?**

SQLite + gzip containing access graph data from sync. Inspect with `baton` CLI.

**Q: What happens during sync?**

| Stage | Method | Purpose |
|-------|--------|---------|
| 1 | ResourceType() | Learn what types exist |
| 2 | List() | Fetch all instances |
| 3 | Entitlements() | What permissions each offers |
| 4 | Grants() | Who has each permission |

SDK processes ALL types per stage, not type-by-type.

---

## Authentication

**Q: Which auth method to use?**

Whatever target system requires:

| Method | Use Case |
|--------|----------|
| API Key | Token-based APIs |
| Bearer Token | OAuth2 APIs |
| OAuth2 Client Credentials | Service-to-service |
| JWT Service Account | Google-style |
| LDAP Bind | Directory services |

---

## Pagination

**Q: How to handle pagination?**

| Helper | Use Case |
|--------|----------|
| pagination.Token | Linear pagination |
| pagination.Bag | Nested (children within parents) |

**Q: bag.Current() returns nil?**

Expected on first call. Nil-check before accessing fields.

---

## Caching

**Q: Can I use sync.Map?**

Yes. Recommended for thread-safe caching. Cache users in List(), use in Grants().

**Q: Package-level sync.Map?**

ANTI-PATTERN. Use struct fields. Package-level persists across syncs in daemon mode.

---

## Meta-connectors

**Q: What are baton-http and baton-sql?**

Configuration-driven connectors using YAML + CEL instead of Go code.

| Connector | Target |
|-----------|--------|
| baton-http | Any REST API |
| baton-sql | Any SQL database |

**Q: When to use?**

Standard patterns, don't want to write Go. Won't handle all edge cases.

---

## Troubleshooting

**Q: Pagination loop detected?**

Returning same token causes infinite loop. Check:
- Returning empty string when done
- Not modifying cursor
- API actually returning different cursors

**Q: Empty sync results?**

Check:
- Credentials valid
- Permissions sufficient
- Filters not too restrictive
- API returning data
