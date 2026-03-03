---
name: rap-documentation
description: Create RAP (Retrieval Augmented Prompt) documentation - agent-optimized, chunked documentation for selective retrieval by LLM agents. Use when documentation exceeds context windows, when creating agent-facing docs, or when asked about "rap", "agent docs", or chunked documentation.
---

# Retrieval Augmented Prompt (RAP) Documentation

For AI agent consumption, create a parallel `rap/` directory with chunked, self-contained skill files optimized for selective retrieval.

## Why RAP Documentation

Full documentation may exceed context windows. RAP format allows agents to:
1. Read a small index describing available sections
2. Select relevant sections based on user query
3. Retrieve only what's needed
4. Answer with focused context

## Structure

RAP documentation lives in a unified `rap/` directory with subdirectories for each knowledge domain:

```
rap/
  INDEX.md                   # Master index routing to subdomains
  connectors/                # Baton connector development
    INDEX.md                 # Domain-specific retrieval guide
    concepts-overview.md
    build-setup.md
    ...
  service-principals/        # API automation, workload federation
    INDEX.md
    concepts-overview.md
    auth-client-credentials.md
    ...
  cel-expressions/           # CEL in policies, groups, automations
    index.md
    env-policy-conditions.md
    functions-directory.md
    ...
```

**When to use subdirectories:**
- Each subdirectory represents a distinct knowledge domain
- Create a new subdirectory when adding RAP docs for a major feature area
- Each subdirectory has its own INDEX.md with domain-specific retrieval guidance

**Master INDEX.md** routes LLMs to the correct subdomain:

```markdown
| Domain | Path | Use for |
|--------|------|---------|
| Connectors | `connectors/INDEX.md` | Building Baton connectors |
| Service Principals | `service-principals/INDEX.md` | API automation |
| CEL Expressions | `cel-expressions/index.md` | Writing CEL expressions |
```

## INDEX.md Requirements

The index is always loaded. It must:

1. **Describe each section concisely** - What it covers in one line
2. **Provide file names** - So agent knows what to request
3. **Include selection guidelines** - Map query patterns to relevant files
4. **Show usage examples** - Demonstrate retrieval for common questions

**Example INDEX structure:**

```markdown
## Available Sections

| Section | File | Covers |
|---------|------|--------|
| What connectors do | `concepts-overview.md` | Problem solved, sync vs provision |
| Resource model | `concepts-resources.md` | Resources, entitlements, grants |

## Selection Guidelines

**User asks "how do I..."**
- Build a connector -> `build-setup.md`, `build-syncer.md`
- Debug a problem -> `debug-workflow.md`, `debug-errors.md`

**User shows code with errors**
- Look at error message -> `debug-errors.md`
```

## Skill File Requirements

Each skill file must be:

1. **Self-contained** - Understandable without other files
2. **Focused** - One topic, not comprehensive overview
3. **Actionable** - Code examples, concrete patterns
4. **Concise** - 100-300 lines typical, under 500 max

**Naming convention:** `category-topic.md`
- `concepts-*` - Conceptual understanding
- `build-*` - Building/implementation
- `provision-*` - Provisioning operations
- `meta-*` - Meta-connector configuration
- `ops-*` - Operations/deployment
- `debug-*` - Debugging/troubleshooting
- `ref-*` - Reference material

## Tone for RAP Files

RAP files target LLM agents, not humans. Write differently than human-facing docs:

**Do:**
- Be direct and terse - agents don't need warmth or encouragement
- Front-load the most important information
- Use consistent structure across files (agents pattern-match)
- Include precise technical details (types, signatures, exact flags)
- State facts without hedging

**Don't:**
- Add marketing language or enthusiasm
- Use rhetorical questions (agents don't need engagement hooks)
- Include "why this matters" context (agents retrieve based on query, not motivation)
- Soften with "you might want to" or "consider" - just state the pattern

**Example contrast:**

Human docs: "The Baton connector framework solves this elegantly: you write one integration, and ConductorOne handles the rest."

RAP docs: "A connector translates access data from any system into ConductorOne's common format."

The human version has warmth and sells the benefit. The RAP version states the fact. Both are correct; they serve different audiences.

## Creating RAP from Full Docs

1. **Identify discrete topics** - Each should answer a specific class of questions
2. **Extract and simplify** - Pull content, remove cross-references to other sections
3. **Add context** - Each file should open with a one-line description of what it covers
4. **Verify independence** - Can this file be understood alone?
5. **Strip human-targeted tone** - Remove warmth, marketing, rhetorical questions

## When to Create RAP Version

Create `rap/` when:
- Documentation will be used by AI agents
- Full docs exceed typical context windows (>50k tokens)
- Users will have varied, specific questions (not reading cover-to-cover)

Don't create when:
- Docs are short enough to fit in context entirely
- Content is inherently linear (must be read in order)
- Target audience is humans only

## The Breadcrumb Pattern

Add a comment at the bottom of the main human-readable doc pointing LLMs to the RAP index. Point to the specific subdirectory index, not the master index.

**For MDX files** (Mintlify, Docusaurus, etc.) - use JSX comment syntax:

```jsx
{/*
LLM Note: For AI assistants answering questions about Baton connector development,
a structured knowledge base is available at rap/connectors/INDEX.md
with focused, retrievable documentation chunks.
*/}
```

```jsx
{/*
LLM Note: For AI assistants answering questions about service principals and workload federation,
a structured knowledge base is available at rap/service-principals/INDEX.md
with focused, retrievable documentation chunks.
*/}
```

**For plain Markdown/HTML** - use HTML comment syntax:

```html
<!--
LLM Note: For AI assistants answering questions about CEL expressions in ConductorOne,
a structured knowledge base is available at rap/cel-expressions/index.md
with focused, retrievable documentation chunks.
-->
```

MDX parsers reject HTML comments (`<!-- -->`). Always check file extension: `.mdx` requires `{/* */}`.

This works because:
- Comments don't render for human readers
- LLMs processing the page see the comment
- Crawling LLMs can discover and fetch the structured index
- The index then guides retrieval of specific chunks
