# C1 as an MCP Gateway

ConductorOne (C1) is an MCP gateway. An AI client connects to one C1 MCP endpoint, and C1 sits in front of the organization's approved MCP servers and integrations. Agents do not connect to those upstream servers directly.

Mental model: **one MCP connection, many governed systems behind it.**

## What the Gateway Does on Every Call

1. **Authenticates the caller.** C1 resolves the human or workload identity behind the agent. Every tool call carries that identity — the gateway is identity-aware, not an anonymous relay.
2. **Checks governance.** The tool must be **Enabled** by an admin, and the caller must hold a **grant** for it. Both conditions are required. Enabling a tool does not grant it to anyone.
3. **Runs hooks.** Admin-configured pre-tool-use hooks may rewrite the input or deny the call.
4. **Routes upstream.** C1 forwards the call to the correct upstream server using that server's configured auth mode, so the agent never handles upstream credentials.
5. **Runs post hooks.** Post-tool-use hooks may rewrite, redact, or deny the returned output.
6. **Writes an audit log entry** with identity, client, server, tool, result, denial reason, and latency.

## Upstream Server Types

The agent cannot tell these apart and does not need to. All appear as tools behind the same endpoint.

| Upstream | What it is |
|----------|------------|
| Hosted catalog server | An MCP server C1 hosts and registers on the org's behalf |
| Vendor MCP server | A third-party MCP server registered by an admin |
| Bridged server | A private or on-premises MCP server reached through C1's MCP bridge |

## Toolsets, Access Profiles, and Grants

- A **tool** is one capability exposed by an upstream MCP server (for example, `github_create_issue`).
- Discovered tools start in an unreviewed state. An admin approves/enables them and may classify them by action (read / write / delete) and risk.
- Approved tools are bundled into a **toolset** — either C1-maintained ("All approved", "Read-only") or an admin-curated custom toolset.
- A toolset is bound to an **access profile**, which carries the approval policy, approvers, and expiry.
- A user requests the access profile from the C1 catalog (web, Slack, or from their AI client). Once approved, the grant makes the toolset's tools callable by that user's clients.

Consequence for agents: the tool surface is per-caller, not per-tenant. Two agents connected to the same gateway can see and call different sets of tools.

## Tool-Call Hooks

Admins can attach hooks that fire on every governed call:

- **Pre-tool-use** — inspect or rewrite input, or deny the call.
- **Post-tool-use** — inspect or rewrite output, or deny the response.

Hooks run in priority order, can stack, can be scoped to specific tools by expression, and are **fail-closed**: a hook that errors or times out causes the call to be denied.

Built-in patterns include PII field redaction, credit-card blocking, capping numeric input fields such as `limit` and `page_size`, denying writes by classification or outside business hours, and blocking references to sensitive file paths.

Consequence for agents: a call can be denied by policy, or return output that has been redacted, truncated, or capped below the requested size. That is governance working, not a malfunction. Do not retry with the same input hoping for a different result, and do not attempt to work around a cap by fanning out many smaller calls.

## Kill Switches

Admins can immediately block calls regardless of grants, at tenant, server, tool, or client level. A client kill switch revokes the client's tokens and forces re-authentication. A tool kill switch blocks that tool for everyone. These take effect mid-session.

## Client Types

Each registered AI client is classified — **personal**, **shared**, **service**, or **ephemeral** — and the tenant controls which types may register at all. Individual tools can be restricted to a subset of types. Clients also move through lifecycle states (active → hidden → closed → deleted) based on inactivity; a closed client must re-authenticate.

## Code Mode vs Directly Named Tools

The gateway exposes its tool surface in one of two shapes.

| Shape | What the agent sees | When |
|-------|---------------------|------|
| **Code mode** | Discovery and execution entrypoints — `describe` and `execute` — instead of one named tool per upstream tool | Default for interactive, human-backed clients. Code mode is a tenant-level AI governance setting, on by default |
| **Directly named tools** | Each enabled tool listed individually in the client's tool list | When the tenant setting is off, and for **Service** and **Ephemeral** client types |

In code mode, upstream tools do not appear one by one in the client's tool list. That is expected, not a discovery failure. The agent calls `describe` to find the tools it needs, then invokes them by writing a short TypeScript program passed to `execute`.

Governance is identical in both shapes. Code mode changes the calling interface, not the checks: every underlying call still requires the tool to be Enabled and the caller to hold a grant, still runs hooks, and is still audit logged.

## Denials Are Structured, Not Opaque

When the caller lacks access to a tool, the gateway does not fail with a generic error. It returns a structured envelope:

- `{status: 'request_created', tool, task_id, task_number, task_url, entitlement_id}` — the tool is requestable. C1 opened an access request; the upstream API was **not** called. Once the request is approved, the same call executes.
- `{status: 'denied', reason}` — no access path exists for this caller.

This is the gateway's signature behavior and the thing agents most often misread. A `request_created` result is not a failure and not an empty result set — it means a request was filed and the human needs the task link.

Correct agent behavior: check for these envelopes before touching any domain field, hand the user the `task_url`, and stop that line of work until approval. Never retry in the same program, and never coerce the envelope into a default value such as an empty list.

## Two Governance Paths, One Platform

C1 governs MCP access two ways. The gateway path (this document) proxies the agent's tool calls through C1. In **enterprise-managed authorization**, C1 instead issues a short-lived scoped token and the agent calls the MCP server directly. Code mode, `describe`/`execute`, and access-request envelopes belong to the gateway path only.

## Also in This Domain

- Writing programs for `execute`: `use-code-mode.md`
- Handling access-request envelopes: `use-access-requests.md`
- Polling long-running executions: `use-async-executions.md`
