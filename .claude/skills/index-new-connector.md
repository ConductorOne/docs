---
name: index-new-connector
description: >-
  Add a newly-published connector to the capabilities and intro index pages.
  Use when a new connector .mdx file has been added to /baton/ and needs to
  appear in the capabilities table and the A-Z/category/New this month lists.
---

# Index a new connector

Add entries for a new connector to `baton/capabilities.mdx` and `baton/intro.mdx`.

## Workflow

### 1. Read the connector file

```bash
# The connector slug is the filename without .mdx, e.g. "sonarqube"
cat baton/<connector-slug>.mdx
```

Extract from the connector file:
- **Display name** — from `sidebarTitle:` in frontmatter
- **Hosting** — does it have Cloud-hosted and/or Self-hosted tabs?
- **Provisioning** — from the capabilities table: does any resource have a checkmark in the Provision column?
- **Account provisioning/deprovisioning** — does it create users? Delete or deactivate them?
- **Other capabilities** — secrets syncing, last login, vault passwords, shadow apps, ticketing?
- **Category** — which `By category` section in intro.mdx fits best?

### 2. Build the capabilities.mdx row

The row format is:
```
| [Display Name](/baton/<slug>) | <hosting icons> | <provisioning icons> | <other icons> |
```

**Hosting icons** (`<Icon icon="cloud" />` = cloud-hosted, `<Icon icon="plug" />` = self-hosted):
- Both: `<Icon icon="cloud" /> <Icon icon="plug" />`
- Self-hosted only: `<Icon icon="plug" />`
- Cloud-hosted only: `<Icon icon="cloud" />`

**Provisioning icons** (leave column empty if connector is sync-only):
- `<Icon icon="key"  />` — provisions entitlements (roles, groups, permissions)
- `<Icon icon="user" />` — provisions accounts (creates users)
- `<Icon icon="face-confused"  />` — deprovisions accounts (deletes or deactivates users)

**Other icons** (leave empty if none apply):
- `<Icon icon="face-shush"  />` — syncs secrets
- `<Icon icon="clock" />` — reports last login
- `<Icon icon="ticket" />` — external ticketing support
- `<Icon icon="flashlight" />` — shadow app detection
- Vault password SVG (copy from another row that has it, e.g. Active Directory)

### 3. Find the insertion point in capabilities.mdx

The table is alphabetical, **case-insensitive, character by character**.

```bash
# Show rows near where the new connector would fall
grep -n "^\| \[" baton/capabilities.mdx | grep -i "^[0-9]*:| \[<first few letters>"
```

Common pitfall: names starting with the same letters need careful comparison.
- "SonarQube" (S-o-n-a-**r**) sorts before "Sonatype" (S-o-n-a-**t**) because r < t
- "ADP" (A-D-**P**) sorts after "Adobe" (A-D-**o**) because o < P

### 4. Add to intro.mdx in four places

#### A) A-Z tab (alphabetical, same rules as above)

```bash
grep -n "^\s*- \[" baton/intro.mdx | grep -i "<nearby name>"
```

#### B) New this month tab

Add the connector to the `<Tab title="New this month">` list. No fixed order required — just add it.

#### C) By category — pick one section

Common categories and what goes in them:

| Category | Fits |
| :--- | :--- |
| Cloud providers | AWS, GCP, Azure, cloud infrastructure |
| Data and analytics | BI tools, databases, data warehouses |
| Developer tools | CI/CD, code repos, dev platforms, code quality |
| Finance, legal, and ERP | Finance, billing, legal, ERP |
| Human resources and training | HRIS, payroll, learning management |
| Identity and access management | IdP, SSO, directory, PAM |
| IT management | ITSM, ticketing, device management, monitoring |
| Marketing and CRM | CRM, marketing automation, sales tools |
| Productivity and collaboration | Email, docs, calendars, messaging |
| Security | Security platforms, SIEM, vulnerability management |

Find the right alphabetical position within the chosen section.

#### D) (Optional) By category — secondary section

If the connector clearly fits a second category (e.g., a tool that is both a developer tool and a security tool), add it there too. When in doubt, skip.

### 5. Commit and open a PR

```bash
git checkout -b docs/index-<connector-slug>
git add baton/capabilities.mdx baton/intro.mdx
git commit -m "docs: add <Display Name> to connector indexes"
git push -u origin docs/index-<connector-slug>
gh pr create --title "docs: add <Display Name> to connector indexes" \
  --body "Adds <Display Name> to capabilities.mdx and intro.mdx."
```
