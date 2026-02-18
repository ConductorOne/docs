# Dynamic Group Expressions

Dynamic groups use CEL to determine membership. Expressions evaluate to `bool` - `true` means user is in the group.

## Available Variables

| Variable | Type | Description |
|----------|------|-------------|
| `subject` | `User` | The user being evaluated for group membership |

Only `subject` is available. No `entitlement` or `task`.

## Common Patterns

### Department-Based

```cel
// Single department
subject.department == "Engineering"

// Multiple departments
subject.department in ["Engineering", "Product", "Design"]

// Exclude departments
!(subject.department in ["Contractors", "Vendors"])
```

### Job Title Patterns

```cel
// Simple contains
subject.job_title.contains("Manager")

// Case-insensitive
subject.job_title.lowerAscii().contains("manager")

// Multiple patterns
subject.job_title.contains("Director") || subject.job_title.contains("VP")
```

### Email Domain

```cel
// Internal employees
subject.email.endsWith("@company.com")

// Exclude contractors
!subject.email.endsWith("@contractor.company.com")
```

### Status-Based

```cel
// Only enabled users
subject.status == USER_STATUS_ENABLED

// Human users only (not service accounts)
subject.type == UserType.HUMAN
```

### Profile Attributes

```cel
// Cost center from profile
has(subject.profile.costCenter) && subject.profile["costCenter"] == "CC-123"

// Profile key with spaces (must use bracket notation)
"Cost Center" in subject.profile && subject.profile["Cost Center"] == "R&D"

// Numeric threshold
has(subject.profile.level) && subject.profile.level >= 6
```

### Manager Relationship

```cel
// Direct reports of specific manager
subject.manager_id == "manager-user-id"

// Users who have a manager assigned
has(subject.manager_id)
```

## What Can Go Wrong

| Scenario | What Happens | How to Handle |
|----------|--------------|---------------|
| Empty department | User excluded from group | May be intentional |
| Expression always returns `false` | Group is empty | Preview before saving |
| Expression always returns `true` | Everyone in group | Probably wrong |
| Profile key doesn't exist | Runtime error | Use `has()` or `in` check first |

## Performance Note

Dynamic group expressions are evaluated against every user in your directory. Keep expressions simple (string comparisons) rather than complex (function calls).
