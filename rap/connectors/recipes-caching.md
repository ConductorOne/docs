# recipes-caching

Caching patterns and anti-patterns for connectors.

---

## When to cache

| Scenario | Cache? | Reason |
|----------|--------|--------|
| Grants() needs user details from List() | Yes | Avoids N+1 API calls |
| Entitlements() needs role definitions | Yes | Role metadata is stable |
| List() needs parent context | Maybe | Often passed via parentID |
| Any data across sync runs | No | Stale data causes drift |

Do NOT cache across sync runs. Connector restarts clear caches anyway.

---

## Thread-safe caching with sync.Map

```go
type Connector struct {
    client    *client.Client
    userCache sync.Map  // map[userID]User - struct field, not package-level
}

// Populate during List()
func (u *userBuilder) List(ctx context.Context, _ *v2.ResourceId,
    pToken *pagination.Token) ([]*v2.Resource, string, annotations.Annotations, error) {

    users, next, err := u.client.ListUsers(ctx, pToken.Token)
    if err != nil {
        return nil, "", nil, err
    }

    var resources []*v2.Resource
    for _, user := range users {
        u.connector.userCache.Store(user.ID, user)  // Cache for later
        r, _ := resource.NewUserResource(user.Name, userResourceType, user.ID)
        resources = append(resources, r)
    }
    return resources, next, nil, nil
}

// Use during Grants()
func (g *groupBuilder) Grants(ctx context.Context, resource *v2.Resource,
    pToken *pagination.Token) ([]*v2.Grant, string, annotations.Annotations, error) {

    memberIDs, _ := g.client.GetGroupMemberIDs(ctx, resource.Id.Resource)

    var grants []*v2.Grant
    for _, memberID := range memberIDs {
        if cached, ok := g.connector.userCache.Load(memberID); ok {
            user := cached.(User)
            // Use cached user data
        }
    }
    return grants, "", nil, nil
}
```

---

## ANTI-PATTERN: Package-level caches

**Critical bug pattern.** Package-level `sync.Map` persists across syncs in daemon mode.

```go
// WRONG - package-level cache persists across syncs
var userCache sync.Map

func lookupUser(id string) (*User, bool) {
    if cached, ok := userCache.Load(id); ok {
        return cached.(*User), true
    }
    return nil, false
}
```

What goes wrong:
1. Sync 1 caches users A, B, C
2. User B deleted from target system
3. Sync 2 runs (same process in daemon mode)
4. Cache still has user B
5. Grants reference deleted user
6. Access reviews show phantom access

**Correct pattern - struct-scoped:**

```go
type Connector struct {
    client    *client.Client
    userCache sync.Map  // Fresh per connector instance
}

func New(ctx context.Context, client *client.Client) *Connector {
    return &Connector{
        client:    client,
        userCache: sync.Map{},  // Fresh cache
    }
}
```

Find violations:
```bash
grep -r "^var.*sync\.Map" pkg/
```

---

## Memory-bounded caching

For large datasets, use LRU cache:

```go
import "github.com/hashicorp/golang-lru/v2"

type Connector struct {
    userCache *lru.Cache[string, User]
}

func New(ctx context.Context) (*Connector, error) {
    cache, err := lru.New[string, User](10000)  // Max 10k entries
    if err != nil {
        return nil, err
    }
    return &Connector{userCache: cache}, nil
}
```

Alternative for very large datasets - batch lookups instead of caching:

```go
func (c *Connector) lookupUsers(ctx context.Context, ids []string) (map[string]User, error) {
    return c.client.GetUsersByIDs(ctx, ids)  // Single batch API call
}
```

---

## Cache lifetime in daemon mode

| Mode | Cache Lifetime | Risk |
|------|----------------|------|
| One-shot (CLI) | Process lifetime | Low - exits after sync |
| Daemon mode | Must be managed | High - stale data persists |

Clear caches at sync boundaries:

```go
type Connector struct {
    client    *client.Client
    userCache sync.Map
}

func (c *Connector) PrepareForSync(ctx context.Context) error {
    c.userCache = sync.Map{}  // Clear from previous sync
    return nil
}
```

Time-based invalidation for long syncs:

```go
type Connector struct {
    userCache        sync.Map
    cachePopulatedAt time.Time
}

func (c *Connector) getCachedUser(id string) (*User, bool) {
    if time.Since(c.cachePopulatedAt) > 5*time.Minute {
        c.userCache = sync.Map{}
        c.cachePopulatedAt = time.Now()
    }
    if cached, ok := c.userCache.Load(id); ok {
        return cached.(*User), true
    }
    return nil, false
}
```

---

## Cache expectations by mode

| Scenario | Expected Behavior |
|----------|-------------------|
| CLI one-shot | Cache lives for single sync, process exits |
| Daemon between syncs | Cache cleared before each sync |
| Daemon during sync | Cache valid for sync duration |
| Long sync (>5 min) | Consider time-based invalidation |
