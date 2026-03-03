# Account Provisioning Expressions

Generate dynamic values for account provisioning. Used to compute account attributes during grant operations.

## When to Use

Use Account Provisioning CEL for:
- Computing account username or email from user attributes
- Deriving account properties from entitlement or task context
- Building provisioning payloads with dynamic values

## Available Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `subject` | `User` | Yes | The user being provisioned |
| `entitlement` | `AppEntitlement` | Optional | The entitlement being granted |
| `task` | `Task` | Optional | The provisioning task context |

## Common Patterns

### Derive Account Properties from User

```cel
// Email as username
subject.email

// Build username from name
subject.display_name.lowerAscii().replace(" ", ".")

// Department-prefixed username
subject.department.lowerAscii() + "_" + subject.username
```

### Use Profile Attributes

```cel
// Employee ID from profile
subject.profile['employee_id']

// Cost center
subject.profile['cost_center']

// Location
subject.profile['office_location']
```

### Use Attribute Mappings

The `subject.attributes` field contains pre-fetched attribute mappings:

```cel
// Access mapped attribute by display name
subject.attributes['Job Code']

// Use mapped attribute with fallback
has(subject.attributes['Team']) ? subject.attributes['Team'] : "Default"
```

### Conditional Values

```cel
// Different value based on user type
subject.employment_type == "contractor" ? "ext_" + subject.username : subject.username

// Based on entitlement (if available)
has(entitlement) && entitlement.app_resource_type == "Admin"
  ? "admin_" + subject.username
  : subject.username
```

### From Entitlement Context

```cel
// Use entitlement properties
entitlement.app_resource_type

// App-specific behavior
entitlement.app_id
```

### From Task Context

```cel
// Grant duration awareness
task.is_grant_permanent ? "permanent" : "temporary"

// Request origin
task.origin == TASK_ORIGIN_CERTIFY ? "recertified" : "new"
```

## Directory Functions

Full directory library is available:

```cel
// Get managers
c1.directory.users.v1.GetManagers(subject)

// Check existing access
c1.user.v1.HasEntitlement(subject, "app-id", "entitlement-id")

// Get app accounts
c1.user.v1.GetAppUsersForUser(subject, "app-id")
```

## What Can Go Wrong

| Scenario | What Happens | How to Handle |
|----------|--------------|---------------|
| Profile attribute missing | Empty string or error | Use `has()` check |
| Attribute mapping not found | Empty value | Check mapping exists in C1 config |
| `entitlement` not available | Compile error if referenced | Check context provides entitlement |
| `task` not available | Compile error if referenced | Check context provides task |

## Best Practice

Keep expressions simple. The result becomes an account attribute, so ensure it's a clean string value appropriate for the target system.
