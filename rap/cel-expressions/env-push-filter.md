# Push Config Filter Environment

Filter which users are targeted by push rules. Evaluates to `bool`.

## When to Use

Use Push Config Filter CEL for:
- Targeting entitlement grants to specific user groups
- Filtering who receives automatically provisioned access
- Defining user criteria for push-based provisioning

## Available Variables

| Variable | Type | Description |
|----------|------|-------------|
| `subject` | `User` | The user being evaluated for push rule targeting |

## Common Patterns

### Department-Based Targeting

```cel
// Push to Engineering
subject.department == "Engineering"

// Push to multiple departments
subject.department in ["Engineering", "Product"]
```

### Status-Based

```cel
// Only enabled users
subject.status == UserStatus.ENABLED

// Exclude disabled users
subject.status != UserStatus.DISABLED
```

### Profile Attributes

```cel
// Users in specific location
subject.profile['location'] == 'San Francisco'

// Users with specific cost center
subject.profile['department'] == 'Engineering'

// Multiple profile conditions
subject.profile['department'] == 'Engineering' &&
  subject.profile['location'] == 'San Francisco'
```

### Email Domain

```cel
// Only company domain
subject.email.endsWith('@company.com')

// Starts with specific prefix
subject.email.startsWith('admin')
```

### String Operations

```cel
// Display name contains
subject.display_name.contains('John')

// Case-insensitive check
subject.email.lowerAscii().endsWith('@company.com')

// Length check
subject.username.size() > 5
```

### Compound Conditions

```cel
// Engineering + enabled + company email
subject.department == 'Engineering' &&
  subject.status == UserStatus.ENABLED &&
  subject.email.endsWith('@company.com')

// Either condition (or)
subject.department == 'IT' || subject.department == 'Security'
```

## What Can Go Wrong

| Scenario | What Happens | How to Handle |
|----------|--------------|---------------|
| Profile key doesn't exist | Runtime error or empty value | Use `has()` or `in` check |
| Expression always true | Everyone gets pushed | Probably not intended |
| Expression always false | No one gets pushed | Check logic |
| Typo in field name | Compile-time error | Expression won't save |
| Case mismatch | No match | Use `lowerAscii()` |

## Functions Available

Directory and user functions are available:

```cel
// Users with specific entitlement
c1.user.v1.HasEntitlement(subject, "app-id", "entitlement-id")

// Users with any access to app
c1.user.v1.HasApp(subject, "app-id")
```

## Best Practice

Push filters run against your entire user directory. Keep expressions simple and fast - prefer field comparisons over function calls.
