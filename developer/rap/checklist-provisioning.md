# Provisioning Checklist

Verify Grant/Revoke operations before shipping.

## ExternalId

- [ ] All resources set `ExternalId`
- [ ] `ExternalId` uses the native system's identifier (what the API expects)
- [ ] `ExternalId` is set even for resources that won't be provisioned (consistency)

## Grant/Revoke Implementation

- [ ] `Grant()` contains actual API call logic (not just `return nil`)
- [ ] `Revoke()` contains actual API call logic
- [ ] Both handle errors and return meaningful messages
- [ ] Both are idempotent (safe to call twice)

## Validate()

- [ ] `Validate()` makes an actual API call
- [ ] `Validate()` returns error if credentials are invalid
- [ ] `Validate()` does NOT just return nil

## Testing

- [ ] Tested in sandbox environment
- [ ] Grant operation verified (user gains access)
- [ ] Revoke operation verified (user loses access)
- [ ] Error cases handled (user not found, permission denied)

## Quick Verification

```bash
# Test grant
./baton-myservice grant --entitlement "group:123:member" --principal "user:456"

# Test revoke
./baton-myservice revoke --grant "grant-id"

# Verify validate catches bad credentials
./baton-myservice --api-key "invalid" validate
# Should error, not succeed
```

## Common Mistakes

**No ExternalId:**
```go
// Wrong - provisioning can't find resource
resource, _ := rs.NewResource(name, rt, id)

// Correct
resource, _ := rs.NewResource(name, rt, id,
    rs.WithExternalID(&v2.ExternalId{Id: nativeID}),
)
```

**Stub implementations:**
```go
// Wrong - doesn't actually provision
func (c *Connector) Grant(...) error {
    return nil
}

// Correct - calls the API
func (c *Connector) Grant(...) error {
    return c.client.AddMember(ctx, groupID, userID)
}
```

**Validate always succeeds:**
```go
// Wrong
func (c *Connector) Validate(ctx context.Context) error {
    return nil
}

// Correct
func (c *Connector) Validate(ctx context.Context) error {
    _, err := c.client.GetCurrentUser(ctx)
    return err
}
```
