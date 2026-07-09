# Entitlement Configuration Rule Expressions

Entitlement configuration rules are app-scoped rules that resolve the **request settings** (request policy, emergency grant behavior, maximum grant duration) for an entitlement. Each rule's condition evaluates to `bool`. Rules are evaluated by priority (then id), and the first rule whose condition returns `true` provides the effective settings. An empty condition is a catch-all that matches every entitlement no higher-priority rule has claimed.

The condition is authored as a CEL expression.

## Available Variables

Every evaluation receives a single top-level variable: **`entitlement`**.

| Variable | Type | Description |
|----------|------|-------------|
| `entitlement` | `AppEntitlement` | The entitlement being routed. For sparse (role-scope) targets, `entitlement.role` and `entitlement.scope` are populated. |

There is **no** `subject`, `task`, `user`, or `app` variable here—configuration rules see only the entitlement and its binding context, and are already scoped per-app.

### `entitlement` fields

| Field | Type | Description |
|-------|------|-------------|
| `entitlement.id` | string | Entitlement identifier. Empty for sparse targets unless persisted. |
| `entitlement.app_id` | string | App that owns the entitlement. |
| `entitlement.app_resource_type_id` | string | Resource type the entitlement is on (for sparse: the role's resource type). |
| `entitlement.app_resource_id` | string | Resource the entitlement is on (for sparse: the role's resource). |
| `entitlement.display_name` | string | Display name. For sparse targets, mirrors the role's display name. |
| `entitlement.description` | string | Description. For sparse targets, mirrors the role's description. |
| `entitlement.risk_level_value_id` | string | Risk-level value id, if set. |

camelCase aliases also work (`appId`, `appResourceTypeId`, `appResourceId`, `displayName`).

### `entitlement.role` and `entitlement.scope` (sparse targets only)

For **classic** targets these nested resources are empty—every string field is `""`. For **sparse** (role-scope binding) targets they are filled from the binding.

| Field | Type | Description |
|-------|------|-------------|
| `entitlement.role.id` | string | Role resource identifier. |
| `entitlement.role.app_resource_type_id` | string | Resource type of the role. |
| `entitlement.role.display_name` | string | Role display name. |
| `entitlement.scope.id` | string | Scope resource identifier. |
| `entitlement.scope.app_resource_type_id` | string | Resource type of the scope. |
| `entitlement.scope.display_name` | string | Scope display name. |

## Common Patterns

### Classic targets

```cel
// Match every entitlement on a specific resource type
entitlement.app_resource_type_id == "group"

// Match by display-name pattern
entitlement.display_name.startsWith("prod-")

// Match a specific entitlement
entitlement.display_name == "Admin"
```

### Sparse (role-scope binding) targets

These rules only fire for sparse targets—the empty-string sentinel on classic targets makes the comparison fail.

```cel
// Any sparse target that grants an admin role
entitlement.role.display_name.contains("Admin")

// Sparse target on a specific scope resource type
entitlement.scope.app_resource_type_id == "production_database"

// Admin-role grant on a production-prefixed scope
entitlement.role.display_name.contains("Admin")
  && entitlement.scope.display_name.startsWith("prod-")

// Pin by stable IDs (survives an upstream rename)
entitlement.role.id == "ROLE_ID" && entitlement.scope.id == "SCOPE_ID"
```

### Sparse-only / classic-only gating

```cel
// Sparse-only: scope.id is "" for classic targets
entitlement.scope.id != ""

// Classic-only: role.id is "" for classic targets
entitlement.role.id == ""
```

## What Can Go Wrong

| Scenario | What Happens | How to Handle |
|----------|--------------|---------------|
| `entitlement.role.*` referenced on a classic app | Comparison returns `false` (fields are `""`) | Expected—this is what fences a rule to sparse targets |
| Two rules can match the same entitlement | First by (priority, id) wins | Order specific rules above general ones |
| No rule matches | Entitlement falls through to the app default | Add a catch-all rule with an empty condition |
| Typo in a field name | Compile-time error | Expression won't save |

## Best Practice

Keep each condition simple and use ordering rather than complex boolean logic. Use the rule editor's preview panel to confirm which entitlements a draft condition matches before saving.
