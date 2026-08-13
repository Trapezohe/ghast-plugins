---
name: ddconfig
description: Diagnose or change Datadog MCP site, authentication, permissions, toolsets, and connectivity in Ghast without exposing credentials.
---

# Datadog MCP Configuration

Use this flow when Datadog was configured previously but tools are missing,
authentication fails, the wrong organization opens, or the user needs another
regional site.

## Checks

1. Confirm Node.js and npm are available. The plugin runs pinned
   `mcp-remote@0.1.38`; do not silently install or upgrade other packages.
2. Resolve `DD_MCP_DOMAIN`, defaulting to `mcp.datadoghq.com`, and confirm it
   is one of the seven supported public domains listed by `ddsetup`.
3. Probe `https://<domain>/v1/mcp` without credentials. HTTP 401 means the
   official endpoint is reachable. DNS, TLS, timeout, or 5xx errors indicate a
   network or service problem.
4. If OAuth is in use, restart the MCP connection and complete browser login.
   The user chooses the Datadog organization in the browser. Do not inspect
   local OAuth token storage. Clear stored authorization only when the user
   explicitly asks to reconnect or switch accounts.
5. If key authentication is in use, check only that both `DD_API_KEY` and
   `DD_APPLICATION_KEY` are present. Never display their values. Recommend
   scoped service-account keys with only the required permissions.
6. Read `datadog://mcp/whoami` when available and verify the user,
   organization, and site. Do not expose the email or organization to a new
   recipient without authorization.
7. Report exact permission, product-entitlement, toolset, rate-limit, and
   validation errors. A successful login does not grant access beyond the
   authenticated user's Datadog roles.

## Changing sites

Ask which Datadog site the user intends to use, map it to the supported domain
table in `ddsetup`, then ask the user to update `DD_MCP_DOMAIN` in the host
environment and reload the active Ghast profile. Never edit global shell
startup files or credential stores without an explicit request.

## Organization OAuth policy

Datadog organizations can restrict MCP OAuth redirect URLs. If login reports a
redirect policy error, an organization administrator must allow the callback
in Datadog Organization Preferences. Do not work around that policy with
another user's token.
