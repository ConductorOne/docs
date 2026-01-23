# CEL Expression Knowledge Base

This directory contains focused documentation chunks for CEL (Common Expression Language) in ConductorOne. Each file is self-contained and designed for selective retrieval.

## How to Use This Index

When answering questions about CEL expressions in ConductorOne:

1. Identify the question type from the tables below
2. Retrieve 1-3 relevant files from this directory
3. Use the retrieved content to answer accurately
4. If the answer is incomplete, retrieve additional files

## Available Knowledge Files

### CEL Environments

These files document where CEL expressions are used and what variables/functions are available in each context.

| File | Use When User Asks About |
|------|--------------------------|
| `env-policy-conditions.md` | Policy condition expressions, routing requests, access control rules |
| `env-dynamic-groups.md` | Dynamic group membership, group expressions, user filtering |
| `env-policy-approvers.md` | Approver selection, manager routing, approval workflows |
| `env-triggers.md` | Automation triggers, detecting user/account changes, event-driven expressions |
| `env-access-reviews.md` | Access review scope, filtering users/accounts for certification |
| `env-push-filter.md` | Push rule targeting, user provisioning filters |
| `env-workflow.md` | Workflow templates, step data flow, ctx object, interpolation |
| `env-account-provisioning.md` | Account attribute mapping, provisioning expressions |
| `env-user-attribute.md` | Derived user attributes, computed attribute values |

### Functions

These files document specific function categories available in CEL expressions.

| File | Use When User Asks About |
|------|--------------------------|
| `functions-directory.md` | GetManagers, FindByEmail, GetByID, DirectReports, GetEntitlementMembers |
| `functions-user.md` | HasEntitlement, HasApp, checking user access |
| `functions-time.md` | Date/time operations, time.parse, time.format, now(), durations |
| `functions-ip.md` | IP addresses, CIDR ranges, network-based access control |
| `functions-strings.md` | String operations, ifEmpty, contains, endsWith, lowerAscii |

### Types and References

| File | Use When User Asks About |
|------|--------------------------|
| `types.md` | Type definitions, enums, User vs AppUser, primitives, collections, built-in variables |

### Patterns and Debugging

| File | Use When User Asks About |
|------|--------------------------|
| `patterns-common.md` | Safe field access, null handling, list operations, ternary expressions |
| `debug-errors.md` | CEL errors, troubleshooting, compile-time vs runtime issues |
| `overview-intro.md` | What is CEL, basic concepts, getting started |

### Integrations

| File | Use When User Asks About |
|------|--------------------------|
| `terraform-examples.md` | CEL in Terraform, conductorone_policy resources, IaC patterns |
| `connectors-bcel.md` | CEL in baton-http, baton-sql, connector data transformation |

## Quick Retrieval Guide

**User wants to write an expression:**
- "Route to manager" -> `env-policy-approvers.md`, `functions-directory.md`
- "Create a group for contractors" -> `env-dynamic-groups.md`, `patterns-common.md`
- "Trigger when user disabled" -> `env-triggers.md`
- "Check if user has access" -> `functions-user.md`

**User asks about types:**
- "What's the difference between User and AppUser?" -> `types.md`
- "What fields does subject have?" -> `types.md`
- "What are the UserStatus values?" -> `types.md`
- "How do I use duration?" -> `types.md`, `functions-time.md`
- "What enums are available?" -> `types.md`
- "What's in appOwners?" -> `types.md`

**User has an error:**
- Any CEL error -> `debug-errors.md` first, then relevant env file
- Type mismatch error -> `types.md`, `debug-errors.md`

**User asks what's available:**
- "What variables can I use?" -> `types.md` (built-in variables), then relevant `env-*.md`
- "What functions exist?" -> `functions-directory.md`, `functions-user.md`, `functions-time.md`

## File Characteristics

- Each file is under 300 lines
- Each file is self-contained (understandable without other files)
- Each file includes concrete examples with inline comments
- Examples show both correct usage and common pitfalls
