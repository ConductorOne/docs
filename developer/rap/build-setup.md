# Build Setup

How to start a new ConductorOne connector project.

## Prerequisites

- Go 1.21+
- `baton-sdk` v0.7.1+

## Project Structure

```
baton-myservice/
  cmd/baton-myservice/
    main.go           # Entry point, CLI setup
  pkg/
    connector/
      connector.go    # Implements ConnectorBuilder
      users.go        # User syncer
      groups.go       # Group syncer (if applicable)
    client/
      client.go       # API client for target service
  go.mod
  go.sum
```

## Minimal main.go

```go
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/conductorone/baton-sdk/pkg/cli"
    "github.com/conductorone/baton-sdk/pkg/connectorbuilder"
    "github.com/conductorone/baton-sdk/pkg/field"
    configSdk "github.com/conductorone/baton-sdk/pkg/field"
    "github.com/conductorone/baton-sdk/pkg/types"
    "github.com/conductorone/baton-myservice/pkg/connector"
)

var version = "dev"

func main() {
    ctx := context.Background()
    cfg := &connector.Config{}

    _, cmd, err := configSdk.DefineConfiguration(ctx, cfg,
        field.StringField("api-key", field.WithRequired(true)),
        field.StringField("base-url", field.WithDefaultValue("https://api.myservice.com")),
    )
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }

    cmd, err = cli.NewCmd(ctx, "baton-myservice", cfg, getConnector)
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }

    cmd.Version = version
    if err := cmd.Execute(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}

func getConnector(ctx context.Context, cfg *connector.Config) (types.ConnectorServer, error) {
    cb, err := connector.New(ctx, cfg)
    if err != nil {
        return nil, err
    }
    return connectorbuilder.NewConnector(ctx, cb)
}
```

## Config struct

```go
type Config struct {
    APIKey  string `mapstructure:"api-key"`
    BaseURL string `mapstructure:"base-url"`
}

func (c *Config) GetString(key string) string {
    switch key {
    case "api-key":
        return c.APIKey
    case "base-url":
        return c.BaseURL
    }
    return ""
}

func (c *Config) GetBool(key string) bool             { return false }
func (c *Config) GetInt(key string) int               { return 0 }
func (c *Config) GetStringSlice(key string) []string  { return nil }
func (c *Config) GetStringMap(key string) map[string]any { return nil }
```

## After creating files

```bash
go mod tidy    # Required - creates go.sum
go build ./... # Verify it compiles
```
