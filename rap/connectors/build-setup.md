# build-setup

Directory structure, go.mod, main.go, Makefile for a new connector.

---

## Project Structure

```
baton-myservice/
  cmd/
    baton-myservice/
      main.go          # Entry point
  pkg/
    connector/
      connector.go     # Connector interface implementation
      users.go         # User resource syncer
      groups.go        # Group resource syncer
      client.go        # API client wrapper
  go.mod
  go.sum
  Makefile
  .golangci.yaml
```

## go.mod

```go
module github.com/conductorone/baton-myservice

go 1.21

require (
    github.com/conductorone/baton-sdk v0.2.x
    github.com/grpc-ecosystem/go-grpc-middleware v1.4.0
)
```

Check baton-sdk for the current minimum Go version.

## main.go

```go
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/conductorone/baton-sdk/pkg/config"
    "github.com/conductorone/baton-sdk/pkg/connectorbuilder"
    "github.com/conductorone/baton-sdk/pkg/field"
    "github.com/conductorone/baton-sdk/pkg/types"
    "github.com/conductorone/baton-myservice/pkg/connector"
)

var version = "dev"

func main() {
    ctx := context.Background()

    cfg := &config.Config{
        Fields: []field.SchemaField{
            field.StringField("api-token",
                field.WithRequired(true),
                field.WithDescription("API token for authentication"),
            ),
            field.StringField("base-url",
                field.WithDescription("API base URL"),
                field.WithDefaultValue("https://api.myservice.com"),
            ),
        },
    }

    cb, err := connector.New(ctx, cfg)
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }

    c, err := connectorbuilder.NewConnector(ctx, cb)
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }

    connectorbuilder.Run(ctx, c, cfg)
}
```

## Connector Constructor

```go
// pkg/connector/connector.go
package connector

type Connector struct {
    client *MyServiceClient
}

func New(ctx context.Context, cfg *config.Config) (*Connector, error) {
    token := cfg.GetString("api-token")
    baseURL := cfg.GetString("base-url")

    client, err := NewClient(baseURL, token)
    if err != nil {
        return nil, err
    }

    return &Connector{client: client}, nil
}

func (c *Connector) ResourceSyncers(ctx context.Context) []connectorbuilder.ResourceSyncer {
    return []connectorbuilder.ResourceSyncer{
        newUserBuilder(c.client),
        newGroupBuilder(c.client),
    }
}

func (c *Connector) Metadata(ctx context.Context) (*v2.ConnectorMetadata, error) {
    return &v2.ConnectorMetadata{
        DisplayName: "My Service",
        Description: "Syncs users and groups from My Service",
    }, nil
}

func (c *Connector) Validate(ctx context.Context) (annotations.Annotations, error) {
    // Test the connection
    _, err := c.client.GetCurrentUser(ctx)
    if err != nil {
        return nil, fmt.Errorf("failed to validate credentials: %w", err)
    }
    return nil, nil
}
```

## Makefile

```makefile
GOOS = $(shell go env GOOS)
GOARCH = $(shell go env GOARCH)
BUILD_DIR = dist

.PHONY: build
build:
    go build -o $(BUILD_DIR)/baton-myservice ./cmd/baton-myservice

.PHONY: lint
lint:
    golangci-lint run

.PHONY: test
test:
    go test -v ./...

.PHONY: update-deps
update-deps:
    go get -u ./...
    go mod tidy
```

## Required Dependencies

| Tool | Purpose |
|------|---------|
| Go | See go.mod for version |
| golangci-lint | Code quality |
| make | Build automation |
