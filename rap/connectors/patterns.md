# patterns

Key patterns for robust Baton connector implementation.

---

## Entity Sources in Grant/Revoke

In Grant/Revoke operations, data comes from two entities. Use the right one.

**Principal** provides context (who):
```go
// Context (workspace, org, tenant) comes from principal
workspaceID := principal.ParentResourceId.Resource
userID := principal.Id.Resource
```

**Entitlement** provides the target (what):
```go
// The permission/role being granted comes from entitlement
roleID := entitlement.Resource.Id.Resource
```

**Pattern**: Ask "which entity provides this data?" Principal = who. Entitlement = what.

---

## HTTP Response Handling

Always check error before using response.

**Correct pattern**:
```go
resp, err := client.Do(req)
if err != nil {
    return fmt.Errorf("request failed: %w", err)
}
defer resp.Body.Close()
```

**When you need response body on error**:
```go
resp, err := client.Do(req)
if err != nil {
    if resp != nil {
        defer resp.Body.Close()
        // Can read error body here
    }
    return err
}
defer resp.Body.Close()
```

---

## Pagination Termination

Use explicit next token to terminate, not result count.

**Correct pattern**:
```go
for {
    results, nextToken, err := client.List(ctx, cursor)
    if err != nil {
        return err
    }
    // process results...
    if nextToken == "" {
        break  // Explicit end signal
    }
    cursor = nextToken
}
```

**Pagination bag initialization**:
```go
// Initialize bag on first call
if bag.Current() == nil {
    bag.Push(pagination.PageState{Token: ""})
}
state := bag.Current()
```

---

## Idempotent Operations

Grant and Revoke should be idempotent.

**Grant - handle "already exists"**:
```go
err := client.AddMember(ctx, groupID, userID)
if err != nil {
    if isAlreadyExistsError(err) {
        // Success - desired state achieved
        grant := sdkGrant.NewGrant(entitlement.Resource, entitlement.Slug, principal.Id)
        return []*v2.Grant{grant}, nil, nil
    }
    return nil, nil, err
}
```

**Revoke - handle "not found"**:
```go
err := client.RemoveMember(ctx, groupID, userID)
if err != nil && !isNotFoundError(err) {
    return nil, err
}
return nil, nil  // Success - desired state achieved
```

---

## ParentResourceId Access

Check for nil before accessing ParentResourceId.

**Correct pattern**:
```go
var parentID string
if resource.ParentResourceId != nil {
    parentID = resource.ParentResourceId.Resource
}
```

---

## Map Type Assertions

Use two-value form for type assertions.

**Correct pattern**:
```go
userID, ok := data["user_id"].(string)
if !ok {
    return fmt.Errorf("user_id missing or not string")
}
```

---

## API Argument Order

When APIs take multiple string IDs, verify order matches API signature.

**Document clearly**:
```go
// AddMember(groupID, userID) - order per API docs
err := client.AddMember(
    groupID,  // first param: group
    userID,   // second param: user
)
```

---

## JSON ID Flexibility

APIs may return IDs as numbers or strings. Handle both.

**Flexible pattern**:
```go
type User struct {
    ID json.Number `json:"id"`  // Handles "12345" and 12345
}

// Usage
userID := user.ID.String()
```

---

## Trait Selection

Match traits to entity type.

| Entity Type | Trait |
|-------------|-------|
| Human users | `TRAIT_USER` |
| Service accounts | `TRAIT_APP` |
| AWS accounts | `TRAIT_APP` |
| Groups | `TRAIT_GROUP` |
| Roles | `TRAIT_ROLE` |

---

## Quick Reference

1. Grant/Revoke: Principal = who, Entitlement = what
2. HTTP: Check error before accessing response
3. Pagination: Use explicit token for termination
4. Idempotency: "Already exists" and "not found" are success
5. ParentResourceId: Nil-check before access
6. Map access: Use two-value type assertion
7. API calls: Verify argument order
8. JSON IDs: Use json.Number for flexibility
9. Traits: Service accounts use App, humans use User
