# Handling Access-Request Envelopes

ConductorOne (C1) is an MCP gateway: one MCP endpoint in front of the organization's approved MCP servers, enforcing governance on every call. A tool call only executes when the tool is **Enabled** by an admin and the caller holds a **grant** for it. When the caller lacks access, the gateway does not fail opaquely — it returns a structured envelope in place of domain data.

This applies to any `tools.<toolName>()` call inside an `execute` program, and to directly named tool calls where code mode is off.

## The Two Envelopes

**Access request opened:**

```json
{
  "status": "request_created",
  "tool": "salesforce_query",
  "task_id": "...",
  "task_number": "...",
  "task_url": "<link to the task in C1>",
  "entitlement_id": "..."
}
```

Meaning: the tool is *requestable* by this caller but not yet granted. C1 opened an access request on the caller's behalf. **The upstream API was not called** — no data was read, nothing was written. Approval flows through the tool's normal policy (manager approval, auto-approve, JIT expiry, and so on). Once the grant lands, the same call executes normally.

**No access path:**

```json
{
  "status": "denied",
  "reason": "..."
}
```

Meaning: no access path exists for this caller — the tool is disabled, under a kill switch, restricted to other client types, blocked by a hook, or otherwise unavailable. There is nothing to wait for. Surface the `reason`.

## Rule: Check Status Before Domain Fields

Check for an envelope **before** touching any domain field of a result.

```ts
import { tools } from '@c1/code-mode';
export default async function main(input) {
  const result = await tools.salesforce_query({ soql: 'SELECT Id FROM Account LIMIT 10' });

  // FIRST: envelope check, before any domain field access.
  if (result?.status === 'request_created' || result?.status === 'denied') {
    return result;   // verbatim, so the human sees task_url or reason
  }

  if (!Array.isArray(result?.records)) {
    console.log('unexpected response from salesforce_query:', JSON.stringify(result));
    throw new Error('salesforce_query returned no records array');
  }

  return { accounts: result.records.map(r => ({ id: r.Id })), count: result.records.length };
}
```

With more than one governed call, check each result:

```ts
const results = await Promise.all([
  tools.github_list_repos({}),
  tools.jira_list_projects({}),
]);
const blocked = results.find(r => r?.status === 'request_created' || r?.status === 'denied');
if (blocked) return blocked;
```

## Do Not

| Do not | Why |
|--------|-----|
| `(result?.records ?? []).map(...)` on an unchecked result | Silently turns an access request into "zero results" and reports a false answer |
| Retry the call in the same program | The grant cannot appear mid-execution; approval is a human-timescale event |
| Swallow the envelope into a default value | The `task_url` is the only thing that unblocks the user |
| Report the envelope as a tool bug or an outage | It is the gateway's designed response |
| Try a different tool to route around the denial | Each tool is separately governed; probing alternatives generates audit noise and more requests |
| Rewrite the request as a broader query | Scope is not the constraint; the grant is |

## Agent Behavior After `request_created`

1. Stop that line of work. Do not proceed with dependent steps that need the missing data.
2. Give the user the `task_url` directly, plus which tool it is for. The user (or an approver) acts on it in C1.
3. Report what remains blocked so the user knows what will resume.
4. Retry only after the user confirms approval. Retrying before approval returns the same envelope, and may re-surface the same pending task.
5. If part of the task is independently answerable with tools that did succeed, complete that part and state clearly what is still blocked.

Report it as an access request awaiting approval, not as an error or an empty result.

## Agent Behavior After `denied`

State the `reason` and stop. There is no access path to wait on. If the user believes the denial is wrong, the escalation path is their IT or security team — not a retry, and not another tool. Common causes: the tool is disabled or under a kill switch, the client type is not allowed for that tool, a fail-closed hook denied the call, or the caller is not an app user of the upstream server's app.

## Governance Working, Not Malfunctioning

Two further outcomes are normal gateway behavior, not defects:

- **A hook denied the call.** Admin-configured pre- and post-tool-use hooks can block a call outright — for example, denying writes, or blocking output containing card numbers. Hooks are fail-closed, so a hook that errors or times out also results in a denial.
- **Output was modified.** Post hooks may redact fields (SSN, date of birth, salary, bank account, and similar), and pre hooks may cap numeric inputs such as `limit` or `page_size` below what was requested. A redacted or truncated result is the governed result.

In both cases, report what happened and stop. Do not retry with the same input, do not fan out into many smaller calls to defeat a cap, and do not describe the result as broken.

## How a Caller Gets Access

Tool access is granted through C1's normal request-and-approval flow. Approved tools are bundled into **toolsets**, toolsets are bound to **access profiles**, and a user requests the access profile:

1. In C1, go to **Requests**. Access profiles containing toolsets appear in the catalog next to app entitlements, each showing which toolset it grants, which tools are in it, and the approval policy (auto-approve, requires approval, or JIT with an expiry).
2. Open the access profile and click **Request access**, adding a justification if required.
3. Alternatively submit from Slack with `/c1 request` where the C1 Slack integration is installed. The same approval flow runs either way.
4. Track status on **My requests**; notifications arrive by Slack or email depending on tenant configuration.

A `request_created` envelope has already filed this request — the user follows the `task_url` rather than starting a new one.

Once approved, the granted tools become callable from the user's AI client, usually after the connection refreshes. Some upstream services also require the user's own credentials (per-user OAuth); the user authorizes those from their C1 profile under **AI & API > MCP connections**.

Access can also disappear mid-session: a revoked grant, an expired JIT grant, a flipped kill switch, or a client closed for inactivity all cause subsequent calls to return a denial. In-flight calls finish.
