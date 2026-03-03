# Time Functions

Functions for working with dates, times, and durations.

## now()

Get the current timestamp.

```cel
now() -> timestamp
```

**Example:**
```cel
// Business hours check (UTC)
now().getHours() >= 9 && now().getHours() < 17
```

---

## time.parse

Parse a string into a timestamp.

```cel
time.parse(value: string, layout: string) -> timestamp
time.parse(value: string, layout: string, timezone: string) -> timestamp
```

**Layout aliases:** `rfc3339`, `date`, `datetime`, `time`

**Example:**
```cel
// Parse hire date from profile
time.parse(subject.profile["hire_date"], "date")

// With timezone
time.parse("2024-01-15", "date", "America/New_York")
```

---

## time.format

Format a timestamp as a string.

```cel
time.format(ts: timestamp, layout: string) -> string
time.format(ts: timestamp, layout: string, timezone: string) -> string
```

**Example:**
```cel
// Format for display
time.format(now(), "datetime", "America/New_York")
```

---

## time.unix

Create timestamp from Unix epoch seconds.

```cel
time.unix(seconds: int) -> timestamp
```

**Example:**
```cel
// Parse Unix timestamp from profile
time.unix(int(subject.profile["last_login"])) > now() - duration("720h")
```

---

## time.start_of / time.truncate

Truncate timestamp to start of a time unit.

```cel
time.start_of(ts: timestamp, unit: string) -> timestamp
time.truncate(ts: timestamp, unit: string) -> timestamp
```

**Units:** `day`, `week`, `month`, `quarter`, `year`, `hour`, `minute`

**Example:**
```cel
// Start of current quarter
time.start_of(now(), "quarter")
```

---

## time.end_of

Get end of a time unit.

```cel
time.end_of(ts: timestamp, unit: string) -> timestamp
```

**Example:**
```cel
// Access expires at end of quarter
time.end_of(now(), "quarter")
```

---

## duration()

Create a duration value.

```cel
duration(spec: string) -> duration
```

**Format:** `"Nh"` for hours, `"Nm"` for minutes, `"Ns"` for seconds

**Example:**
```cel
// Grants over 30 days
task.grant_duration > duration("720h")

// Recently hired (within 90 days)
time.parse(subject.profile["hire_date"], "date") > now() - duration("2160h")
```

---

## Common Patterns

### Recently Hired Users

```cel
has(subject.profile.hire_date) &&
  time.parse(subject.profile["hire_date"], "date") > now() - duration("2160h")
```

### Active Users (logged in within 30 days)

```cel
time.unix(int(subject.profile["last_login"])) > now() - duration("720h")
```

### Business Hours

```cel
now().getHours() >= 9 && now().getHours() < 17
```
