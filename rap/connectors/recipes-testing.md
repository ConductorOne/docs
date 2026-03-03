# recipes-testing

Testing patterns for connectors.

---

## Configurable base URL (required)

Every connector must support configurable base URL for testing:

```go
// cmd/baton-example/main.go
fields := []field.SchemaField{
    field.StringField("api-key",
        field.WithRequired(true),
        field.WithDescription("API key for authentication"),
    ),
    field.StringField("base-url",
        field.WithDefaultValue("https://api.example.com"),
        field.WithDescription("Base URL (use http://localhost:8080 for testing)"),
    ),
}

// pkg/client/client.go
func New(cfg *Config) *Client {
    baseURL := cfg.BaseURL
    if baseURL == "" {
        baseURL = "https://api.example.com"
    }
    return &Client{baseURL: baseURL}
}
```

Usage:
```bash
./baton-example --api-key $KEY                           # Production
./baton-example --api-key test --base-url http://localhost:8080  # Testing
```

Without configurable base URL, you cannot test without hitting production.

---

## Insecure TLS for mock servers

For mock servers with self-signed certificates:

```go
type Config struct {
    APIKey   string `mapstructure:"api-key"`
    BaseURL  string `mapstructure:"base-url"`
    Insecure bool   `mapstructure:"insecure"`
}

func New(ctx context.Context, cfg *Config) (*Client, error) {
    opts := []uhttp.Option{}
    if cfg.Insecure {
        transport := &http.Transport{
            TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
        }
        opts = append(opts, uhttp.WithTransport(transport))
    }
    httpClient, err := uhttp.NewBaseHttpClient(ctx, opts...)
    if err != nil {
        return nil, err
    }
    return &Client{http: httpClient, baseURL: cfg.BaseURL}, nil
}
```

Usage:
```bash
./baton-example --api-key test --base-url https://localhost:8443 --insecure
```

---

## Unit testing resource builders

```go
func TestUserBuilder_List(t *testing.T) {
    // Mock client
    mockClient := &MockClient{
        users: []User{
            {ID: "u1", Name: "Alice", Email: "alice@example.com"},
            {ID: "u2", Name: "Bob", Email: "bob@example.com"},
        },
    }

    builder := &userBuilder{client: mockClient}
    resources, nextToken, _, err := builder.List(context.Background(), nil, &pagination.Token{})

    require.NoError(t, err)
    require.Len(t, resources, 2)
    require.Empty(t, nextToken)

    assert.Equal(t, "u1", resources[0].Id.Resource)
    assert.Equal(t, "Alice", resources[0].DisplayName)
}
```

---

## Integration testing with mock server

```go
func TestConnector_Integration(t *testing.T) {
    // Start mock server
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        switch r.URL.Path {
        case "/users":
            json.NewEncoder(w).Encode(map[string]any{
                "users": []map[string]string{
                    {"id": "u1", "name": "Alice"},
                },
            })
        default:
            w.WriteHeader(http.StatusNotFound)
        }
    }))
    defer server.Close()

    // Create connector pointing to mock
    cfg := &Config{
        APIKey:  "test-key",
        BaseURL: server.URL,
    }
    connector, err := NewConnector(context.Background(), cfg)
    require.NoError(t, err)

    // Test sync
    // ...
}
```

---

## Testing pagination

```go
func TestUserBuilder_Pagination(t *testing.T) {
    mockClient := &MockClient{
        pages: map[string][]User{
            "":       {{ID: "u1"}, {ID: "u2"}},  // First page
            "page2":  {{ID: "u3"}, {ID: "u4"}},  // Second page
            "page3":  {{ID: "u5"}},               // Last page
        },
        nextTokens: map[string]string{
            "":      "page2",
            "page2": "page3",
            "page3": "",  // Empty = no more pages
        },
    }

    builder := &userBuilder{client: mockClient}

    // First page
    r1, next1, _, _ := builder.List(ctx, nil, &pagination.Token{Token: ""})
    assert.Len(t, r1, 2)
    assert.Equal(t, "page2", next1)

    // Second page
    r2, next2, _, _ := builder.List(ctx, nil, &pagination.Token{Token: "page2"})
    assert.Len(t, r2, 2)
    assert.Equal(t, "page3", next2)

    // Last page
    r3, next3, _, _ := builder.List(ctx, nil, &pagination.Token{Token: "page3"})
    assert.Len(t, r3, 1)
    assert.Empty(t, next3)
}
```

---

## Testing grants

```go
func TestGroupBuilder_Grants(t *testing.T) {
    mockClient := &MockClient{
        groupMembers: map[string][]string{
            "g1": {"u1", "u2"},
        },
    }

    builder := &groupBuilder{client: mockClient}
    groupResource := makeGroupResource("g1", "Admins")

    grants, _, _, err := builder.Grants(ctx, groupResource, &pagination.Token{})

    require.NoError(t, err)
    require.Len(t, grants, 2)
    assert.Equal(t, "u1", grants[0].Principal.Id.Resource)
    assert.Equal(t, "u2", grants[1].Principal.Id.Resource)
}
```

---

## Makefile test targets

```makefile
.PHONY: test
test:
	go test -v ./...

.PHONY: test-integration
test-integration:
	go test -v -tags=integration ./...

.PHONY: test-coverage
test-coverage:
	go test -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out
```
