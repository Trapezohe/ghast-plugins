# Using Catalyst Skills with Ghast

This file is adapted by Ghast from Catalyst by Zoho's official Codex setup
reference. Shared installation, data-center, and pre-flight guidance remains
in `setup-common.md`.

## Skill activation

Install or enable the `catalyst-by-zoho` Ghast plugin, open the Catalyst
project, and ask which Catalyst skills are available. The official index and
focused service skills should be listed.

## MCP setup

The plugin already bundles the official Global MCP bridge. Set
`CATALYST_MCP_REGION` in the host environment to `us`, `eu`, `in`, `au`, `ca`,
`sa`, `jp`, or `ae`; `us` is the default. Restart the plugin session and
complete the Zoho browser authorization.

Confirm the connection by checking for `ZohoMCP_getSchema`,
`ZohoMCP_executeTool`, `ZohoMCP_listTools`, and `ZohoMCP_getFeatures`. The
`CatalystbyZoho_*` operations are values passed to `ZohoMCP_executeTool`, not
separate visible tools.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| Catalyst skills not appearing | Plugin not installed or session predates installation | Install or update the plugin, then start a fresh session |
| MCP tools not appearing | Browser authorization incomplete or bridge not restarted | Complete OAuth, verify `CATALYST_MCP_REGION`, and restart the plugin session |
| Wrong organization or project | Region or local project context mismatch | Re-run the official pre-flight and reconcile `.catalystrc` with MCP |
