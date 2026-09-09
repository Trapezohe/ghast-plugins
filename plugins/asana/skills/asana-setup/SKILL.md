---
name: asana-setup
description: Connect Asana V2 MCP in Ghast through managed OAuth when the connection is not active.
---

# Asana MCP Setup

Open the Asana plugin details in Ghast and click Connect account, then authorize in Asana. Application credentials are held by the Ghast backend. Never ask users for a Client ID, Client Secret, API key, token or local credential file. No separate MCP bridge or Node.js setup is needed.

The endpoint is https://mcp.asana.com/v2/mcp. Asana MCP has no granular read-only scopes: authorization permits tools within the user's Asana access, including write tools. Do not describe this authorization as read-only. Ask for explicit approval before writes and obey the user's task scope.

After connection, discover available tools and use a read-only identity or task-list query to verify it. Never create, update, comment on or delete work just to test connectivity. Report real tool results and any workspace policy restrictions.
