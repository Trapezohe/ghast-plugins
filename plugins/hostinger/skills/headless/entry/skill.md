---
name: hostinger-headless-entry
description: >
  Authenticate the official Hostinger MCP connection before using the bundled
  Hostinger Headless create, connect, iterate, ecommerce, WordPress, and
  deployment workflows.
---

# Hostinger Headless Entry

The full `hostinger-headless` skill is already bundled in this plugin. Do not
download another copy and do not install an unpinned server release.

## Preferred hosted connection

This plugin declares Hostinger's official remote MCP endpoint as
`hostinger-hosted`:

`https://mcp.hostinger.com`

Use the host's normal MCP connection flow and complete Hostinger browser OAuth
when prompted. The protected resource advertises the `mcp:use` scope. Never
ask the user to paste an access token, refresh token, password, or API token
into chat.

After authentication, return to `../SKILL.md`. Start with read-only account,
website, and order discovery so the workflow can resolve the user's available
products and permissions.

## Pinned local fallback

Use this only when the active host cannot connect to remote Streamable HTTP
MCP. Node.js 20 or newer is required.

```sh
npx --yes hostinger-api-mcp@1.34.0 --login
```

The official CLI opens a browser OAuth flow and stores its own credentials in
the user's Hostinger MCP configuration directory. Do not inspect, print,
copy, or move that credential file. For CI, a user-managed
`HOSTINGER_API_TOKEN` environment variable may replace OAuth; never put it in
a command argument, project file, plugin file, or conversation.

The full local server command is:

```sh
npx --yes hostinger-api-mcp@1.34.0
```

When the client has a tool-count limit, use the matching official scoped
binary at the same pinned version, such as:

```sh
npx --yes --package hostinger-api-mcp@1.34.0 hostinger-horizons-mcp
npx --yes --package hostinger-api-mcp@1.34.0 hostinger-hosting-mcp
npx --yes --package hostinger-api-mcp@1.34.0 hostinger-ecommerce-mcp
npx --yes --package hostinger-api-mcp@1.34.0 hostinger-wordpress-mcp
```

Do not run more than one overlapping Hostinger server unless the client can
disambiguate duplicate tool names. Once authenticated and connected, return
to `../SKILL.md`.
