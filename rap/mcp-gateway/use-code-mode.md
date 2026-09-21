# Using Code Mode

ConductorOne (C1) is an MCP gateway: one MCP endpoint in front of the organization's approved MCP servers. In **code mode**, the gateway does not list each upstream tool as its own named tool. It exposes two entrypoints, and the agent invokes upstream tools by writing a short TypeScript program.

| Entrypoint | Purpose |
|------------|---------|
| `describe` | Discovery. Find the tools available to this caller and read their exact names, input schemas, and response shapes. |
| `execute` | Execution. Run a TypeScript program that calls those tools. |

Upstream tools not appearing individually in the client's tool list is expected in code mode, not a discovery failure.

## Order of Operations

1. Call `describe` at the top level to find tool names and schemas. Do this **before** writing the program.
2. Write **one** program that does all the work.
3. Call `execute` once with that program.
4. If `execute` returns `{status: 'pending', execution_id}`, poll with `get_execution`. See `use-async-executions.md`.

Never call a discovery entrypoint from inside a program. Discovery is a top-level step.

## Execute Input Shape

`execute` takes a JSON object with a required `source_code` key and an optional `args` key.

```json
{
  "source_code": "import { tools } from '@c1/code-mode';\nexport default async function main(input) {\n  return { ok: true };\n}",
  "args": { "appId": "app-123" }
}
```

Runtime values go under `args` and arrive as the `input` parameter of `main`. **A key placed beside `source_code` instead of inside `args` is silently dropped** — `input.<key>` will be `undefined`.

Prefer inlining already-resolved ids as consts in the source. When parameterizing, guard at the top:

```ts
if (!input?.appId) throw new Error('appId missing from args');
```

## Program Shape

```ts
import { tools } from '@c1/code-mode';   // the ONLY valid import
export default async function main(input) {
  const result = await tools.some_tool_name({ some_arg: 'value' });
  return { result };                      // must resolve to a JSON object
}
```

Rules:

- `import { tools } from '@c1/code-mode'` is the only valid import. There are no other modules.
- The default export must be an async function named `main` taking one argument.
- Call upstream tools as `tools.<toolName>(args)`, using names and argument shapes taken from `describe`.
- `main` must resolve to a JSON object. A bare array, string, or number is rejected by the runtime.
- Never pass `undefined` as an argument value. Omit optional keys entirely.

## Single-Program Principle

Write a SINGLE program that does all the work.

Each `execute` call deploys an ephemeral function. `tools.X()` calls **inside** a program are fast; round-tripping through repeated `execute` calls is not. Do not split a task into a chain of `execute` calls to inspect intermediate values — do the chaining inside one program and return what is needed.

## Call Patterns

**Dependent calls** — sequential `await`s:

```ts
import { tools } from '@c1/code-mode';
export default async function main(input) {
  const user = await tools.okta_get_user({ user_id: input.userId });
  if (!user?.id) {
    console.log('unexpected response from okta_get_user:', JSON.stringify(user));
    throw new Error('okta_get_user returned no id');
  }
  const groups = await tools.okta_list_user_groups({ user_id: user.id });
  return { user: { id: user.id, email: user.email }, groups: groups?.records ?? [] };
}
```

**Independent lookups** — `Promise.all()`:

```ts
const [users, apps] = await Promise.all([
  tools.okta_list_users({}),
  tools.okta_list_apps({}),
]);
```

**Large result sets** — `do/while` on the page token until it is empty:

```ts
import { tools } from '@c1/code-mode';
export default async function main(input) {
  const out = [];
  let pageToken;
  do {
    const page = await tools.okta_list_users({ page_token: pageToken });
    out.push(...(page?.records ?? []));
    pageToken = page?.nextPageToken;
  } while (pageToken);
  return { users: out, count: out.length };
}
```

The pagination key names above are illustrative. Read the real key names for each tool from `describe`.

## Robustness Rules

1. **Validate before use.** Assign each result to a variable and check for the keys you expect. On a missing key, `console.log('unexpected response from <tool>:', JSON.stringify(result))` and then `throw`. Never deep-chain unvalidated values.
2. **Handle access-request envelopes first.** Any `tools.X()` call may return `{status: 'request_created', ...}` or `{status: 'denied', reason}` instead of domain data. Check `result?.status` before touching any domain field and return the envelope verbatim. See `use-access-requests.md`.
3. **`console.log()` only for errors.** Never log successful results. Logs are captured and returned, so logging a large success payload wastes context. The return value is captured anyway.
4. **Always return a structured object**, for example `{ users, count }` — never a bare primitive, array, or string. On failure, `throw`; never return partial results as if they were complete.
5. **Response shapes come from discovery, not convention.** Envelope keys differ per tool. Do not port a key such as `records` or `list` from a different tool. If an expected list comes back empty, log one raw result once, read the real keys, and fix the program.
6. **Result-size discipline.** Return only what was asked for. Project large lists down to the needed fields plus a `count`. Do not return whole records when a few fields answer the question.

## Anti-Patterns

| Anti-pattern | Correct approach |
|--------------|------------------|
| Several `execute` calls to chain steps | One program with sequential `await`s |
| Guessing a tool name or argument name | Take both from `describe` |
| Runtime values placed beside `source_code` | Place them inside `args` |
| Passing `undefined` for an optional argument | Omit the key |
| `return users` (bare array) | `return { users, count: users.length }` |
| `console.log(result)` on success | Return the value; log only on error |
| `(result?.records ?? []).map(...)` on an unchecked result | Check `result?.status` for an envelope, then validate the expected key, then map |
| Retrying a denied call inside the same program | Return the envelope and stop |
| Returning every field of thousands of records | Project to needed fields plus a count |
| Importing anything other than `@c1/code-mode` | Not available; there is no other module |

## Checklist Before Calling Execute

- Tool names and argument shapes came from `describe`.
- One program covers the whole task.
- No discovery calls inside the program.
- Runtime values are under `args`, and guarded at the top of `main`.
- Every tool result is checked for an access-request envelope, then validated.
- `main` returns a structured JSON object, projected to what was asked for.
- No `console.log` on success paths.
