# build-pagination

Token vs Bag, cursor vs offset, nested pagination patterns.

---

## Two Pagination Strategies

**Cursor-based**: API returns opaque token for next page
```
GET /users?cursor=abc123
Response: { users: [...], next_cursor: "def456" }
```

**Offset-based**: You track page number or offset
```
GET /users?offset=100&limit=50
Response: { users: [...], total: 500 }
```

## Simple Pagination with Token

For flat lists where API returns a next-page token:

```go
func (b *userBuilder) List(
    ctx context.Context,
    parentResourceID *v2.ResourceId,
    token *pagination.Token,
) ([]*v2.Resource, string, annotations.Annotations, error) {
    pageToken := ""
    if token != nil && token.Token != "" {
        pageToken = token.Token
    }

    users, nextToken, err := b.client.ListUsers(ctx, pageToken, 100)
    if err != nil {
        return nil, "", nil, err
    }

    // Convert users to resources...

    // Return nextToken directly - empty string means done
    return resources, nextToken, nil, nil
}
```

## Offset-Based Pagination

When API uses offset/limit instead of cursors:

```go
func (b *userBuilder) List(
    ctx context.Context,
    parentResourceID *v2.ResourceId,
    token *pagination.Token,
) ([]*v2.Resource, string, annotations.Annotations, error) {
    offset := 0
    if token != nil && token.Token != "" {
        var err error
        offset, err = strconv.Atoi(token.Token)
        if err != nil {
            return nil, "", nil, err
        }
    }

    pageSize := 100
    users, total, err := b.client.ListUsers(ctx, offset, pageSize)
    if err != nil {
        return nil, "", nil, err
    }

    // Convert users to resources...

    // Calculate next token
    nextOffset := offset + len(users)
    nextToken := ""
    if nextOffset < total {
        nextToken = strconv.Itoa(nextOffset)
    }

    return resources, nextToken, nil, nil
}
```

## Nested Pagination with Bag

When paginating children within parents (e.g., members within groups):

```go
func (b *groupBuilder) Grants(
    ctx context.Context,
    resource *v2.Resource,
    token *pagination.Token,
) ([]*v2.Grant, string, annotations.Annotations, error) {
    bag := &pagination.Bag{}
    if token != nil && token.Token != "" {
        err := bag.Unmarshal(token.Token)
        if err != nil {
            return nil, "", nil, err
        }
    }

    // Get or initialize page state
    pageState := bag.Current()
    if pageState == nil {
        pageState = &pagination.PageState{
            ResourceTypeID: "member",
            ResourceID:     resource.Id.Resource,
        }
        bag.Push(pageState)
    }

    // Fetch members using page state token
    members, nextCursor, err := b.client.GetGroupMembers(
        ctx,
        resource.Id.Resource,
        pageState.Token,
    )
    if err != nil {
        return nil, "", nil, err
    }

    // Convert to grants...

    // Update pagination state
    if nextCursor != "" {
        pageState.Token = nextCursor
    } else {
        bag.Pop()
    }

    nextToken, err := bag.Marshal()
    if err != nil {
        return nil, "", nil, err
    }

    return grants, nextToken, nil, nil
}
```

## Meta-Connector Pagination

In YAML config, declare pagination strategy:

```yaml
# Cursor-based
pagination:
  strategy: "cursor"
  primary_key: "id"

# Offset-based
pagination:
  strategy: "offset"
  limit_param: "limit"
  offset_param: "offset"
  page_size: 100
```

For baton-sql, use query placeholders:
```sql
SELECT * FROM users
WHERE id > ?<Cursor>
ORDER BY id ASC
LIMIT ?<Limit>
```

## Critical Invariant

**Your next token must progress.** The SDK detects loops where the same token is returned twice in a row and errors.

```go
// WRONG - returns same token, causes infinite loop
if hasMore {
    return resources, currentToken, nil, nil  // Bug!
}

// RIGHT - return new token or empty string
if hasMore {
    return resources, newToken, nil, nil
}
return resources, "", nil, nil  // Done
```
