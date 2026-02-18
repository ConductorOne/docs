# User Attribute Mapping Expressions

Compute derived attribute values from user data. Returns `string` or `list<string>`.

## When to Use

Use User Attribute Mapping CEL for:
- Deriving attributes from existing user fields
- Transforming profile data into standardized formats
- Computing values for downstream systems

## Available Variables

| Variable | Type | Description |
|----------|------|-------------|
| `subject` | `User` | The user whose attributes are being computed |

## Return Type

Expressions must return either:
- A single `string`
- A `list<string>` (array of strings)

Empty strings and empty lists are valid returns.

## Common Patterns

### Simple Field Access

```cel
// Return email domain
subject.email.split("@")[1]

// Return uppercase department
subject.department.upperAscii()

// Return display name parts
subject.display_name.split(" ")[0]  // First name
```

### Transform Profile Values

```cel
// Normalize job code format
"JC-" + subject.profile['raw_job_code']

// Combine profile fields
subject.profile['city'] + ", " + subject.profile['state']
```

### Conditional Mapping

```cel
// Map employment type to category
subject.employment_type == "contractor" ? "external" : "internal"

// Map department to cost center prefix
subject.department == "Engineering" ? "ENG"
  : subject.department == "Sales" ? "SLS"
  : "OTH"
```

### Return List

```cel
// Return all email domains user might use
[subject.email.split("@")[1], "company.com"]

// Return multiple values based on profile
has(subject.profile['secondary_email'])
  ? [subject.email, subject.profile['secondary_email']]
  : [subject.email]
```

### String Operations

```cel
// Remove whitespace and lowercase
subject.job_title.lowerAscii().trim()

// Replace characters
subject.username.replace(".", "_")

// Check and transform
subject.email.contains("@company.com")
  ? subject.email.replace("@company.com", "@corp.com")
  : subject.email
```

## Directory Functions

Directory functions are available:

```cel
// Get manager's department
size(c1.directory.users.v1.GetManagers(subject)) > 0
  ? c1.directory.users.v1.GetManagers(subject)[0].department
  : "No Manager"

// Check entitlement membership
c1.user.v1.HasEntitlement(subject, "app-id", "admin-role")
  ? "admin"
  : "user"
```

## What Can Go Wrong

| Scenario | What Happens | How to Handle |
|----------|--------------|---------------|
| Profile field missing | Empty string | Use `has()` check |
| Array index out of bounds | Runtime error | Check `size()` first |
| String split with no delimiter | Single-element array | Handle single-element case |
| Wrong return type | Conversion error | Ensure string or list<string> |

## Best Practice

- Return clean, normalized values suitable for downstream systems
- Handle missing data gracefully with defaults
- Keep expressions simple and testable
- Document expected input/output formats
