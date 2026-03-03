# Triggers Environment

Event-driven expressions that fire when users or accounts change. Evaluate to `bool`.

## When to Use

Use Triggers CEL for:
- Detecting attribute changes (email, status, department)
- Firing automations when users are modified
- Comparing old vs new state during sync

## Available Variables

Variables are nested under `ctx.trigger` with both snake_case and camelCase forms.

### For User Changes

| Variable | Type | Description |
|----------|------|-------------|
| `ctx.trigger.oldUser` / `ctx.trigger.old_user` | `User` | User state before change |
| `ctx.trigger.newUser` / `ctx.trigger.new_user` | `User` | User state after change |

### For Account Changes

| Variable | Type | Description |
|----------|------|-------------|
| `ctx.trigger.oldAccount` / `ctx.trigger.old_account` | `AppUser` | Account state before change |
| `ctx.trigger.newAccount` / `ctx.trigger.new_account` | `AppUser` | Account state after change |

## Available Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `now()` | `timestamp` | Current time for date comparisons |

## Common Patterns

### Detect Field Change

```cel
// Email changed
ctx.trigger.oldUser.email != ctx.trigger.newUser.email

// Status changed to disabled
ctx.trigger.oldUser.status == UserStatus.ENABLED &&
  ctx.trigger.newUser.status == UserStatus.DISABLED

// Account status change
ctx.trigger.oldAccount.status.status == Status.ENABLED &&
  ctx.trigger.newAccount.status.status == Status.DISABLED
```

### Date-Based Triggers

```cel
// Hire date is today (fire onboarding)
timestamp(ctx.trigger.newUser.profile.hire_date).getDayOfYear() ==
  timestamp(now()).getDayOfYear() &&
timestamp(ctx.trigger.newUser.profile.hire_date).getFullYear() ==
  timestamp(now()).getFullYear()
```

### Multiple Fields

```cel
// Both email and department changed
ctx.trigger.oldUser.email != ctx.trigger.newUser.email &&
  ctx.trigger.oldUser.department != ctx.trigger.newUser.department
```

## What Can Go Wrong

| Scenario | What Happens | How to Handle |
|----------|--------------|---------------|
| Typo in field name | Compile-time error | Expression won't save |
| Using User fields on AppUser | Wrong variable type | Check if trigger is for users or accounts |
| Profile field doesn't exist | Runtime error accessing it | Use `has()` check first |
| Comparing nested nil objects | Panic or unexpected result | Check parent exists: `has(ctx.trigger.newUser.status)` |

## Best Practice

Keep trigger conditions focused on a single change type. Use separate triggers for different events rather than one complex trigger that handles everything.
