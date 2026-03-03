# CEL Error Reference

## Error Types

| Type | When Caught | Examples |
|------|-------------|----------|
| **Compile-time** | When you save | Syntax errors, type mismatches, undefined variables |
| **Runtime** | When expression evaluates | Empty lists, missing users, function failures |

Compile-time errors prevent saving. Runtime errors cause unexpected behavior.

---

## Compile-Time Errors

### Syntax Error

**Error:** `Syntax error: mismatched input`

```cel
// BAD: single quotes not valid
subject.department == 'Engineering'

// GOOD: use double quotes
subject.department == "Engineering"
```

### Undefined Variable

**Error:** `undeclared reference to 'xyz'`

```cel
// BAD: typo
subjct.department == "Engineering"

// BAD: wrong environment
ctx.trigger.user_id  // ctx only in workflows

// GOOD
subject.department == "Engineering"
```

### Type Mismatch

**Error:** `found no matching overload`

```cel
// BAD: comparing string to number
subject.profile["level"] > 5  // profile values are strings

// GOOD: convert types
int(subject.profile["level"]) > 5
```

### Wrong Return Type

**Error:** `expected type 'bool' but found 'string'`

Policy conditions must return `bool`. Approver expressions must return `User` or `list<User>`.

---

## Runtime Errors

### Empty Approver List

**Symptom:** Policy step is skipped unexpectedly.

**Cause:** Approver expression returned `[]`.

```cel
// Problem: user has no manager
c1.directory.users.v1.GetManagers(subject)  // returns []

// Solution: add fallback
size(c1.directory.users.v1.GetManagers(subject)) > 0
  ? c1.directory.users.v1.GetManagers(subject)
  : appOwners
```

### User Not Found

**Symptom:** `FindByEmail` or `GetByID` fails.

**Cause:** User doesn't exist or left company.

```cel
// Risky: hardcoded email
[c1.directory.users.v1.FindByEmail("john@company.com")]

// Better: use entitlement-based groups
c1.directory.apps.v1.GetEntitlementMembers("app", "approvers")
```

### Profile Key Missing

**Symptom:** Expression fails for some users.

**Cause:** Profile key doesn't exist.

```cel
// BAD: fails if costCenter missing
subject.profile["costCenter"] == "CC-123"

// GOOD: check first
has(subject.profile.costCenter) && subject.profile["costCenter"] == "CC-123"
```

### Empty vs Missing

**Symptom:** `has()` returns `true` but value is empty.

**Cause:** `has()` checks existence, not emptiness.

```cel
// has() returns true for empty strings
has(subject.department)  // true even if department == ""

// Check for non-empty
has(subject.department) && subject.department != ""

// Or use ifEmpty for defaults
subject.department.ifEmpty("Unknown")
```

---

## Debugging Strategies

### 1. Check Return Type

Conditions must return `bool`. Approvers must return `User` or `list<User>`.

### 2. Test with Real Users

Use the CEL validation service to see what an expression returns for actual users.

### 3. Simplify

Break complex expressions into smaller parts. Test each part.

### 4. Check for Empty Lists

Approver expressions that return `[]` skip the step. Always add fallbacks.

### 5. Preview Before Saving

For dynamic groups, preview who would be included before saving.
