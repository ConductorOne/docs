# CEL Type Definitions

This document covers all types used in ConductorOne CEL expressions: primitives, time types, collections, enums, and object types.

## Primitive Types

| Type | Description | Example values |
|:-----|:------------|:---------------|
| `string` | Text value | `"Engineering"`, `"user@company.com"` |
| `bool` | Boolean true/false | `true`, `false` |
| `int` | Integer number | `0`, `42`, `-1` |
| `double` | Floating-point number | `3.14`, `0.5` |

## Time Types

| Type | Description | How to create |
|:-----|:------------|:--------------|
| `timestamp` | A point in time (UTC) | `now()`, `timestamp("2025-01-01T00:00:00Z")`, `time.parse(...)` |
| `duration` | A length of time | `duration("24h")`, `duration("30m")`, `duration("720h")` |

**Duration format:** Use `h` for hours, `m` for minutes, `s` for seconds.
- `"2h"` = 2 hours
- `"30m"` = 30 minutes
- `"720h"` = 30 days

**Timestamp arithmetic:**
```go
now() + duration("24h")              // 24 hours from now
now() - duration("720h")             // 30 days ago
timestamp1 - timestamp2              // Returns a duration
```

## Collection Types

| Type | Description | Example |
|:-----|:------------|:--------|
| `list<T>` | Ordered list of items | `[user1, user2]`, `["a", "b", "c"]` |
| `map<K,V>` | Key-value mapping | `subject.profile` (map of string to any) |

**List operations:**
```go
size(myList)                         // Number of items
myList[0]                            // First item (0-indexed)
"value" in myList                    // Check membership
myList + otherList                   // Concatenate lists
myList.filter(x, x.status == UserStatus.ENABLED)  // Filter
myList.map(x, x.email)               // Transform to list of emails
myList.exists(x, x.department == "IT")  // Any match?
myList.all(x, x.status == UserStatus.ENABLED)     // All match?
```

## Enum Types

Always use the full enum name (e.g., `UserStatus.ENABLED`, not just `ENABLED`).

### UserStatus

| Value | Meaning |
|:------|:--------|
| `UserStatus.ENABLED` | User is active |
| `UserStatus.DISABLED` | User is disabled |
| `UserStatus.DELETED` | User is deleted |

### UserType

| Value | Meaning |
|:------|:--------|
| `UserType.HUMAN` | Regular human user |
| `UserType.AGENT` | Automated agent |
| `UserType.SERVICE` | Service account |
| `UserType.SYSTEM` | System account |

### TaskOrigin

| Value | Meaning |
|:------|:--------|
| `TaskOrigin.WEBAPP` | Created in ConductorOne web interface |
| `TaskOrigin.SLACK` | Created via Slack integration |
| `TaskOrigin.API` | Created via API |
| `TaskOrigin.JIRA` | Created via Jira integration |
| `TaskOrigin.COPILOT` | Created via Copilot |
| `TaskOrigin.PROFILE_MEMBERSHIP_AUTOMATION` | Created by automation |
| `TaskOrigin.TIME_REVOKE` | Created by time-based revocation |

### AppUserStatus (for triggers)

Used in `ctx.trigger.oldAccount.status.status` and `ctx.trigger.newAccount.status.status`:

| Value | Meaning |
|:------|:--------|
| `APP_USER_STATUS_ENABLED` | Account is active |
| `APP_USER_STATUS_DISABLED` | Account is disabled |
| `APP_USER_STATUS_DELETED` | Account is deleted |

### TimeFormat

| Constant | Format | Example output |
|:---------|:-------|:---------------|
| `TimeFormat.RFC3339` | ISO 8601 / RFC 3339 | `2025-10-22T14:30:00Z` |
| `TimeFormat.DATE` | Date only | `2025-10-22` |
| `TimeFormat.DATETIME` | Date and time | `2025-10-22 14:30:00` |
| `TimeFormat.TIME` | Time only | `14:30:00` |

## Object Types

### User vs AppUser

These are different types:
- **User** = A person in the ConductorOne directory (synced from identity provider)
- **AppUser** = That person's account in a specific app (GitHub account, Okta account, etc.)

One User can have many AppUsers across different connected applications.

### User

A person in the ConductorOne directory.

**Returned by:** `FindByEmail`, `GetByID`, `GetManagers`, `DirectReports`, `GetEntitlementMembers`

**Available as:** `subject`, elements of `appOwners`, `ctx.trigger.oldUser`, `ctx.trigger.newUser`

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | string | Unique user identifier |
| `email` | string | Primary email address |
| `emails` | list&lt;string&gt; | All email addresses |
| `displayName` | string | Display name |
| `username` | string | Username |
| `usernames` | list&lt;string&gt; | All usernames |
| `department` | string | Department |
| `jobTitle` | string | Job title |
| `employmentType` | string | Employment type (e.g., "Full Time") |
| `employmentStatus` | string | Employment status (e.g., "Active") |
| `status` | UserStatus | User status enum |
| `directoryStatus` | UserStatus | Directory sync status |
| `type` | UserType | User type enum |
| `manager` | string | Manager's email |
| `manager_id` | string | Manager's user ID |
| `profile` | map | Custom profile attributes |
| `attributes` | map | Custom user attributes |

### AppUser

A user's account within a specific connected application.

**Returned by:** `ListAppUsersForUser`

**Available as:** `ctx.trigger.oldAccount`, `ctx.trigger.newAccount`

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | string | App user identifier |
| `displayName` | string | Display name |
| `username` | string | Username in the app |
| `usernames` | list&lt;string&gt; | All usernames |
| `email` | string | Email in the app |
| `emails` | list&lt;string&gt; | All emails |
| `employeeIds` | list&lt;string&gt; | Employee IDs |
| `status` | AppUserStatus | Nested status object |
| `status.status` | enum | APP_USER_STATUS_ENABLED/DISABLED/DELETED |
| `status.details` | string | Status details |
| `profile` | map | Custom profile attributes |
| `attributes` | map | Attribute mappings |

### Group

A ConductorOne group (entitlement in the builtin Groups app).

**Returned by:** `FindByName`

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | string | Group identifier |
| `app_id` | string | App ID the group belongs to |
| `display_name` | string | Group display name |

### Task

An access request or task. Available as `task` in policy expressions.

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | string | Unique task identifier |
| `numericId` | string | Numeric task identifier |
| `displayName` | string | Human-readable task name |
| `origin` | TaskOrigin | Where the task was created |
| `isGrantPermanent` | bool | Whether access is permanent |
| `grantDuration` | duration | How long access is granted |
| `subjectUserId` | string | ID of user who is subject of task |
| `requestorUserId` | string | ID of user who created task |
| `analysis` | TaskAnalysis | Task analysis data |

### TaskAnalysis

Analysis data attached to a task. Available as `task.analysis`.

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | string | Analysis identifier |
| `hasConflictViolations` | bool | Whether conflicts exist |
| `conflictViolations` | list&lt;string&gt; | List of conflict IDs |

### Entitlement

The entitlement being requested. Available as `entitlement` in policy expressions.

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | string | Entitlement identifier |
| `appId` | string | Application identifier |

## Built-in Variables

| Variable | Type | Available in | Description |
|:---------|:-----|:-------------|:------------|
| `subject` | User | Policies, Groups, Automations, Campaigns, Account provisioning | The current user being evaluated |
| `task` | Task | Policies only | The current access request |
| `entitlement` | Entitlement | Policies only | The entitlement being requested |
| `appOwners` | list&lt;User&gt; | Policy step approvers only | Owners of the application |
| `ctx` | Context | Automations only | Workflow context and trigger data |
| `ip` | IP | Policies, Automations | Requestor's IP address (when available) |
