# String Functions

Standard CEL string methods plus ConductorOne extensions.

## ifEmpty()

Return a default value if string is empty. ConductorOne extension.

```cel
string.ifEmpty(default: string) -> string
```

**Example:**
```cel
// Default for empty department
subject.department.ifEmpty("Unknown")

// Chain with other operations
subject.profile["team"].ifEmpty("Unassigned").lowerAscii()
```

---

## contains()

Check if string contains a substring.

```cel
string.contains(substring: string) -> bool
```

**Example:**
```cel
subject.job_title.contains("Manager")
subject.email.contains("@company.com")
```

---

## startsWith() / endsWith()

Check string prefix or suffix.

```cel
string.startsWith(prefix: string) -> bool
string.endsWith(suffix: string) -> bool
```

**Example:**
```cel
// Email domain check
subject.email.endsWith("@company.com")

// Department prefix
subject.department.startsWith("Engineering")
```

---

## lowerAscii() / upperAscii()

Convert to lowercase or uppercase (ASCII only).

```cel
string.lowerAscii() -> string
string.upperAscii() -> string
```

**Example:**
```cel
// Case-insensitive comparison
subject.department.lowerAscii() == "engineering"

// Case-insensitive contains
subject.job_title.lowerAscii().contains("manager")
```

---

## size()

Get string length.

```cel
size(string) -> int
```

**Example:**
```cel
size(subject.department) > 0
```

---

## has() vs ifEmpty()

| Scenario | Use | Why |
|----------|-----|-----|
| Field might not exist | `has()` | Prevents runtime error |
| Field exists but might be empty | `ifEmpty()` | Provides default for empty |
| Both | Combine | `has(x) ? x.ifEmpty("default") : "missing"` |

`has()` checks existence. `ifEmpty()` handles empty strings. Different problems.

---

## Common Patterns

### Case-Insensitive Match

```cel
subject.job_title.lowerAscii().contains("manager")
```

### Email Domain Check

```cel
subject.email.lowerAscii().endsWith("@company.com")
```

### Safe Field Access with Default

```cel
has(subject.department) ? subject.department.ifEmpty("Unknown") : "Not Set"
```
