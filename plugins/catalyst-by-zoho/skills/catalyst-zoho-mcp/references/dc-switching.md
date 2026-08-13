## DC Switching — Catalyst Zoho MCP

Use this reference when the user wants to switch the Catalyst MCP server to a different data center.

---

## DC URL Map

| DC | Region | MCP URL |
|----|--------|---------|
| US | United States | `https://catalyst.zohomcp.com/mcp/message` |
| EU | Europe | `https://catalyst.zohomcp.eu/mcp/message` |
| IN | India | `https://catalyst.zohomcp.in/mcp/message` |
| AU | Australia | `https://catalyst.zohomcp.com.au/mcp/message` |
| CA | Canada | `https://catalyst.zohomcp.ca/mcp/message` |
| SA | Saudi Arabia | `https://catalyst.zohomcp.sa/mcp/message` |
| JP | Japan | `https://catalyst.zohomcp.jp/mcp/message` |
| UAE | United Arab Emirates | `https://catalyst.zohomcp.ae/mcp/message` |

---

## Ghast

Set `CATALYST_MCP_REGION` in the Ghast host environment to the target code:
`us`, `eu`, `in`, `au`, `ca`, `sa`, `jp`, or `ae`. Restart the plugin session
so the pinned bridge starts against the new official endpoint.

The selected data center has an independent OAuth issuer. Expect a new browser
authorization flow after restart. Credentials and sessions for the old data
center are not modified.

---

## Claude Code

Claude Code loads the MCP server URL from the catalyst-by-zoho plugin. The plugin config is cached in multiple locations — **all of them must be updated** or the switch has no effect.

**Files to update:**

1. **Plugin source** — find the source `.mcp.json` by checking `~/.claude/settings.json` under `extraKnownMarketplaces.catalyst-by-zoho.source.path`, then read the `.mcp.json` at that path.

2. **Marketplace cache:**
   `~/.claude/plugins/marketplaces/catalyst-by-zoho/.mcp.json`

3. **Version cache** — find it with:
   ```
   find ~/.claude/plugins/cache/catalyst-by-zoho -name ".mcp.json"
   ```

In each file, update the `url` field to the new DC's MCP URL. Do not change any other fields.

**After updating:** Instruct the user to restart Claude Code. The new DC server will require re-authentication — a browser login prompt appears on the next connection. Credentials on the old DC are not affected.

---

## Claude Desktop

Edit `claude_desktop_config.json`:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Update the `url` field under `mcpServers.catalyst-by-zoho` to the new DC's MCP URL. Restart Claude Desktop.

---

## Cursor

Edit `.cursor/mcp.json` in the project root. Update the `url` field under `mcpServers.catalyst-by-zoho`. Restart Cursor.

---

## GitHub Copilot (VS Code)

Edit `.vscode/mcp.json` in the workspace root. Update the `url` field under `servers.catalyst-by-zoho`. Reload the VS Code window.

---

## What to Tell the User After Switching

- Config files have been updated to `<new-dc>` DC.
- Restart your AI client to apply the change.
- After restart, you'll be prompted to log in to your Zoho account for the new DC — this is expected.
- Your session on the old DC is not affected.
- Until authentication completes, only `authenticate` and `complete_authentication` tools will be visible.

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| DC switch has no effect after restart | Connector or client cache not refreshed | In Ghast, set `CATALYST_MCP_REGION` and restart the plugin session. In Claude Code, find and update all `.mcp.json` files under `~/.claude/plugins/` referencing `zohomcp` |
| Only `authenticate` tool visible after switch | Not yet authorized on the new DC | Complete the browser login flow that appears after restarting |
| Org data from wrong DC appears | Connector or cache still points to the old DC | In Ghast, verify `CATALYST_MCP_REGION` and restart the plugin session. In Claude Code, verify all three cache paths have the new URL |
