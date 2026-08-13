# asana

Read and manage Asana tasks, subtasks, comments, due dates, projects, portfolios, status updates, teams, users, and workspace priorities through Asana's official V2 MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/Asana/cursor-marketplace-plugin` at `caf02337846594b6af5221ea5165c1dd0d273d9b`.

Skills, references, scripts, commands, and public MCP declarations remain sourced from the pinned official repository. Unsupported client metadata is omitted.

## Ghast compatibility

- Ghast imports Asana's three official skills, MIT-licensed logo, and behavioral rules from the pinned Asana repository.
- Cursor-specific setup is rewritten for Asana's official Codex V2 flow through pinned mcp-remote@0.1.38. The bridge reads an absolute, permission-restricted OAuth JSON path from ASANA_OAUTH_CLIENT_FILE, so the client secret is never stored in the plugin or passed as a process argument.
- Asana's official rules are retained and merged into the active usage skill because Ghast does not execute Cursor rule files directly.
- Only https://mcp.asana.com/v2/mcp is used. The older V1 beta endpoint was retired on August 5, 2026.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
