# community

Getting help and contributing to the Baton connector ecosystem.

---

## Getting help

### GitHub Discussions

| Repository | Use For |
|------------|---------|
| [baton-sdk](https://github.com/ConductorOne/baton-sdk/discussions) | SDK questions, general development |
| Specific connector repos | Issues with that connector |

Before asking:
1. Search existing issues
2. Check documentation
3. Review Cookbook patterns

### Good question format

Include:
- What you're trying to accomplish
- What you've tried
- Error messages (full text)
- Relevant code
- Connector version

Bad: "My connector doesn't work"

Good: "Sync fails with 'unauthorized' when listing users. Using baton-okta v0.5.2, API token auth, read_users scope. Error: [full text]"

---

## Support channels

| Channel | Response | Use For |
|---------|----------|---------|
| GitHub Issues | Days | Bugs, features |
| GitHub Discussions | Days | Questions |
| ConductorOne Support | Hours | Production (customers) |

---

## Reporting issues

### Bug report template

```markdown
**Connector:** baton-example v1.2.3
**Environment:** macOS 14.0, Go 1.23

**Steps:**
1. Configure with API key
2. Run sync
3. Observe error

**Expected:** Sync completes
**Actual:** Error: [paste]
```

### Feature requests

Describe the problem, not just the solution:

Good: "Need to sync custom Okta attributes for access reviews"

Not: "Add custom attribute support"

### Security issues

DO NOT file publicly.

Report to: security@conductorone.com

---

## Contributing

### Pre-PR checklist

- [ ] Follows SDK patterns
- [ ] `make lint` passes
- [ ] `make test` passes
- [ ] README documents permissions
- [ ] No credentials in code

### Flow

```
1. Fork repo
2. Create branch
3. Make changes
4. Run build/lint/test
5. Submit PR
6. Address feedback
7. Merge
```

---

## Maintainer guide

### Responsibilities

| Task | Frequency |
|------|-----------|
| Triage issues | Weekly |
| Review PRs | As submitted |
| Update deps | Monthly |
| Release versions | As needed |
| Security monitoring | Ongoing |

### Release process

```bash
git tag v1.2.3
git push origin v1.2.3
# GitHub Actions handles build and release
```

### Issue handling

| Type | Response |
|------|----------|
| Bug with repro | Prioritize fix |
| Bug without repro | Request info |
| Feature request | Evaluate, label |
| Question | Point to docs |
| Security | Follow security process |

---

## Code of conduct

Follows Contributor Covenant.

Report violations to: open-source@conductorone.com
