---
name: docusign-setup
description: Configure Docusign's official hosted MCP server for Ghast using a user-owned confidential OAuth application.
---

# Docusign MCP Setup

Docusign requires a pre-registered Confidential Authorization Code Grant
client. Dynamic client registration is not supported.

## Security boundary

- Never ask the user to paste an Integration Key, client secret, access token,
  refresh token, or credential-file contents into conversation.
- Never print, log, or inspect credential values.
- The plugin reads only `DOCUSIGN_OAUTH_CLIENT_FILE`, an absolute path to a
  user-managed JSON file outside the project and plugin.
- The local compatibility bridge binds only to `127.0.0.1`, stores no
  credentials, and forwards only Docusign MCP traffic.

## Demo setup

1. In the Docusign developer Apps and Keys page, create an app and copy its
   Integration Key.
2. Add a Client Secret and store it securely.
3. Register this exact redirect URI:

   `http://localhost:3335/oauth/callback`

4. Create a private JSON file outside the repository:

```json
{
  "client_id": "YOUR_INTEGRATION_KEY",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

5. On macOS or Linux, restrict the file:

```bash
chmod 600 /absolute/path/to/docusign-mcp-oauth.json
```

6. Set only the path in the host environment:

```bash
export DOCUSIGN_OAUTH_CLIENT_FILE="/absolute/path/to/docusign-mcp-oauth.json"
export DOCUSIGN_MCP_ENVIRONMENT="demo"
```

7. Reload the active Ghast profile and complete browser authorization.

The plugin requests only `adm_store_unified_repo_read`, `aow_manage`, and
`signature`. It intentionally omits the demo-only `manage_app_keys` scope.

## Production setup

Production requires a production Docusign app, production Integration Key and
secret, the same callback URI, and production account access. Point
`DOCUSIGN_OAUTH_CLIENT_FILE` at the production credential file and set:

```bash
export DOCUSIGN_MCP_ENVIRONMENT="production"
```

Never reuse a demo app or assume demo authorization grants production access.

## Safe verification

Check only the variable and file presence:

```bash
test -n "$DOCUSIGN_OAUTH_CLIENT_FILE" &&
test -f "$DOCUSIGN_OAUTH_CLIENT_FILE" &&
echo "Docusign OAuth client file is configured"
```

After browser authorization, verify with `getUserInfo` and `getAccount`.
Do not create, send, remind, update, void, purge, or trigger anything as a
connection test.
