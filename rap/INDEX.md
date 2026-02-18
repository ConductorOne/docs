# ConductorOne RAP Documentation

Retrieval Augmented Prompt (RAP) documentation for AI agents. Each subdirectory contains focused, self-contained documentation chunks optimized for selective retrieval.

## How to Use

1. Identify the user's question domain
2. Navigate to the relevant subdirectory
3. Read that subdirectory's INDEX.md for detailed retrieval guidance
4. Retrieve 1-3 relevant files based on the question
5. Answer using the retrieved content

## Available Knowledge Domains

| Domain | Path | Use for |
|--------|------|---------|
| **Connectors** | `connectors/INDEX.md` | Building Baton connectors, sync/provision patterns, SDK interfaces |
| **Service Principals** | `service-principals/INDEX.md` | API automation, client credentials, workload federation, CI/CD integration |
| **CEL Expressions** | `cel-expressions/index.md` | Writing CEL in policies, dynamic groups, automations, access reviews |

## Quick Routing Guide

**User asks about building integrations:**
→ `connectors/INDEX.md`

**User asks about API authentication, service accounts, CI/CD:**
→ `service-principals/INDEX.md`

**User asks about expressions, policies, dynamic groups, automation conditions:**
→ `cel-expressions/index.md`

## Subdirectory Structure

Each subdirectory follows the same pattern:
- `INDEX.md` or `index.md` - Detailed retrieval guide for that domain
- Topic-specific `.md` files - Self-contained, focused documentation chunks
- Files are under 500 lines, typically 100-300 lines
- Each file is understandable without reading other files
