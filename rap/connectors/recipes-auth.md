# recipes-auth

Authentication patterns for connector API clients.

---

## API key (Bearer token)

```go
import "github.com/conductorone/baton-sdk/pkg/uhttp"

func NewClient(ctx context.Context, apiKey string) (*Client, error) {
    httpClient, err := uhttp.NewBaseHttpClient(ctx,
        uhttp.WithBearerToken(apiKey))
    if err != nil {
        return nil, err
    }
    return &Client{http: httpClient, baseURL: "https://api.example.com"}, nil
}
```

`WithBearerToken` sets `Authorization: Bearer <token>`. The SDK handles retries and rate limiting.

---

## OAuth2 client credentials

```go
import "golang.org/x/oauth2/clientcredentials"

func NewClient(ctx context.Context, clientID, clientSecret, tokenURL string) (*Client, error) {
    config := &clientcredentials.Config{
        ClientID:     clientID,
        ClientSecret: clientSecret,
        TokenURL:     tokenURL,
        Scopes:       []string{"read", "write"},
    }
    httpClient := config.Client(ctx)  // Auto-refreshes tokens
    return &Client{http: httpClient}, nil
}
```

The `clientcredentials` package handles token refresh automatically.

---

## JWT service account (Google-style)

```go
import (
    "google.golang.org/api/option"
    admin "google.golang.org/api/admin/directory/v1"
)

func NewGoogleClient(ctx context.Context, credentialsJSON []byte, adminEmail string) (*admin.Service, error) {
    config, err := google.JWTConfigFromJSON(credentialsJSON,
        admin.AdminDirectoryUserReadonlyScope,
        admin.AdminDirectoryGroupReadonlyScope,
    )
    if err != nil {
        return nil, fmt.Errorf("failed to parse credentials: %w", err)
    }
    config.Subject = adminEmail  // Impersonate domain admin
    return admin.NewService(ctx, option.WithHTTPClient(config.Client(ctx)))
}
```

Domain-wide delegation requires `Subject` to specify which user to impersonate.

---

## LDAP bind

```go
import "github.com/go-ldap/ldap/v3"

func NewLDAPClient(ctx context.Context, serverURL, bindDN, bindPassword string) (*ldap.Conn, error) {
    conn, err := ldap.DialURL(serverURL) // ldaps://dc.example.com:636
    if err != nil {
        return nil, fmt.Errorf("failed to connect to LDAP: %w", err)
    }
    err = conn.Bind(bindDN, bindPassword)
    if err != nil {
        conn.Close()
        return nil, fmt.Errorf("failed to bind: %w", err)
    }
    return conn, nil
}
```

LDAP requires binding before queries. Use `ldaps://` (port 636) for TLS.

---

## Basic auth

```go
func NewClient(ctx context.Context, username, password string) (*Client, error) {
    httpClient, err := uhttp.NewBaseHttpClient(ctx,
        uhttp.WithBasicAuth(username, password))
    if err != nil {
        return nil, err
    }
    return &Client{http: httpClient}, nil
}
```

---

## Custom header auth

Some APIs use non-standard headers like `X-API-Key`:

```go
func NewClient(ctx context.Context, apiKey string) (*Client, error) {
    httpClient, err := uhttp.NewBaseHttpClient(ctx)
    if err != nil {
        return nil, err
    }
    // Add custom header to all requests
    httpClient.Transport = &headerTransport{
        base:   httpClient.Transport,
        header: "X-API-Key",
        value:  apiKey,
    }
    return &Client{http: httpClient}, nil
}

type headerTransport struct {
    base   http.RoundTripper
    header string
    value  string
}

func (t *headerTransport) RoundTrip(req *http.Request) (*http.Response, error) {
    req.Header.Set(t.header, t.value)
    return t.base.RoundTrip(req)
}
```
