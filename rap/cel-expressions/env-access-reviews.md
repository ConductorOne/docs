# Access Reviews Environment

Filter which users or accounts are in scope for an access review. Evaluates to `bool`.

## When to Use

Use Access Reviews CEL for:
- Scoping reviews to specific departments or roles
- Filtering users by employment type or status
- Defining which accounts should be reviewed

## Two Scopes

Access reviews can operate at two levels:

### User Scope

Reviews the user identity across all their app accounts.

| Variable | Type | Description |
|----------|------|-------------|
| `subject` | `User` | The user being evaluated for review |

### Account Scope

Reviews a specific app account.

| Variable | Type | Description |
|----------|------|-------------|
| `subject` | `AppUser` | The app account being evaluated for review |

## User Scope Patterns

### Department-Based

```cel
// Review all Engineering users
subject.department == "Engineering"

// Multiple departments
subject.department in ["Engineering", "Product", "Design"]

// Exclude certain departments
!(subject.department in ["Contractors", "Vendors"])
```

### Job Title Patterns

```cel
// Review all managers
subject.job_title.contains("Manager")

// Case-insensitive match
subject.job_title.lowerAscii().contains("manager")
```

### Email Domain

```cel
// Only internal users
subject.email.endsWith("@company.com")

// Exclude contractors
!subject.email.endsWith("@contractor.company.com")
```

### Complex Filters

```cel
// Engineering managers with company email
subject.email.endsWith("@company.com") &&
  subject.department == "Engineering" &&
  subject.job_title.contains("Manager")
```

## Account Scope Patterns

### Status-Based

```cel
// Only review enabled accounts
subject.status.status == Status.ENABLED

// Only review disabled accounts (for cleanup review)
subject.status.status == Status.DISABLED
```

### Account Properties

```cel
// Accounts with specific username pattern
subject.username.startsWith("svc_")

// Accounts by email domain
subject.email.endsWith("@company.com")
```

### Status Details

```cel
// Check status details for specific text
subject.status.details.contains("Active")
```

## What Can Go Wrong

| Scenario | What Happens | How to Handle |
|----------|--------------|---------------|
| Using User fields on AppUser scope | Compile error or missing fields | Know which scope you're in |
| `subject.status` is nil | Status check returns false | May be intended; check `has(subject.status)` first |
| Complex expression always false | No users/accounts in review scope | Preview before saving |
| Complex expression always true | Everyone in scope | Defeats purpose of scoping |
| Case sensitivity | "Engineering" != "engineering" | Use `lowerAscii()` |

## Functions Available

Both scopes support directory and user functions:

```cel
// Check if user has specific entitlement
c1.user.v1.HasEntitlement(subject, "app-id", "entitlement-id")

// Check if user has access to app
c1.user.v1.HasApp(subject, "app-id")
```

## Best Practice

Prefer simple expressions. Access review scopes run against many users/accounts - keep them fast. Use department or email domain filters over function calls when possible.
