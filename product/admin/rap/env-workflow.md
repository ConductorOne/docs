# Workflow Execution Expressions

Dynamic data access within ConductorOne workflow automations. Supports template interpolation and step-to-step data flow.

## When to Use

Use Workflow CEL for:
- Accessing trigger data in workflow steps
- Passing data between workflow steps
- Building dynamic messages and payloads
- Conditional workflow logic

## The `ctx` Object

All workflow expressions use the `ctx` object:

| Path | Description |
|------|-------------|
| `ctx.trigger` | Data from the event that started the workflow |
| `ctx.<step_name>` | Output from a completed step |

## Template Syntax

Use double curly braces for interpolation:

```
Hello {{ ctx.trigger.user.display_name }}!
```

## Common Patterns

### Access Trigger Data

```cel
// User information
ctx.trigger.user.display_name
ctx.trigger.user.email
ctx.trigger.user_id

// Custom trigger fields
ctx.trigger.custom_field
```

### Access Previous Step Output

```cel
// Single value
ctx.lookup_step.user_id

// Array
ctx.approval_step.user_ids

// Nested
ctx.manager_lookup.user.manager.email
```

### Build JSON Output

```json
{
  "name": "{{ ctx.trigger.user.display_name }}",
  "email": "{{ ctx.step_one.email }}"
}
```

This becomes a struct accessible by later steps.

### Conditional Values

```cel
{{ ctx.trigger.status == "approved" ? "Approved!" : "Denied" }}
```

### Directory Functions

```cel
// Look up user
c1.directory.users.v1.GetByID(ctx.trigger.user_id)

// Get managers
c1.directory.users.v1.GetManagers(ctx.trigger.user)

// Find by email
c1.directory.users.v1.FindByEmail(ctx.step_one.email)
```

## What Can Go Wrong

| Scenario | What Happens | How to Handle |
|----------|--------------|---------------|
| Reference undefined step | Compile error | Check step order and names |
| Access missing field | Runtime error | Use `has()` check or ensure upstream produces field |
| Template syntax error | Error in output | Check matching braces |
| Output too large (>1KB) | Truncated | Keep outputs small |

## Safe Field Access

```cel
// Unsafe - fails if optional_field is missing
ctx.trigger.optional_field.value

// Safe - provide default
has(ctx.trigger.optional_field) ? ctx.trigger.optional_field.value : "default"
```

## Time Functions

```cel
// Current time
now()

// Parse date
time.parse(ctx.trigger.date_field, "date")

// End of quarter
time.end_of(now(), "quarter")
```

## Best Practice

- Use descriptive step names (`lookup_manager`, not `step1`)
- Keep step outputs small and focused
- Test expressions before deploying
- Always handle optional fields with `has()`
