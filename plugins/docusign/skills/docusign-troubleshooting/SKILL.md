---
name: docusign-troubleshooting
description: Diagnose Docusign MCP environment, OAuth app, callback, credential-file, local bridge, entitlement, and tool failures in Ghast.
---

# Docusign MCP Troubleshooting

Work through these checks in order and stop at the first failure.

## 1. Confirm environment and credentials

- `DOCUSIGN_MCP_ENVIRONMENT` must be exactly `demo` or `production`; demo is
  the default.
- The credential file must belong to an app in that same environment.
- Check only whether `DOCUSIGN_OAUTH_CLIENT_FILE` is set, absolute, and exists.
  Do not display the file or environment contents.
- On macOS and Linux, the file must be mode 600 or otherwise inaccessible to
  group and other users.

## 2. Confirm the Docusign app

- The app needs an Integration Key and Client Secret from the same app.
- The exact redirect URI is `http://localhost:3335/oauth/callback`.
- A rotated secret requires the user to update their private file and reload
  the active profile.
- The authorization request uses `adm_store_unified_repo_read`, `aow_manage`,
  and `signature`. Account policy or missing product entitlements can still
  deny individual tools.

## 3. Confirm local prerequisites and ports

- Check `node --version`, `npm --version`, and network access to the selected
  Docusign MCP host.
- OAuth callback port 3335 and compatibility proxy port 3336 must be free.
- If only 3336 conflicts, set `DOCUSIGN_MCP_PROXY_PORT` to another unused local
  port from 1024 through 65535. Changing it creates a new local OAuth cache
  identity and can require authorization again.
- Do not change callback port 3335 without also changing the registered
  Docusign redirect URI and this audited plugin.

## 4. Understand the compatibility bridge

Docusign currently returns HTTP 403 with `RBAC: access denied` when no bearer
token is present, while its official OAuth flow is triggered by a 401 invalid
token response. The local loopback bridge supplies only a three-part invalid
sentinel token for the first unauthenticated request. After OAuth, the real
host-managed bearer token replaces it and is forwarded unchanged.

The bridge:

- binds only to `127.0.0.1`;
- accepts only `/mcp` and protected-resource metadata paths;
- forwards only to the selected official Docusign host;
- does not write tokens or credential values;
- uses pinned `mcp-remote@0.1.38` for OAuth and token refresh.

Do not remove the bridge or replace it with a manually pasted bearer token.

## 5. Confirm account and products

After authorization, call `getUserInfo` and verify the returned account,
environment, and API base URI. Then use a read-only account or envelope query.

Agreement Manager tools require accessible agreement data and extraction
entitlements. Workflow Builder tools require configured workflows and
permissions. eSignature tools require the relevant account permissions.
Report the exact Docusign denial instead of falling back to another account.

## 6. Confirm live tools

Production currently publishes 22 tools. Demo currently publishes 35,
including additional beta, developer, billing, brand, tab-group, and data
verification tools. The plugin requests least-privilege scopes, so demo
developer app-key management can remain unavailable by design.

If tool names differ, rerun the audited importer and re-review Docusign's
published catalog before changing instructions or enabling writes.
