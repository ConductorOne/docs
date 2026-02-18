# recipes-errors

Error handling patterns for connectors.

---

## Distinguish retryable from fatal errors

```go
func (u *userBuilder) List(ctx context.Context, _ *v2.ResourceId,
    pToken *pagination.Token) ([]*v2.Resource, string, annotations.Annotations, error) {

    users, err := u.client.ListUsers(ctx)
    if err != nil {
        if isRateLimitError(err) || isNetworkError(err) {
            return nil, "", nil, err  // SDK retries automatically
        }
        if isAuthError(err) {
            return nil, "", nil, fmt.Errorf("baton-example: authentication failed (check credentials): %w", err)
        }
        return nil, "", nil, err
    }
    // ...
}

func isRateLimitError(err error) bool {
    var httpErr *HTTPError
    if errors.As(err, &httpErr) {
        return httpErr.StatusCode == 429
    }
    return false
}
```

SDK handles retries for transient errors. Fatal errors need clear messages.

---

## Context cancellation in loops

```go
func (u *userBuilder) List(ctx context.Context, _ *v2.ResourceId,
    pToken *pagination.Token) ([]*v2.Resource, string, annotations.Annotations, error) {

    users, err := u.client.ListUsers(ctx)
    if err != nil {
        return nil, "", nil, err
    }

    var resources []*v2.Resource
    for _, user := range users {
        select {
        case <-ctx.Done():
            return nil, "", nil, ctx.Err()
        default:
        }
        r, err := resource.NewUserResource(user.Name, userResourceType, user.ID)
        if err != nil {
            return nil, "", nil, err
        }
        resources = append(resources, r)
    }
    return resources, "", nil, nil
}
```

Check `ctx.Done()` in loops processing many items. Cancelled context means stop immediately.

---

## Error prefix convention

Prefix errors with connector name for debugging:

```go
return nil, "", nil, fmt.Errorf("baton-example: failed to list users: %w", err)
```

Pattern: `baton-<name>: <action>: %w`

---

## Wrapping vs returning errors

**Wrap** when adding context:
```go
if err != nil {
    return fmt.Errorf("failed to parse user %s: %w", userID, err)
}
```

**Return directly** when no additional context helps:
```go
if err != nil {
    return err
}
```

---

## HTTP status code handling

| Status | Meaning | Action |
|--------|---------|--------|
| 400 | Bad request | Fatal - log request details |
| 401 | Unauthorized | Fatal - check credentials |
| 403 | Forbidden | Fatal - check permissions |
| 404 | Not found | Usually skip, not error |
| 429 | Rate limited | Retry (SDK handles) |
| 500+ | Server error | Retry (SDK handles) |

```go
func handleResponse(resp *http.Response) error {
    switch resp.StatusCode {
    case http.StatusOK, http.StatusCreated:
        return nil
    case http.StatusNotFound:
        return nil  // Resource doesn't exist, not an error
    case http.StatusUnauthorized:
        return fmt.Errorf("baton-example: unauthorized (check API key)")
    case http.StatusForbidden:
        return fmt.Errorf("baton-example: forbidden (check permissions)")
    default:
        if resp.StatusCode >= 500 {
            return fmt.Errorf("server error: %d", resp.StatusCode)  // Will retry
        }
        return fmt.Errorf("unexpected status: %d", resp.StatusCode)
    }
}
```

---

## Partial success handling

When processing multiple items, decide strategy upfront:

**Fail fast** (default for sync):
```go
for _, item := range items {
    if err := process(item); err != nil {
        return err  // Stop on first error
    }
}
```

**Collect errors** (for provisioning):
```go
var errs []error
for _, item := range items {
    if err := process(item); err != nil {
        errs = append(errs, fmt.Errorf("item %s: %w", item.ID, err))
    }
}
if len(errs) > 0 {
    return errors.Join(errs...)
}
```
