---
name: c1-docs-writer
description: Write documentation for ConductorOne's website following established voice, tone, and style guidelines. Use when creating new documentation pages, updating existing docs, writing how-to guides, or any content for conductorone.com/docs. Ensures consistency with ConductorOne's direct, action-oriented documentation style.
---

# ConductorOne Documentation Writer

Write ConductorOne documentation that matches the established voice, tone, and style of the existing docs site.

## When to Use This Skill

Use this skill when:
- Creating new documentation pages for ConductorOne
- Writing or updating how-to guides
- Drafting admin guides or end-user documentation
- Creating quickstart guides
- Writing any content intended for conductorone.com/docs

## File Format

**Always use .mdx format** for ConductorOne documentation files. MDX (Markdown with JSX) is the required format for the docs site. When creating new documentation, save files with the `.mdx` extension.

### Content Structure

- All docs are MDX files with YAML frontmatter
- Required frontmatter: `title`, `description`
- Optional: `og:title`, `og:description`, `sidebarTitle`
- Add editor refresh comment: `{/* Editor Refresh: YYYY-MM-DD */}`

## Writing Process

Follow this process when creating ConductorOne documentation:

1. **Read the style guide first**: Always start by reading `references/style-guide.md` to refresh on the voice, tone, and formatting conventions.

2. **Understand the purpose**: Clarify with the user what the documentation should accomplish:
   - What feature or task does it cover?
   - Who is the audience (admin, end-user, developer)?
   - What should readers be able to do after reading?

3. **Structure the content**:
   - Start with a clear one-sentence description of the feature/page
   - Use descriptive H2 headings for major sections
   - Break procedures into numbered steps
   - Include a "What's [feature name]?" section if conceptual explanation is needed

4. **Write in ConductorOne's voice**:
   - Direct and helpful, like a knowledgeable colleague
   - Action-oriented, focused on what users need to do
   - Use "you" and "your" to address readers
   - Use contractions naturally (you'll, don't, can't)

5. **Apply formatting conventions**:
   - Bold UI elements: **Admin** > **Access profiles**
   - Use sentence case for headings
   - Start callouts with context: "Want to..." or "Tips for..."
   - Make link text descriptive

6. **Review against the style guide**: Before finalizing, check that the content follows all style guide conventions.

## Key Style Points

**Quick reference** (full details in `references/style-guide.md`):

- **Voice**: Second person ("you"), active voice, direct language
- **Tone**: Technical, precise, no marketing speak or promotional language
- **Headings**: Sentence case only ("Getting started" not "Getting Started")
- **Procedures**: Numbered steps starting with action verbs
- **UI elements**: Bold formatting (**New profile**)
- **Navigation paths**: **Admin** > **Access profiles** > **New profile**
- **Terminology**: Use product-specific terms consistently (access profile, entitlement, campaign)
- **Clarity**: Be specific, cite sources, avoid vague claims
- **Simplicity**: Keep examples practical, avoid excessive options

## Technical Standards

- Add language tags to all code blocks
- Use relative paths for internal links
- Include alt text on all images
- List prerequisites at the start of procedural content
- Use precise version numbers and specifications
- Maintain consistent terminology throughout

## Mintlify Components

### Layout Components

```mdx
<Columns cols={2}>
  <Card title="Title" icon="icon-name" href="/path" />
</Columns>

<Tabs>
  <Tab title="Tab Name">Content</Tab>
</Tabs>

<Frame>
  <img src="/images/path.png" alt="Description"/>
</Frame>
```

### Content Components

```mdx
<Tip>Helpful information</Tip>
<Warning>Important warning</Warning>
<Note>Additional context</Note>
<Info>General information</Info>

<Accordion title="Expandable section">
  Hidden content
</Accordion>

<Steps>
  <Step></Step>
  <Step></Step>
</Steps>
```

### Icons

- Use Lucide icon library
- Common icons: `book-open`, `code`, `terminal`, `rocket`, `shield-check`, `user-check`
- Format: `<Icon icon="icon-name" size={24} />`

## Component Patterns

- **Cards**: Start with action verbs ("Create", "Set up", "Configure")
- **Property descriptions**: End with periods, use proper technical terms
- **Code examples**: Simple, practical, tested before inclusion
- **Links**: Verify all external links work

## Navigation (docs.json)

- Pages map to MDX files (no extension)
- Groups organize sidebar sections
- Tabs create distinct URL paths
- Anchors for persistent sidebar links
- Avoid `/api` and `/mcp` as root paths (reserved)

## Common Mistakes to Avoid

- Don't use "bool" (use "Boolean")
- Don't use promotional language ("amazing", "powerful" unless justified)
- Don't use excessive conjunctions ("moreover", "furthermore")
- Don't editorialize ("it's important to note")
- Don't create duplicate content (update existing docs instead)
- Don't use title case for headings

## Reference Material

- **references/style-guide.md** - Complete style guide covering voice, tone, language, structure, and common patterns. Read this before writing any documentation.
