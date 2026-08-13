---
name: asana-setup
description: Detect and configure Asana V2 MCP credentials for Ghast. Run before using Asana when the connection is not already active.
---

# Asana MCP Setup

This plugin connects to Asana's official V2 MCP server through the Codex flow
documented by Asana. V2 requires a pre-registered Asana MCP app and does not
support dynamic client registration.

## Security boundary

- Never ask the user to paste a client ID, client secret, access token, or
  refresh token into conversation.
- Never print, log, or inspect credential values.
- The plugin reads only `ASANA_OAUTH_CLIENT_FILE`, which must be an absolute
  path to a user-managed JSON file outside the project and plugin.
- The file must contain `client_id` and `client_secret` and should be readable
  only by the current user.

## Setup

1. Ask the user to open Asana's developer console and create an **MCP app**.
2. Configure the exact redirect URI:

   `http://localhost:3334/oauth/callback`

3. Configure the app for the intended workspace or for any workspace.
4. Ask the user to create a private JSON file outside the repository:

```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

5. On macOS or Linux, ask the user to protect it with:

```bash
chmod 600 /absolute/path/to/asana-mcp-oauth.json
```

6. Ask the user to set the file path in the host environment:

```bash
export ASANA_OAUTH_CLIENT_FILE="/absolute/path/to/asana-mcp-oauth.json"
```

7. Reload the active Ghast profile after setting the variable.

## Safe verification

Check only whether the variable and file are present. Do not print the file:

```bash
test -n "$ASANA_OAUTH_CLIENT_FILE" &&
test -f "$ASANA_OAUTH_CLIENT_FILE" &&
echo "Asana OAuth client file is configured"
```

The plugin launcher validates that the path is absolute, the JSON has both
required keys, and Unix permissions are restricted. It passes only the file
path to pinned `mcp-remote@0.1.38`; the secret does not enter the process
arguments.

After the browser authorization succeeds, verify with `get_me` or
`get_my_tasks`. Do not create or modify a record merely to test connectivity.
