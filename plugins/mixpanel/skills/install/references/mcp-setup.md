# Mixpanel MCP server setup for Ghast

Official documentation: `https://docs.mixpanel.com/docs/mcp`.

## Regional endpoints

| Region | `MIXPANEL_MCP_REGION` | Official URL |
| --- | --- | --- |
| US | `us` | `https://mcp.mixpanel.com/mcp` |
| EU | `eu` | `https://mcp-eu.mixpanel.com/mcp` |
| India | `in` | `https://mcp-in.mixpanel.com/mcp` |

The bundled launcher accepts only these three values and defaults to US.
Set the region in the Ghast host environment before loading or reloading the
profile that contains this plugin.

## Interactive OAuth

Leave `MIXPANEL_MCP_SA_TOKEN` unset. The bundled bridge uses
`mcp-remote@0.1.38`, discovers Mixpanel's RFC 9728/RFC 8414 metadata,
dynamically registers a public client, and completes Authorization Code +
PKCE S256 in the browser. Tokens are managed by the bridge's local OAuth
storage. Never inspect, print, or move those token files.

## Service account

Mixpanel's MCP service-account support is beta and intended for
non-interactive agents. The user creates the account in Mixpanel and stores
the base64 encoding of `username:secret` in `MIXPANEL_MCP_SA_TOKEN` outside
the conversation. Do not accept the raw username, secret, or encoded token in
chat and do not write it into the plugin.

The launcher validates the token's base64 shape, constructs Mixpanel's
required `Authorization: Bearer Basic <token>` value in child-process
environment memory, and passes only an environment placeholder in argv.

## Verify

1. Reload the active Ghast profile and connect the `mixpanel` MCP server.
2. Confirm the server lists tools.
3. Call `Get-Projects` (the client may normalize its name) and confirm at
   least the expected accessible project is visible.
4. If projects are missing, verify the selected region before changing auth.

The official documentation currently lists 63 tools. They cover analytics,
dashboards, data discovery, Lexicon and data quality writes, custom
properties, cohorts, lookup tables, metrics, session replay, experiments, and
feature flags.

## Safety and access

- MCP must be enabled for the Mixpanel organization.
- Existing Mixpanel roles, project permissions, and Data Views still apply.
- Reads and writes are both available. Preview and explicitly confirm
  destructive, bulk, merge, lifecycle, or high-impact changes.
- Mixpanel states that MCP is not currently covered for HIPAA/PHI use.
- The current documented limit is 600 MCP requests per hour per user.
