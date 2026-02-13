# Directory Functions

Functions in the `c1.directory.*` namespace for looking up users and relationships.

## GetManagers

Get a user's manager(s).

```cel
c1.directory.users.v1.GetManagers(user: User) -> list<User>
```

**Example:**
```cel
// Get subject's managers as approvers
c1.directory.users.v1.GetManagers(subject)

// Safe access with fallback
size(c1.directory.users.v1.GetManagers(subject)) > 0
  ? c1.directory.users.v1.GetManagers(subject)
  : appOwners
```

**Returns:** Empty list `[]` if user has no manager.

---

## FindByEmail

Look up a user by email address.

```cel
c1.directory.users.v1.FindByEmail(email: string) -> User
```

**Example:**
```cel
// Specific approver
[c1.directory.users.v1.FindByEmail("security@company.com")]
```

**Fails** if email doesn't exist. Verify email before deploying.

---

## GetByID

Look up a user by their ID.

```cel
c1.directory.users.v1.GetByID(id: string) -> User
```

**Example:**
```cel
[c1.directory.users.v1.GetByID("user-abc123")]
```

**Fails** if user ID doesn't exist.

---

## FindByName

Look up a user by display name.

```cel
c1.directory.users.v1.FindByName(name: string) -> User
```

**Example:**
```cel
[c1.directory.users.v1.FindByName("Jane Smith")]
```

**Returns** null if no user found with that name.

**Warning:** Display names are not guaranteed to be unique. If multiple users share the same name, results may be unpredictable. Use `FindByEmail` when you need to identify a specific user reliably.

---

## DirectReports

Get users who report to the given user(s).

```cel
c1.directory.users.v1.DirectReports(managers: list<User>) -> list<User>
```

**Example:**
```cel
// Manager can delegate to their direct reports
c1.directory.users.v1.DirectReports(appOwners)
```

---

## GetEntitlementMembers

Get members of a specific entitlement (useful for approval groups).

```cel
c1.directory.apps.v1.GetEntitlementMembers(appId: string, entitlementSlug: string) -> list<User>
```

**Example:**
```cel
// Security team as approvers
c1.directory.apps.v1.GetEntitlementMembers("approvers-app", "security-reviewers")
```

**Returns:** Empty list `[]` if entitlement has no members (step will be skipped).

---

## Common Patterns

### Manager with Fallback

```cel
size(c1.directory.users.v1.GetManagers(subject)) > 0
  ? c1.directory.users.v1.GetManagers(subject)
  : appOwners
```

### Skip-Level Approval

```cel
c1.directory.users.v1.GetManagers(
  c1.directory.users.v1.GetManagers(subject)[0]
)
```

**Warning:** Fails if subject has no manager. Add null checks.

### Entitlement-Based Approvers

Prefer entitlement members over hardcoded emails - handles employee turnover:

```cel
// Better than FindByEmail("john@company.com")
c1.directory.apps.v1.GetEntitlementMembers("approval-app", "security-reviewers")
```
