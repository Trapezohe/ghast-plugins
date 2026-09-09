---
name: asana-mcp-troubleshooting
description: Diagnose Ghast-managed Asana OAuth, workspace access and official MCP connection failures.
---

# Asana MCP Troubleshooting

Use only https://mcp.asana.com/v2/mcp. Check the connection in Ghast plugin details and reconnect there when authorization has expired or been revoked. Never inspect or request credential values, token files or client secrets.

If Connect is unavailable, report the displayed service availability reason; application configuration belongs to the Ghast backend, not the user. If Asana reports the application is blocked or unavailable to a workspace, its administrator may need to enable it. Do not bypass organization policy or switch to a PAT.

After authorization, discover current official MCP tools and make a read-only identity or task-list call. Report actual errors, including network or permission failures. Do not perform writes as a connection test. Asana MCP authorization is not a granular read-only grant; continue to require explicit user approval for writes.
