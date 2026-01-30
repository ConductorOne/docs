# Policy Condition Expressions

Policy conditions determine which policy step applies to a request. They evaluate to `bool`.

## Available Variables

| Variable | Type | Description |
|----------|------|-------------|
| `subject` | `User` | The user requesting access |
| `entitlement` | `AppEntitlement` | The entitlement being requested |
| `task` | `Task` | The access request task/ticket |

## Common Patterns

### Route by User Attribute

```cel
// By department
subject.department == "Engineering"

// By employment type
subject.employment_type == "contractor"

// By job title (contains)
subject.job_title.contains("Manager")
```

### Route by Entitlement

```cel
// By resource type
entitlement.app_resource_type == "Production"

// By specific entitlement ID
entitlement.id == "admin-entitlement-id"

// By app
entitlement.app_id == "production-database-app"
```

### Route by Request Properties

```cel
// Permanent grants need extra approval
task.is_grant_permanent == true

// Long-term grants (over 30 days)
task.grant_duration > duration("720h")

// Request origin
task.origin == TASK_ORIGIN_CERTIFY
task.origin == TASK_ORIGIN_REQUEST
```

### Compound Conditions

```cel
// Contractor + production = escalated
subject.employment_type == "contractor" && entitlement.app_resource_type == "Production"

// Either sensitive app OR permanent grant
entitlement.app_id == "high-security-app" || task.is_grant_permanent
```

## What Can Go Wrong

| Scenario | What Happens | How to Handle |
|----------|--------------|---------------|
| `subject.department` is empty | Comparison returns `false` | May be intentional; use `has()` for explicit check |
| Typo in field name | Compile-time error | Expression won't save |
| Complex boolean logic | Hard to debug | Use multiple policy rules instead |

## Best Practice

Keep conditions simple. Use multiple policy rules with simple conditions rather than one rule with complex compound logic.
