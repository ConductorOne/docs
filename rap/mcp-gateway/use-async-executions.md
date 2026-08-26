# Async Executions and Polling

ConductorOne (C1) is an MCP gateway: one MCP endpoint in front of the organization's approved MCP servers. In code mode, the agent runs work by passing a TypeScript program to `execute`. A program that runs longer than the synchronous wait window does not fail — it continues server-side and is collected by polling.

## The Contract

`execute` waits roughly **25 seconds** for the program to finish.

- Finishes inside the window: `execute` returns the program's result directly.
- Exceeds the window: `execute` returns `{status: 'pending', execution_id: '...'}` and the program **keeps running server-side**.

A `pending` response is not an error, not a timeout, and not a partial failure. The work is still in progress.

Collect the result by polling:

```
get_execution({ execution_id: '<id from the pending response>' })
```

## Statuses

| Status | Meaning | Action |
|--------|---------|--------|
| `pending` | Queued, not started | Keep polling |
| `running` | Executing | Keep polling |
| `success` | Finished; full result available (output plus logs) | Stop polling; use the result |
| `error` | Failed; error detail and logs available | Stop polling; read the logs and the error |

On `success` and `error`, the response carries the full result — the program's returned object and anything written with `console.log`. The polling response's `message` includes elapsed and remaining time.

## Backoff Schedule

Poll with exponential backoff, capped at 30 seconds:

```
1s → 2s → 4s → 8s → 16s → 30s → 30s → 30s → ...
```

Do not poll in a tight loop. Do not poll on a fixed short interval for minutes.

## Do Other Work First

Polling is idle time. Before the first poll, do any independent work that does not depend on the pending result: read files, run unrelated queries, prepare the next step, summarize what has already been learned. Poll only when there is nothing else productive to do.

Do not start a second `execute` with the same program hoping it will finish faster. The first one is still running, and duplicating it doubles the upstream calls and the audit trail.

## Limits

| Limit | Value |
|-------|-------|
| Synchronous wait window | ~25 seconds |
| Maximum total execution time | 15 minutes |

A program that has not completed within 15 minutes is terminated. If a task legitimately needs more than that, narrow its scope — fewer pages, a tighter filter, a projection to fewer fields — rather than retrying the same oversized program.

## execution_id

- Opaque. Do not parse it or infer anything from its shape.
- Scoped to the calling session's tenant and principal. It is not portable to another session, user, or tenant.
- Do not persist it beyond the polling loop, and do not write it into user-facing output as a handle to be reused later.

## Loop Shape

```
result = execute({ source_code, args })
if result.status != 'pending':
    use result
else:
    id = result.execution_id
    do any independent work that does not need this result
    for delay in [1, 2, 4, 8, 16, 30, 30, ...]:
        wait(delay)
        r = get_execution({ execution_id: id })
        if r.status in ('success', 'error'):
            handle r and stop
        # pending or running: continue
```

## Reporting to the User

While polling, say the work is still running — never state or imply a result that has not come back. When `success` arrives, report the result. When `error` arrives, report the error and the relevant log lines rather than reconstructing a guess about what the program would have returned.

If a result inside a completed execution turns out to be an access-request envelope (`{status: 'request_created', ...}` or `{status: 'denied', reason}`), handle it as a governance outcome, not an execution failure. See `use-access-requests.md`.

## Reducing the Need to Poll

Long runtimes usually come from unbounded fan-out. Before running:

- Bound pagination loops to the pages actually needed.
- Use `Promise.all()` for independent lookups instead of awaiting them one at a time.
- Filter upstream where the tool supports it, rather than fetching everything and filtering in the program.
- Project results to the fields required, so less data crosses the boundary.

These reduce runtime, but a `pending` response remains normal for genuinely large work. Handle it with backoff rather than treating it as something to avoid at all costs.
