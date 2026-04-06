---
name: rebrand-connector
description: Apply the C1 rebrand to a single baton connector repo. Clones the repo, runs scripts/rebrand-connector.py on docs/connector.mdx, and opens a PR. Use for individual repos or as the inner loop when batching across the full connector fleet.
---

# Rebrand connector

Apply the C1 rebrand (brand name, brand color, GitHub org URL) to a single baton connector repo's `docs/connector.mdx`.

## Argument

A repo name in either of these forms:
- `baton-github`
- `ConductorOne/baton-github`

## Steps

### 1. Resolve the repo

Normalize the argument to `ConductorOne/<repo>`. If only `baton-github` is given, prepend `ConductorOne/`.

### 2. Clone to a temp directory

```bash
REPO=<resolved repo name, e.g. baton-github>
WORKDIR=/tmp/rebrand-$REPO
rm -rf $WORKDIR
git clone --depth=1 https://github.com/ConductorOne/$REPO.git $WORKDIR
```

### 3. Check for the target file

```bash
ls $WORKDIR/docs/connector.mdx
```

If the file doesn't exist, report that and stop — this repo doesn't have a connector doc to update.

### 4. Run the transform script

The script lives in the docs repo. Use its absolute path:

```bash
python3 /tmp/c1-docs-fresh/scripts/rebrand-connector.py $WORKDIR/docs/connector.mdx
```

If the script prints "No changes.", the file is already up to date. Report this and stop — no PR needed.

### 5. Create a branch, commit, and push

```bash
cd $WORKDIR
git checkout -b docs/c1-rebrand
git add docs/connector.mdx
git commit -m "docs: apply C1 rebrand to connector.mdx

Renames ConductorOne -> C1 in prose, comments, and placeholder text.
Updates brand color #65DE23 -> #c937ae.
Lowercases GitHub org name in repository link.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push origin docs/c1-rebrand
```

### 6. Open a PR

```bash
gh pr create \
  --repo ConductorOne/$REPO \
  --head docs/c1-rebrand \
  --base main \
  --title "docs: apply C1 rebrand to connector.mdx" \
  --body "Updates \`docs/connector.mdx\` with the C1 rebrand:

- Renames **ConductorOne** → **C1** in prose, comments, and placeholder text
- Updates brand color \`#65DE23\` → \`#c937ae\`
- Lowercases GitHub org name in the repository resource link

URLs that are case-sensitive or functional (distro site, tenant URLs, email addresses, file paths) are unchanged."
```

### 7. Report

Print the PR URL and confirm completion. Clean up the temp directory:

```bash
rm -rf $WORKDIR
```

---

## Batch all connector repos

To run across the full fleet, get every `baton-*` repo in the ConductorOne org and invoke this skill for each one:

```bash
gh repo list ConductorOne \
  --json name \
  --limit 500 \
  --jq '.[].name | select(startswith("baton-"))' \
  | sort \
  | while read repo; do
      echo "=== Processing $repo ==="
      # invoke: rebrand-connector $repo
    done
```

Run a single repo first (e.g. `baton-github`) and review the PR before batching the rest.
