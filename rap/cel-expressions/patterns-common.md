# Common CEL Patterns

Patterns that work across all CEL environments.

## Safe Field Access

### Using has()

```cel
// Check before accessing
has(subject.department) && subject.department == "Engineering"

// For profile fields (always use has)
has(subject.profile.costCenter) && subject.profile["costCenter"] == "CC-123"
```

### Using "in" for Maps

```cel
// Check if key exists in profile
"costCenter" in subject.profile && subject.profile["costCenter"] == "CC-123"

// Required for keys with spaces
"Cost Center" in subject.profile && subject.profile["Cost Center"] == "R&D"
```

### Default Values

```cel
// Using ternary
has(subject.department) ? subject.department : "Unknown"

// Using ifEmpty (for empty strings, not missing fields)
subject.department.ifEmpty("Unknown")
```

---

## List Operations

### Membership Check

```cel
subject.department in ["Engineering", "Product", "Design"]
```

### Size Check

```cel
size(appOwners) > 0
```

### Exists (any match)

```cel
appOwners.exists(owner, owner.department == "Security")
```

### Safe Index Access

```cel
// BAD: crashes on empty list
appOwners[0]

// GOOD: check first
size(appOwners) > 0 ? [appOwners[0]] : []
```

---

## Ternary Conditional

```cel
condition ? value_if_true : value_if_false
```

**Example:**
```cel
// Approver fallback
size(managers) > 0 ? managers : appOwners

// Status mapping
item.active == true ? "enabled" : "disabled"
```

---

## Boolean Logic

### AND (both must be true)

```cel
subject.department == "Engineering" && subject.employment_type == "employee"
```

### OR (either can be true)

```cel
subject.department == "Engineering" || subject.department == "Product"
```

### NOT

```cel
!(subject.department in ["Contractors", "Vendors"])
```

### Best Practice

Keep conditions simple. Prefer multiple policy rules over complex compound expressions:

```cel
// Hard to debug
(a && b) || (c && !d) || (e && f)

// Better: use separate policy rules
```

---

## Enum Comparisons

Both formats work:

```cel
// SCREAMING_SNAKE format
subject.status == USER_STATUS_ENABLED
task.origin == TASK_ORIGIN_REQUEST

// Namespaced format
subject.status == UserStatus.ENABLED
task.origin == TaskOrigin.WEBAPP
```

---

## Anti-Patterns

### Deep Nesting

```cel
// BAD: hard to debug
c1.directory.users.v1.GetManagers(
  c1.directory.users.v1.GetManagers(
    c1.directory.users.v1.GetManagers(subject)[0]
  )[0]
)

// BETTER: use multiple policy steps
```

### Hardcoded Users

```cel
// BAD: user might leave
[c1.directory.users.v1.FindByEmail("john@company.com")]

// BETTER: use entitlement-based groups
c1.directory.apps.v1.GetEntitlementMembers("app", "approvers")
```

### Complex Boolean Logic

```cel
// BAD: impossible to debug
(a && b) || (c && !d) || (e && f && !g)

// BETTER: multiple policy rules with simple conditions
```
