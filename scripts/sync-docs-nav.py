#!/usr/bin/env python3
"""Sync docs.json navigation to include all baton/*.mdx connector pages.

Reads the baton/ directory and ensures every connector MDX file has a
corresponding entry in docs.json's "Pre-built connectors" navigation group.

Usage:
    python scripts/sync-docs-nav.py          # dry-run (default)
    python scripts/sync-docs-nav.py --write  # apply changes
"""

import json
import sys
from pathlib import Path

# Pages in baton/ that are NOT individual connector docs.
# These appear in other navigation groups (Welcome, Deploy, etc.).
NON_CONNECTOR_STEMS = {
    "intro",
    "_release-notes",
    "faq",
    "migration",
    "capabilities",
    "configure",
    "manage-connector",
    "deploy",
    "health-checks",
    "file-connectors",
    "baton-sql",
    "baton-scim",
}


def find_prebuilt_group(docs: dict) -> list | None:
    """Navigate docs.json structure to find the Pre-built connectors pages list."""
    # docs.json uses Mintlify's tab-based navigation.
    # Structure: tabs[] -> tab with pages[] -> group "Pre-built connectors" -> pages[]
    tabs = docs.get("tabs", [])
    if not tabs:
        # Try alternative structure
        tabs = docs.get("navigation", [])

    for tab in tabs:
        if not isinstance(tab, dict):
            continue
        # Look for Connectors tab
        if tab.get("tab") != "Connectors":
            continue
        for group in tab.get("pages", []):
            if not isinstance(group, dict):
                continue
            if group.get("group") == "Pre-built connectors":
                return group["pages"]

    return None


def main():
    write_mode = "--write" in sys.argv

    docs_root = Path(__file__).resolve().parent.parent
    baton_dir = docs_root / "baton"
    docs_json_path = docs_root / "docs.json"

    if not baton_dir.exists():
        print(f"Error: {baton_dir} not found", file=sys.stderr)
        sys.exit(1)

    if not docs_json_path.exists():
        print(f"Error: {docs_json_path} not found", file=sys.stderr)
        sys.exit(1)

    # Collect connector MDX files
    connector_pages = sorted(
        f"baton/{p.stem}"
        for p in baton_dir.glob("*.mdx")
        if p.stem not in NON_CONNECTOR_STEMS
        and not p.stem.startswith("v1")
    )

    # Read docs.json
    with open(docs_json_path) as f:
        docs = json.load(f)

    prebuilt_pages = find_prebuilt_group(docs)
    if prebuilt_pages is None:
        print("Error: could not find 'Pre-built connectors' group in docs.json", file=sys.stderr)
        sys.exit(1)

    existing = set(prebuilt_pages)
    to_add = [p for p in connector_pages if p not in existing]
    orphaned = [p for p in prebuilt_pages if p not in connector_pages]

    if not to_add and not orphaned:
        print(f"Navigation is in sync. {len(connector_pages)} connector pages, all present in docs.json.")
        return

    if to_add:
        print(f"Pages to add ({len(to_add)}):")
        for p in to_add:
            print(f"  + {p}")

    if orphaned:
        print(f"\nPages in docs.json but no MDX file ({len(orphaned)}):")
        for p in orphaned:
            print(f"  ? {p}")

    if not write_mode:
        print("\nDry run. Use --write to apply changes.")
        return

    # Add missing pages and sort
    updated = sorted(set(prebuilt_pages) | set(to_add))
    prebuilt_pages.clear()
    prebuilt_pages.extend(updated)

    with open(docs_json_path, "w") as f:
        json.dump(docs, f, indent=2)
        f.write("\n")

    print(f"\nUpdated docs.json: added {len(to_add)} pages. Total: {len(updated)}.")


if __name__ == "__main__":
    main()
