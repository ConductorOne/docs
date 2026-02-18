# User Functions

Functions in the `c1.user.*` namespace for checking user attributes and entitlements.

## HasEntitlement

Check if a user has a specific entitlement.

```cel
c1.user.v1.HasEntitlement(user: User, appId: string, entitlementSlug: string) -> bool
```

**Example:**
```cel
// Include users with admin access in a dynamic group
c1.user.v1.HasEntitlement(subject, "okta-app-id", "admin-role")

// Policy condition: on-call users get fast-track
c1.user.v1.HasEntitlement(subject, "pagerduty", "on-call")
```

---

## HasApp

Check if a user has any access to an application.

```cel
c1.user.v1.HasApp(user: User, appId: string) -> bool
```

**Example:**
```cel
// Users with any access to critical app
c1.user.v1.HasApp(subject, "critical-app-id")
```

---

## GetAppUserManagers

Get app-specific managers for a user (different from directory managers).

```cel
c1.user.v1.GetAppUserManagers(user: User, appId: string) -> list<User>
```

**Example:**
```cel
// Use app-specific managers if available
size(c1.user.v1.GetAppUserManagers(subject, entitlement.app_id)) > 0
  ? c1.user.v1.GetAppUserManagers(subject, entitlement.app_id)
  : c1.directory.users.v1.GetManagers(subject)
```

---

## Performance Note

Function calls are more expensive than simple field comparisons. In dynamic groups (evaluated against every user), prefer:

```cel
// Faster: field comparison
subject.department == "Engineering"

// Slower: function call
c1.user.v1.HasEntitlement(subject, "app", "role")
```

Use function calls when necessary, but be aware of the performance impact in high-volume contexts.
