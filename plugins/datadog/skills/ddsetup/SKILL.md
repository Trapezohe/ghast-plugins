---
name: ddsetup
description: Configure first-time access to Datadog's official regional MCP server in Ghast using OAuth or optional user-managed API and application keys.
---

# Datadog MCP Setup

This plugin starts Datadog's official hosted MCP server through a pinned
compatibility bridge. OAuth is the default and recommended authentication
method.

## Choose the Datadog site

US1 is used when `DD_MCP_DOMAIN` is unset. For another supported site, ask the
user to set exactly one of these domains in the host environment:

| Site | `DD_MCP_DOMAIN` |
| --- | --- |
| US1 | `mcp.datadoghq.com` |
| US3 | `mcp.us3.datadoghq.com` |
| US5 | `mcp.us5.datadoghq.com` |
| EU | `mcp.datadoghq.eu` |
| AP1 | `mcp.ap1.datadoghq.com` |
| AP2 | `mcp.ap2.datadoghq.com` |
| UK1 | `mcp.uk1.datadoghq.com` |

Datadog MCP is not available for Datadog GovCloud sites. Do not substitute a
non-Datadog host or accept an arbitrary URL.

## Authentication

- Prefer OAuth. Leave `DD_API_KEY` and `DD_APPLICATION_KEY` unset, reload the
  active Ghast profile, and complete the browser login when prompted.
- For service-account use, the user may set both `DD_API_KEY` and
  `DD_APPLICATION_KEY` outside the conversation. Never ask the user to paste
  either value, print them, inspect the full environment, or write them to a
  project file.
- If only one key variable is set, the launcher fails closed instead of
  sending partial credentials.

## Toolsets

The plugin enables `core,widgets` by default, covering logs, metrics, traces,
monitors, incidents, services, dashboards, notebooks, and visual evidence.
Set `DD_MCP_TOOLSETS` to `all`, a comma-separated documented list, or
`default` to use the server's current defaults.

After changing the site, credentials, or toolsets, reload the active Ghast
profile. Verify access with the `datadog://mcp/whoami` resource or one narrow
read-only query, such as listing currently alerting monitors. Do not create or
modify Datadog objects merely to test connectivity.
