---
name: asana-mcp-troubleshooting
description: Diagnose Asana V2 MCP connection, OAuth app, credential-file, workspace, and tool availability failures in Ghast.
---

# Asana MCP Troubleshooting

Work through these checks in order and stop at the first failure.

## 1. Confirm the supported endpoint

The plugin must use `https://mcp.asana.com/v2/mcp`. Do not fall back to the
deprecated V1 beta endpoint; Asana retired it on August 5, 2026.

An unauthenticated request should return HTTP 401 with an Asana Bearer
challenge. A timeout or DNS failure indicates a local network problem.

## 2. Confirm the credential file without exposing it

Never run `cat`, `echo $ASANA_CLIENT_SECRET`, or any command that displays the
JSON. Check only:

```bash
test -n "$ASANA_OAUTH_CLIENT_FILE" || echo "ASANA_OAUTH_CLIENT_FILE is unset"
test -f "$ASANA_OAUTH_CLIENT_FILE" || echo "Asana OAuth client file is missing"
```

The path must be absolute. On macOS and Linux, repair overly broad permissions
with `chmod 600 /absolute/path/to/asana-mcp-oauth.json`.

If the launcher says required keys are missing, ask the user to correct the
file themselves. Do not request its contents.

## 3. Confirm the Asana MCP app

- The app type must be **MCP app**, not a standard API app.
- The redirect URI must exactly match
  `http://localhost:3334/oauth/callback`.
- The app must be distributed to the selected workspace or to any workspace.
- The client ID and secret must belong to the same app.
- If the secret was rotated, the private JSON file must be updated by the
  user and the active profile reloaded.

## 4. Confirm authorization and workspace scope

The browser flow asks the user to select and authorize one workspace. Tokens
are workspace-scoped. A different workspace requires a separate authorization
session.

Enterprise administrators can block the MCP app. Report the exact Asana
policy or permission error and let the user request administrator approval.

## 5. Confirm local prerequisites

The compatibility bridge requires Node.js, npm, and pinned
`mcp-remote@0.1.38`. Check `node --version` and `npm --version`; do not install
or upgrade software without the user's approval.

OAuth tokens are managed by `mcp-remote` under the user's local MCP auth
storage. Do not read or display those files. Clear stored authorization only
when the user explicitly asks to reconnect or switch accounts.

## 6. Confirm tools

After authorization, use `get_me` or `get_my_tasks` for a read-only test. If
tools are missing, reload the active profile and inspect the concrete launcher
error. Do not create, update, comment on, or delete Asana work as a connection
test.
