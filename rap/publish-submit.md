# publish-submit

Publishing connectors to the connector registry.

---

## Publishing flow

```
1. Create Connector  --> Registry
2. Create Version    --> Registry
3. Upload Binaries   --> Registry
4. Finalize Version  --> Registry --> Connector Hub
```

---

## Version states

```
PENDING -> UPLOADING -> VALIDATING -> PUBLISHED
                              |
                              +-> FAILED
PUBLISHED -> YANKED
```

| State | Meaning |
|-------|---------|
| PENDING | Version created, awaiting uploads |
| UPLOADING | Assets being uploaded |
| VALIDATING | Validation in progress |
| PUBLISHED | Available for download |
| YANKED | Withdrawn (still visible) |
| FAILED | Validation failed |

---

## Release manifest

| Field | Purpose |
|-------|---------|
| org | Organization identifier |
| name | Connector name |
| version | Semantic version |
| description | Human-readable description |
| repository_url | Source code repo |
| license | License identifier |
| assets | Platform binaries |
| commit_sha | Git commit |

---

## Asset structure

| Field | Purpose |
|-------|---------|
| platform | Target (e.g., `linux-amd64`) |
| filename | Binary filename |
| size_bytes | File size |
| sha256 | Checksum |
| download_url | Download location |
| signature_url | Detached signature |

---

## Supported platforms

| Platform | Description |
|----------|-------------|
| darwin-amd64 | macOS Intel |
| darwin-arm64 | macOS Apple Silicon |
| linux-amd64 | Linux x86_64 |
| linux-arm64 | Linux ARM64 |
| windows-amd64 | Windows x86_64 |

---

## Publishing paths

### Contributing upstream (recommended)

1. Fork existing connector repo
2. Add changes
3. Submit PR
4. Maintainers review and merge
5. New version published

Benefits: community benefits, maintainers handle publishing.

### Fork and maintain

1. Fork repository
2. Publish under your org
3. Maintain independently

Trade-off: Full control but ongoing maintenance burden.

### Internal only

1. Don't publish to public registry
2. Deploy in daemon mode on your infrastructure
3. Suitable for proprietary systems

---

## Signing

Connectors can be signed with:
- GPG signatures
- Cosign (sigstore)

Signatures verified during download.

---

## Pre-submission checklist

Before publishing:

- [ ] Connector syncs correctly
- [ ] Required permissions documented
- [ ] README complete
- [ ] No credentials in code
- [ ] License file present
- [ ] Tests pass
- [ ] Lint passes
- [ ] Builds for all platforms

---

## Versioning

Use semantic versioning:

| Version | When |
|---------|------|
| Major (1.0 -> 2.0) | Breaking changes |
| Minor (1.0 -> 1.1) | New features, backward compatible |
| Patch (1.0.0 -> 1.0.1) | Bug fixes |

---

## CI/CD

Most connectors use GitHub Actions:

```yaml
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    # Build all platforms
    # Upload to registry
    # Sign binaries
```

Tag push triggers release workflow.
