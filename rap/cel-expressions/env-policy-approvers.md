# Policy Approver Expressions

Policy step expressions determine who approves a request. They evaluate to `User` or `list<User>`.

## Available Variables

| Variable | Type | Description |
|----------|------|-------------|
| `subject` | `User` | The user requesting access |
| `appOwners` | `list<User>` | The owners of the application |
| `entitlement` | `AppEntitlement` | The entitlement being requested |
| `task` | `Task` | The access request task/ticket |

## Critical Behavior

**An approver expression that returns an empty list causes the policy step to be skipped entirely.** This is often not the intended behavior.

## Common Patterns

### Manager Approval

```cel
// Subject's manager(s)
c1.directory.users.v1.GetManagers(subject)

// First manager only
[c1.directory.users.v1.GetManagers(subject)[0]]
```

**Safe pattern with fallback:**
```cel
size(c1.directory.users.v1.GetManagers(subject)) > 0
  ? c1.directory.users.v1.GetManagers(subject)
  : appOwners
```

### App Owner Approval

```cel
// All app owners
appOwners

// First app owner
[appOwners[0]]
```

### Specific Person

```cel
// By email
[c1.directory.users.v1.FindByEmail("security@company.com")]

// By user ID
[c1.directory.users.v1.GetByID("user-abc123")]
```

### Entitlement Members

```cel
// Members of an approval group
c1.directory.apps.v1.GetEntitlementMembers("approvers-app", "security-approvers")
```

### Skip-Level Approval

```cel
// Manager's manager
c1.directory.users.v1.GetManagers(
  c1.directory.users.v1.GetManagers(subject)[0]
)
```

### Conditional Approvers

```cel
// App-specific managers if available, otherwise directory managers
size(c1.user.v1.GetAppUserManagers(subject, entitlement.app_id)) > 0
  ? c1.user.v1.GetAppUserManagers(subject, entitlement.app_id)
  : c1.directory.users.v1.GetManagers(subject)
```

## What Can Go Wrong

| Scenario | What Happens | How to Handle |
|----------|--------------|---------------|
| `GetManagers` returns `[]` | Step is skipped | Add fallback approver |
| `appOwners` is empty | Step is skipped | Ensure app has owners |
| `FindByEmail` user doesn't exist | Step fails | Verify email before deploying |
| User leaves company | Step fails | Use entitlement-based approvers |
| Accessing `[0]` on empty list | Index error | Check `size() > 0` first |

## Best Practice

Always have a fallback. Use the ternary pattern:
```cel
size(primaryApprovers) > 0 ? primaryApprovers : fallbackApprovers
```
