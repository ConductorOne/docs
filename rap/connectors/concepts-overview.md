# concepts-overview

What connectors do, sync vs provision, the reconciliation loop.

---

## What Problem Connectors Solve

A **connector** answers: *who has access to what?*

ConductorOne needs visibility into users, groups, roles, and permissions across all systems. Every system stores this differently - Okta has users and groups, AWS has IAM roles and policies, Salesforce has profiles and permission sets.

A connector translates access data from any system into a common format. Once connected, you get unified visibility across your infrastructure.

## What a Connector Does

In Baton terms, a connector is a program that can:
- **List resources** (users, groups, roles, apps, projects)
- **Define entitlements** (permissions that can be granted)
- **Emit grants** (who currently has which entitlements)

## Sync vs Provision

**Sync** (read): Pull access data into ConductorOne
- Who exists? What groups? What roles?
- What permissions are available?
- Who has what access right now?

**Provision** (write): Push access changes back
- **Grant**: Give someone approved access
- **Revoke**: Remove terminated access
- **Create Account**: JIT provisioning
- **Delete Resource**: Remove accounts entirely

## The Reconciliation Loop

Together, sync and provision create a reconciliation loop:

1. ConductorOne sees what access exists (sync)
2. Compares to what access *should* exist (policy)
3. Corrects any drift (provision)

Access controls become self-healing.

## Identity Providers

IdPs (Okta, Azure AD, Google Workspace) have a unique role - they're the **source of truth** for user identities.

IdP connectors:
- Define canonical user identities
- Enable correlation of users across other systems
- Originate user lifecycle (join, move, leave)

Connecting an IdP establishes the identity foundation other connectors build upon.

## The Connector Binary

When you build a connector, you produce a standalone binary (e.g., `baton-okta`):

- Embeds the SDK at compile time
- Self-contained, no runtime dependencies
- Produces a `.c1z` file as output

```bash
./baton-okta --domain example.okta.com --api-token $TOKEN
ls sync.c1z  # Output file
```

## When to Build vs Reuse

- **Use existing connector** when it meets your needs
- **Contribute upstream** when missing a capability you need
- **Build new** when target system is unsupported
- **Use meta-connectors** (baton-http, baton-sql) for quick REST/SQL integration
