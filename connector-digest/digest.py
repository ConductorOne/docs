#!/usr/bin/env python3
"""
Connector docs digest.

Compares the current stable channel pointers against the saved snapshot,
fetches docs for changed connectors, and posts a summary to Slack.

Usage:
    python3 digest.py                  # print digest to stdout
    SLACK_WEBHOOK_URL=https://... python3 digest.py   # also post to Slack
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

REGISTRY_API = "https://dist.conductorone.com/api/v1"
SNAPSHOT_FILE = Path(__file__).parent / "snapshot.json"
_ENV_FILE = Path(__file__).parent / ".env"

def _load_env():
    if _ENV_FILE.exists():
        for line in _ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

_load_env()
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL", "")


def get_token():
    # Prefer explicit env var (works in GitHub Actions via secret)
    token = os.environ.get("REGISTRY_API_TOKEN", "")
    if token:
        return token
    # Fall back to local gh CLI
    try:
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
        token = result.stdout.strip()
        if token:
            return token
    except FileNotFoundError:
        pass
    # Anonymous fallback — sufficient for public stable channel data
    return ""


def api_get(path, token):
    url = f"{REGISTRY_API}{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def fetch_catalog(token):
    data = api_get("/catalog", token)
    connectors = data.get("catalog", {}).get("connectors", {})
    return {k: v.get("stableVersion", "") for k, v in connectors.items() if v.get("stableVersion")}


def fetch_docs(org, name, version, token):
    if not version:
        return ""
    try:
        data = api_get(f"/connectors/{org}/{name}/versions/{version}/documentation", token)
        return data.get("documentation", "")
    except urllib.error.HTTPError:
        return ""


def extract_capabilities_table(docs):
    lines = docs.split("\n")
    table_lines = []
    in_table = False
    for line in lines:
        if not in_table and "| Resource |" in line:
            in_table = True
        if in_table:
            if line.startswith("|"):
                table_lines.append(line)
            else:
                break
    return "\n".join(table_lines)


def diff_capabilities(old_table, new_table):
    if not old_table and not new_table:
        return None
    if not old_table:
        return None  # new connector — handled separately
    if not new_table:
        return "Capabilities table removed"
    if old_table == new_table:
        return None

    old_rows = [r.strip() for r in old_table.split("\n")[2:] if r.strip()]
    new_rows = [r.strip() for r in new_table.split("\n")[2:] if r.strip()]
    added = [r for r in new_rows if r not in old_rows]
    removed = [r for r in old_rows if r not in new_rows]

    changes = []
    for row in added:
        # Extract just the resource name from the table row
        resource = row.split("|")[1].strip() if "|" in row else row
        changes.append(f"+ {resource}")
    for row in removed:
        resource = row.split("|")[1].strip() if "|" in row else row
        changes.append(f"- {resource}")
    return "\n    ".join(changes) if changes else None


def summarize_doc_changes(old_docs, new_docs, is_new):
    items = []

    if is_new:
        items.append("First stable release — new docs published")
        cap_table = extract_capabilities_table(new_docs)
        if cap_table:
            rows = [r.strip() for r in cap_table.split("\n")[2:] if r.strip()]
            for row in rows:
                resource = row.split("|")[1].strip() if "|" in row else row
                items.append(f"  · {resource}")
        return items

    new_cap = extract_capabilities_table(new_docs)
    old_cap = extract_capabilities_table(old_docs)
    cap_diff = diff_capabilities(old_cap, new_cap)
    if cap_diff:
        items.append(f"Capabilities changed:\n    {cap_diff}")
    else:
        items.append("Capabilities: no changes")

    if old_docs and new_docs:
        old_len = len(old_docs)
        new_len = len(new_docs)
        delta = new_len - old_len
        if abs(delta) > 200:
            direction = "added" if delta > 0 else "removed"
            items.append(f"Content: ~{abs(delta):,} characters {direction}")

    return items


def format_slack_message(changes):
    today = date.today().strftime("%B %-d, %Y")
    count = len(changes)
    noun = "connector" if count == 1 else "connectors"

    blocks = [
        f"*Connector docs update — {today}*",
        f"*{count} {noun} promoted to stable.*",
        "—" * 20,
    ]

    for c in changes:
        version_line = (
            f"NEW: first stable release {c['new_version']}"
            if c["is_new"]
            else f"{c['old_version']} → {c['new_version']}"
        )
        blocks.append(f"\n*{c['display_name']}* (`{c['name']}` {version_line})")
        blocks.append(f":link: dist.conductorone.com/ConductorOne/{c['name']}/{c['new_version']}")
        blocks.append("")
        blocks.append("*What changed in the docs:*")
        for item in c["doc_changes"]:
            blocks.append(f"• {item}")

    return "\n".join(blocks)


def post_to_slack(message, webhook_url):
    payload = json.dumps({"text": message}).encode()
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return r.status


def load_snapshot():
    if SNAPSHOT_FILE.exists():
        data = json.loads(SNAPSHOT_FILE.read_text())
        return data.get("connectors", {})
    return {}


def save_snapshot(connectors):
    data = {
        "snapshotDate": date.today().isoformat(),
        "connectors": dict(sorted(connectors.items())),
    }
    SNAPSHOT_FILE.write_text(json.dumps(data, indent=2))


def main():
    token = get_token()

    print("Fetching catalog...", file=sys.stderr)
    current = fetch_catalog(token)
    previous = load_snapshot()

    changed = []
    for key, new_version in sorted(current.items()):
        old_version = previous.get(key, "")
        if new_version == old_version:
            continue

        org, name = key.split("/", 1)
        is_new = not old_version
        display_name = name.replace("baton-", "").replace("-", " ").title()

        print(f"  {key}: {old_version or '(none)'} → {new_version}", file=sys.stderr)
        new_docs = fetch_docs(org, name, new_version, token)
        old_docs = fetch_docs(org, name, old_version, token) if old_version else ""

        changed.append({
            "name": name,
            "display_name": display_name,
            "old_version": old_version,
            "new_version": new_version,
            "is_new": is_new,
            "doc_changes": summarize_doc_changes(old_docs, new_docs, is_new),
        })

    if not changed:
        print("No stable version changes since last snapshot.")
        save_snapshot(current)
        return

    message = format_slack_message(changed)
    print("\n--- DIGEST ---\n")
    print(message)

    if SLACK_WEBHOOK:
        print("\nPosting to Slack...", file=sys.stderr)
        post_to_slack(message, SLACK_WEBHOOK)
        print("Done.", file=sys.stderr)
    else:
        print("\n(Set SLACK_WEBHOOK_URL to post to Slack)", file=sys.stderr)

    save_snapshot(current)


if __name__ == "__main__":
    main()
