---
name: c1-docs-writer
description: Write documentation for C1's website following established voice, tone, and style guidelines. Use when creating new documentation pages, updating existing docs, writing how-to guides, or any content for conductorone.com/docs. Ensures consistency with C1's direct, action-oriented documentation style.
---

# C1 Documentation Writer

Write C1 documentation that matches the established voice, tone, and style of the existing docs site.

## When to Use This Skill

Use this skill when:
- Creating new documentation pages for C1
- Writing or updating how-to guides
- Drafting admin guides or end-user documentation
- Creating quickstart guides
- Writing any content intended for conductorone.com/docs

## The docs voice

Documentation has a different job than marketing. Marketing makes a case for C1. Docs assume the reader already chose C1 — they're here to get something done. The voice shifts accordingly: less energetic, more instructive.

**Outside-in framing.** Lead with what the reader is trying to accomplish, not with the feature name or how it works internally. "If you run recurring campaigns, use a template to avoid reconfiguring from scratch each time" is outside-in. "Campaign templates are a feature that allows..." is not. The opening sentence of every page should tell the reader what they can *do* after reading it — not what the feature *is*.

**Declarative, not hedged.** If something is true, say it plainly. Don't write "C1 can help streamline the approval process." Write "C1 auto-approves requests that meet policy." Hedging makes docs feel uncertain; readers lose confidence in the product.

**Peer-level respect.** The reader is a security or IT professional. They know why access reviews matter. They need to know how to run one. Skip context they already have and get to the task.

**Empathy means anticipating friction, not cheerfulness.** Acknowledge what's complex. Offer the shortcut when one exists. Write the "why" for non-obvious steps. Don't celebrate task completion ("That's it!", "You're done!", "You're all set!") — state the outcome instead. The outcome sentence is the reward.

- Do: "New tasks will now be automatically reassigned to your delegate."
- Don't: "That's it! Tasks will now be assigned to your delegate."

**Active voice, specific verbs.** "C1 sends a notification" not "a notification is sent." "Click **Save**" not "the Save button should be clicked."

**Avoid hedging verbs.** These drain sentences of authority:
- "helps you to" → use a direct verb
- "can help" → state what it does
- "is designed to" → state what it does
- "allows you to" → "lets you" or just state the action

**No editorializing.** Cut "it's important to note," "it's worth mentioning," "please note," and "from a security perspective." If the information belongs in the doc, put it in the doc without announcing it.

**No promotional language.** "Powerful," "robust," "seamless," "innovative" — cut them. Let the capability speak for itself.

## File Format

**Always use .mdx format** for C1 documentation files. MDX (Markdown with JSX) is the required format for the docs site. When creating new documentation, save files with the `.mdx` extension.

### Content Structure

- All docs are MDX files with YAML frontmatter
- Required frontmatter: `title`, `description`
- Optional: `og:title`, `og:description`, `sidebarTitle`
- Add editor refresh comment: `{/* Editor Refresh: YYYY-MM-DD */}`

## File and Folder Structure

C1 docs use Mintlify, where **file path = URL**. Structure decisions are permanent without redirects, so be intentional.

### Folder rules

- **Flat by default**: Single pages live directly under their section folder — `/admin/page-name`, not `/admin/subsection/page-name`.
- **Add a subfolder when**: A section has three or more related pages that form a coherent group. At that threshold, a subfolder improves navigation in both the repo and the published URLs.
- **Name folders after the primary UI term**: Use the exact term as it appears in the product interface. If the UI says "Service principals," the folder is `service-principals`.

### What not to do

- Don't create a subfolder for a single page.
- Don't invent folder names that don't match UI terminology.
- Don't add folder layers to mirror internal team structures or product roadmap groupings — organize for users, not for the company.

### docs.json

Sidebar grouping in `docs.json` is independent of folder structure. You can visually group pages in the nav without creating subfolders, which is useful when a section is growing but hasn't reached the three-page threshold yet.

## Writing Process

1. **Identify the audience.** Admin, end-user, or developer? Admins configure; end-users request and review; developers integrate and extend. The terminology, assumed knowledge, and task framing differ significantly.

2. **Identify what the reader is trying to accomplish.** This is your outside-in anchor — write it down before drafting. If you can't state it in one sentence, clarify before writing.

3. **Structure the content**:
   - Open with a one-sentence description that is action-led, not feature-led
   - Include a conceptual "What is X?" section only if the feature is genuinely non-obvious or has meaningful prerequisites
   - Use H2 headings for major sections, H3 for subsections
   - Break procedures into numbered steps, each starting with an action verb
   - Put prerequisites before steps, not buried in step 3

4. **Write, then tighten.** First pass for completeness. Second pass to cut every word that isn't doing work.

5. **Self-check before finishing**:
   - Does the opening sentence tell the reader what they can do after reading this — not what the feature is?
   - Is every step action-led?
   - Are there any hedging verbs, editorializing phrases, or throat-clearing openers?
   - Does any sentence try to serve too many stakeholders at once? Split it or cut it.
   - After each procedure, is there an outcome sentence stating what changed?
   - Is the company name "C1" throughout?

## Key Style Points

**Quick reference** (full details in `references/style-guide.md`):

- **Voice**: Second person ("you"), active voice, direct language
- **Tone**: Technical, precise, no marketing speak or promotional language
- **Headings**: Sentence case only ("Getting started" not "Getting Started"); always include explanatory text after a heading before any subheadings; headings must be descriptive enough to make sense out of context — a reader should understand the section's scope without seeing the rest of the page. For example, "FAQ" is too vague; "Frequently asked questions about automations" is correct. "Related" is too vague; "Features related to automations" is correct.
- **Procedures**: Numbered steps starting with action verbs. One action per step — don't bundle two actions into one step unless they're truly inseparable. A `<Steps>` block must always be preceded by at least one sentence of intro text — never place `<Steps>` directly after a heading. Navigation to a page and clicking Save are steps, not intro prose.
- **Outcome sentences**: After a procedure, state what changed as a plain sentence ("New tasks will now be automatically reassigned to your delegate."). Don't celebrate ("That's it!", "Done.", "You're all set!") — state the outcome instead.
- **Optional steps**: Start with **Optional.** (e.g., "**Optional.** Configure advanced settings...")
- **Callouts**: Start with context, not with the callout type. Don't write "Note that..." inside a `<Note>` or "Warning:" inside a `<Warning>` — the component signals that already. `<Warning>` is for destructive or irreversible actions only; `<Tip>` for helpful shortcuts or best practices; `<Note>` for context that applies in specific situations.
- **Optional sections**: Use `## Optional: Section name` for entire optional tasks or sections
- **UI elements**: Bold formatting (**New profile**)
- **Navigation paths**: **Admin** > **Access profiles** > **New profile**
- **Terminology**: Use product-specific terms consistently (access profile, entitlement, campaign)
- **Clarity**: Be specific, cite sources, avoid vague claims
- **Simplicity**: Keep examples practical, avoid excessive options

## Technical Standards

- Add language tags to all code blocks
- For CEL expressions, use `go` as the language tag (CEL isn't recognized for syntax highlighting)
- Use root-relative paths for internal links — start from the site root, never include `/docs/` in the path. The site is served from `/`, so the correct form is `/product/admin/campaigns`, not `/docs/product/admin/campaigns`. Including `/docs/` produces a `/docs/docs/` double-prefix that 404s.
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

## FAQ Sections

When a page includes a FAQ section, always use `<AccordionGroup>` with individual `<Accordion>` components — one per question. This improves search quality and keeps pages visually clean and interactive.

**Section heading**: Always be explicit about what the FAQ covers. Use the format "Frequently asked questions about [topic]" rather than just "FAQ". This improves search quality and sets clear expectations.

```mdx
## Frequently asked questions about [topic]

<AccordionGroup>
  <Accordion title="Question goes here?">
    Answer goes here.
  </Accordion>

  <Accordion title="Another question?">
    Another answer.
  </Accordion>
</AccordionGroup>
```

**Key points:**
- Write questions in the first or second person as a user would ask them ("Can I...", "What happens when...", "How do I...")
- Keep answers concise — accordion format encourages brevity
- Order questions from most common or fundamental to more specific

## Early Access Notes

When documenting features that are in early access, add a standardized warning callout at the top of the page (after the frontmatter and any editor refresh comment):

```mdx
<Warning>
**Early access.** This feature is in early access, which means it's undergoing ongoing testing and development while we gather feedback, validate functionality, and improve outputs. Contact the C1 Support team if you'd like to try it out or share feedback.
</Warning>
```

**Key points:**
- Always use `<Warning>` (not `<Info>` or `<Note>`)
- Always use "the C1 Support team" (not "our Support team" or "your account team")
- Don't name the specific feature (use "This feature")
- Include the explanation of what early access means
- Use "share feedback" (not "have any feedback")

## Navigation (docs.json)

- Pages map to MDX files (no extension)
- Groups organize sidebar sections
- Tabs create distinct URL paths
- Anchors for persistent sidebar links
- Avoid `/api` and `/mcp` as root paths (reserved)

## Product name

Always use **C1** to refer to the product and company in prose. Do not use "ConductorOne" in new documentation.

**Marketing website:** The marketing website is **c1.ai** — use this for any links to the public marketing site. Do not use `conductorone.com` for marketing links.

**Exceptions — never change these to C1:**

| What | Examples |
| :--- | :--- |
| Product and tenant URLs | `conductor.one`, tenant URLs like `example.conductor.one` |
| File and directory paths generated by tools | `~/.conductorone/config.yaml` |
| Code identifiers | Environment variables (`CONDUCTORONE_CLIENT_ID`), package names, binary names |
| GitHub organization in URLs | `github.com/ConductorOne/...` |

When in doubt: if a user would type it into a terminal or config file, leave it as-is.

## Common Mistakes to Avoid

- **Hedging verbs**: "helps you to," "can help," "is designed to," "allows you to" — use direct verbs instead ("lets you," "C1 does X")
- **Feature-first openers**: "Campaign templates are a feature that allows..." → lead with what the reader can do instead
- **Celebrating task completion**: "That's it!", "Done.", "You're all set!" → state the outcome
- **Multi-clause sentences serving too many stakeholders at once** — split or cut
- **Editorializing**: "it's important to note," "it's worth mentioning," "please note"
- **Promotional language**: "powerful," "robust," "seamless," "innovative"
- **Excessive conjunctions**: "moreover," "furthermore," "additionally"
- **Using "ConductorOne"** instead of "C1" in prose
- **Using "bool"** — use "Boolean"
- **Title case in headings** — sentence case only
- **Context-free headings** like "FAQ" or "Related" — always include the subject ("Frequently asked questions about automations")
- **Latin abbreviations** (i.e., e.g., etc.) — use "for example", "that is", "and so on"
- **Placing `<Steps>` directly after a heading** with no intro sentence
- **Putting navigation instructions in intro prose** instead of as steps
- **Duplicate content** — update an existing page instead of creating a new one
