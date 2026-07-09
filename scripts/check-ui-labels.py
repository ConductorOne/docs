#!/usr/bin/env python3
"""
check-ui-labels.py

Extracts bolded text from product docs and checks whether each string
appears in the C1 frontend source. Flags labels that may have drifted.

Usage:
    python3 scripts/check-ui-labels.py [doc-path] --frontend /path/to/frontend

    doc-path    File or folder to check, relative to docs root.
                Defaults to product/ if omitted.

    --frontend  Path to the frontend source directory to search.
                Can also be set via the C1_FRONTEND_DIR environment variable.

Examples:
    C1_FRONTEND_DIR=~/code/c1/frontend python3 scripts/check-ui-labels.py
    python3 scripts/check-ui-labels.py product/how-to/ --frontend ~/code/c1/frontend
    python3 scripts/check-ui-labels.py product/how-to/create-requests.mdx --frontend ~/code/c1/frontend
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional, Tuple

DOCS_ROOT = Path(__file__).parent.parent
PRODUCT_DIR = DOCS_ROOT / "product"

FRONTEND_EXTENSIONS = {".tsx", ".ts", ".jsx", ".js", ".json"}

# Strings that are bolded for emphasis, not because they're UI labels.
SKIP_EXACT = {
    "done", "done.", "note", "tip", "warning", "important", "required",
    "optional", "new", "or", "and", "all", "yes", "no", "on", "off",
    "access",
}

# If the cleaned string starts with any of these, it's a sentence/instruction.
SKIP_STARTSWITH = (
    "if ", "use ", "do ", "can ", "need ", "tell ", "note:", "tip:",
    "before ", "looking ", "wait,", "done", "select ", "click ",
    "navigate ", "go to ", "in ", "on ", "when ", "while ", "after ",
)

# Trailing characters that mark instructions, not labels.
SKIP_ENDSWITH = (":", "?")

# If found in more than this many files, it's too generic to report confidently.
COMMON_THRESHOLD = 15

# Directories inside FRONTEND_DIR to skip (build output, node_modules, etc.)
SKIP_DIRS = {"node_modules", ".cache", "dist", "build", "__mocks__"}


def _build_frontend_index() -> list:
    """Walk the frontend directory once and return all searchable file paths."""
    paths = []
    for root, dirs, files in os.walk(FRONTEND_DIR):
        # Prune directories we don't want to descend into
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if Path(fname).suffix in FRONTEND_EXTENSIONS:
                paths.append(os.path.join(root, fname))
    return paths


def clean_bold(raw: str) -> str:
    """Strip markdown link syntax and surrounding punctuation from a bold string."""
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw)
    cleaned = cleaned.strip(" .,;")
    return cleaned


def extract_bold(text: str) -> list:
    """Extract all **bold** strings from markdown/mdx.

    Skips bold text that opens a list item (e.g. '- **Term**: explanation')
    since that pattern is used for emphasis/definition, not UI labels.
    """
    # Find positions where ** opens a bold that is the first thing in a list item.
    # Matches: optional indent, list marker (- * + or 1.), whitespace, then **
    list_lead_re = re.compile(r"^[ \t]*(?:[-*+]|\d+\.)\s+\*\*", re.MULTILINE)
    list_lead_positions = {m.end() - 2 for m in list_lead_re.finditer(text)}

    matches = []
    for m in re.finditer(r"\*\*([^*\n]+)\*\*", text):
        if m.start() in list_lead_positions:
            continue  # list lead-in, not a UI label
        raw = m.group(1).strip()
        cleaned = clean_bold(raw)
        if cleaned:
            matches.append(cleaned)
    return matches


def is_ui_label(text: str) -> bool:
    """Return True if this bold string is likely a UI label rather than emphasis."""
    if len(text) < 2:
        return False

    lower = text.lower()

    if lower in SKIP_EXACT:
        return False

    if lower.endswith(SKIP_ENDSWITH):
        return False

    if lower.startswith(SKIP_STARTSWITH):
        return False

    # Skip sentence-like strings starting with articles/pronouns
    if re.match(r"^(a|an|the|your|this|these|that)\s", lower):
        return False

    # Skip strings containing backticks — these are code/technical terms, not UI labels
    if "`" in text:
        return False

    return True


def search_files(term: str, file_paths: list) -> Tuple[str, int, Optional[str]]:
    """
    Search for term (case-insensitive) in the given file paths.
    Returns ("found"|"not_found"|"common", file_count, example_relative_path).
    """
    term_lower = term.lower()
    matched = []

    for path in file_paths:
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                if term_lower in f.read().lower():
                    matched.append(path)
                    # Stop early once we're past the common threshold
                    if len(matched) > COMMON_THRESHOLD:
                        return "common", len(matched), None
        except OSError:
            continue

    count = len(matched)
    if count == 0:
        return "not_found", 0, None

    rel = Path(matched[0]).relative_to(FRONTEND_DIR)
    return "found", count, str(rel)


def check_file(doc_path: Path, file_paths: list) -> dict:
    """Check one doc file. Returns result counts."""
    text = doc_path.read_text(encoding="utf-8")
    all_bold = extract_bold(text)

    # Deduplicate, preserving order
    seen = set()
    candidates = []
    for b in all_bold:
        key = b.lower()
        if is_ui_label(b) and key not in seen:
            seen.add(key)
            candidates.append(b)

    results = {"not_found": [], "found": [], "common": []}

    for label in candidates:
        status, count, detail = search_files(label, file_paths)
        if status == "not_found":
            results["not_found"].append(label)
        elif status == "found":
            results["found"].append((label, count, detail))
        else:
            results["common"].append((label, count))

    rel = doc_path.relative_to(DOCS_ROOT)
    print(f"\n{'─' * 64}")
    print(f"  {rel}")
    print(f"{'─' * 64}")

    if not candidates:
        print("  (no UI label candidates found)")
        return {k: len(v) for k, v in results.items()}

    if results["not_found"]:
        print(f"\n  NOT FOUND — may be renamed or removed ({len(results['not_found'])}):")
        for label in results["not_found"]:
            print(f"    ✗  {label!r}")

    if results["found"]:
        print(f"\n  Found in frontend ({len(results['found'])}):")
        for label, count, detail in results["found"]:
            files_str = f"{count} file{'s' if count != 1 else ''}"
            print(f"    ✓  {label!r}  ({files_str})  →  {detail}")

    if results["common"]:
        print(f"\n  Too generic to verify ({len(results['common'])}):")
        for label, count in results["common"]:
            print(f"    ~  {label!r}  (>{COMMON_THRESHOLD} files)")

    return {k: len(v) for k, v in results.items()}


def main():
    # Parse --frontend flag and positional doc-path argument
    args = sys.argv[1:]
    frontend_arg = None
    doc_arg = None

    i = 0
    while i < len(args):
        if args[i] == "--frontend" and i + 1 < len(args):
            frontend_arg = args[i + 1]
            i += 2
        elif not args[i].startswith("--"):
            doc_arg = args[i]
            i += 1
        else:
            i += 1

    # Resolve frontend directory: --frontend flag > env var > error
    frontend_env = os.environ.get("C1_FRONTEND_DIR")
    if frontend_arg:
        frontend_dir = Path(frontend_arg).expanduser().resolve()
    elif frontend_env:
        frontend_dir = Path(frontend_env).expanduser().resolve()
    else:
        print("Error: frontend directory required.")
        print("  Set C1_FRONTEND_DIR env var or pass --frontend /path/to/frontend")
        sys.exit(1)

    if not frontend_dir.is_dir():
        print(f"Error: frontend directory not found: {frontend_dir}")
        sys.exit(1)

    global FRONTEND_DIR
    FRONTEND_DIR = frontend_dir

    # Resolve doc target
    target = Path(doc_arg).resolve() if doc_arg else PRODUCT_DIR

    if not target.exists():
        target = (DOCS_ROOT / doc_arg).resolve()
    if not target.exists():
        print(f"Error: {target} not found")
        sys.exit(1)

    if target.is_file():
        files = [target]
    else:
        files = sorted(target.rglob("*.mdx")) + sorted(target.rglob("*.md"))
        files = [f for f in files if not any(p.startswith("_") for p in f.parts)]

    if not files:
        print(f"No .mdx or .md files found in {target}")
        sys.exit(1)

    print(f"Checking {len(files)} file(s) against {FRONTEND_DIR.name}/...")
    print("Indexing frontend source files...", end=" ", flush=True)
    frontend_files = _build_frontend_index()
    print(f"{len(frontend_files)} files indexed.")

    totals = {"not_found": 0, "found": 0, "common": 0}
    for doc in files:
        counts = check_file(doc, frontend_files)
        for k, v in counts.items():
            totals[k] += v

    print(f"\n{'═' * 64}")
    print(f"  Summary: {len(files)} file(s) checked")
    print(f"    ✗  Not found:   {totals['not_found']}  ← review these")
    print(f"    ✓  Found:       {totals['found']}")
    print(f"    ~  Too generic: {totals['common']}  ← skipped, too common to verify")
    print(f"{'═' * 64}\n")


if __name__ == "__main__":
    main()
