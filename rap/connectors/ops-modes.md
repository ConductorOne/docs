# ops-modes

One-shot vs daemon vs hosted mode.

---

## Three Run Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **One-shot** | No `--client-id` | Run once, produce .c1z file, exit |
| **Daemon** | `--client-id` provided | Connect to C1, poll for tasks, run continuously |
| **Hosted** | ConductorOne infrastructure | Managed by ConductorOne, no local deployment |

## One-Shot Mode

Run once and produce a sync file:

```bash
./baton-myservice \
  --api-token "$API_TOKEN" \
  -f sync.c1z

# Inspect results
baton resources -f sync.c1z
baton grants -f sync.c1z
```

Use for:
- Local development and testing
- CI/CD pipelines
- Manual audits
- Debugging

## Daemon Mode

Connect to ConductorOne and process tasks continuously:

```bash
./baton-myservice \
  --api-token "$API_TOKEN" \
  --client-id "$C1_CLIENT_ID" \
  --client-secret "$C1_CLIENT_SECRET"
```

The connector:
1. Authenticates to ConductorOne
2. Polls for sync/provisioning tasks
3. Executes tasks and reports results
4. Repeats until stopped

Use for:
- Production deployments
- Automated syncs
- Provisioning workflows

## Hosted Mode

ConductorOne runs the connector for you:
- No infrastructure to manage
- Automatic updates
- Credentials stored in ConductorOne

Check if your connector is available as hosted in the ConductorOne console.

## Provisioning Flag

Enable provisioning operations (grant/revoke/create/delete):

```bash
./baton-myservice \
  --api-token "$API_TOKEN" \
  --client-id "$C1_CLIENT_ID" \
  --client-secret "$C1_CLIENT_SECRET" \
  --provisioning
```

Without `--provisioning`, the connector only syncs (read-only).

## Environment Variables

All flags have environment variable equivalents:

| Flag | Environment Variable |
|------|---------------------|
| `--api-token` | `BATON_API_TOKEN` |
| `--client-id` | `BATON_CLIENT_ID` |
| `--client-secret` | `BATON_CLIENT_SECRET` |
| `--provisioning` | `BATON_PROVISIONING` |
| `--file` | `BATON_FILE` |
| `--log-level` | `BATON_LOG_LEVEL` |

## Log Levels

```bash
--log-level debug   # Verbose, for troubleshooting
--log-level info    # Default
--log-level warn    # Warnings and errors only
--log-level error   # Errors only
```
