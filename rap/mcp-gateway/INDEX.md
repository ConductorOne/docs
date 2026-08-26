# MCP Gateway Documentation Index

Documentation for interacting with ConductorOne (C1) as an MCP gateway, and for the code-mode interface agents use to call governed tools through it. Request relevant sections based on the user's question.

C1 is an MCP gateway: an AI client connects to one C1 MCP endpoint, and C1 sits in front of the organization's approved MCP servers. Agents do not connect to those upstream servers directly. Every call is identity-aware, governed per tool, and audit logged.

## How to Use

1. Read the user's question
2. Identify relevant sections (up to 3)
3. Request those files
4. Answer using retrieved content

## Available Sections

| Section | File | Covers |
|---------|------|--------|
| Gateway model and governance | `concepts-gateway.md` | Single endpoint, identity-aware calls, Enabled + grant checks, toolsets and access profiles, hooks, kill switches, audit, client types, code mode vs directly named tools |
| Code mode contract | `use-code-mode.md` | `describe` and `execute`, `source_code`/`args` input shape, program shape, single-program principle, sequential vs `Promise.all` vs pagination, robustness rules, anti-patterns |
| Access-request envelopes | `use-access-requests.md` | `request_created` and `denied` results, checking status before domain fields, agent behavior after each, hook denials and modified output, how a caller gets access |
| Async executions | `use-async-executions.md` | `pending` responses, `execution_id`, `get_execution`, statuses, exponential backoff, 25s window and 15-minute cap |

---

## Selection Guidelines

**"What is..."**
- C1 MCP / the C1 gateway / C1 MCP URL -> `concepts-gateway.md`
- Code mode -> `concepts-gateway.md`, `use-code-mode.md`
- `describe` / `execute` -> `use-code-mode.md`
- `get_execution` -> `use-async-executions.md`
- A toolset / access profile / grant -> `concepts-gateway.md`
- A tool-call hook -> `concepts-gateway.md`

**"How do I..."**
- Write a program for `execute` -> `use-code-mode.md`
- Call a tool through the gateway -> `use-code-mode.md`
- Paginate a large result set -> `use-code-mode.md`
- Run independent lookups in parallel -> `use-code-mode.md`
- Get access to a tool I was denied -> `use-access-requests.md`
- Wait for a long-running program -> `use-async-executions.md`

**Agent hit an unexpected result**
- `{status: 'request_created', ...}` -> `use-access-requests.md`
- `{status: 'denied', reason}` -> `use-access-requests.md`
- `{status: 'pending', execution_id}` -> `use-async-executions.md`
- Access denied / tool not in tool list -> `use-access-requests.md`
- Result fields missing, redacted, or capped below the requested limit -> `concepts-gateway.md`, `use-access-requests.md`
- `main` rejected for returning an array, string, or number -> `use-code-mode.md`
- `input.<key>` is `undefined` inside the program -> `use-code-mode.md`
- Import of a module other than `@c1/code-mode` failed -> `use-code-mode.md`

**Expected tools are missing from the client's tool list**
- Only `describe` and `execute` are listed -> `use-code-mode.md`, `concepts-gateway.md`
- Tools listed individually instead of code mode -> `concepts-gateway.md`
- A specific tool is absent entirely -> `use-access-requests.md`, `concepts-gateway.md`

**Governance questions**
- Why a call was blocked -> `concepts-gateway.md`, `use-access-requests.md`
- What C1 logs per call -> `concepts-gateway.md`
- Which client types get code mode -> `concepts-gateway.md`

---

## Usage Examples

User: "My agent only sees `describe` and `execute` — where did my tools go?"
Retrieve: `use-code-mode.md`, `concepts-gateway.md`

User: "Write a program that lists all users and their groups"
Retrieve: `use-code-mode.md`

User: "The tool returned `request_created` with a task_url — what now?"
Retrieve: `use-access-requests.md`

User: "execute came back pending with an execution_id"
Retrieve: `use-async-executions.md`

User: "How does C1 decide whether my agent can call a tool?"
Retrieve: `concepts-gateway.md`

User: "The result came back with the salary field redacted"
Retrieve: `concepts-gateway.md`, `use-access-requests.md`

User: "How do I request access to a governed MCP tool?"
Retrieve: `use-access-requests.md`
