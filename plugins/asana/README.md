# asana

Read and manage Asana tasks, subtasks, comments, due dates, projects, portfolios, status updates, teams, users, and workspace priorities through Asana's official V2 MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/Asana/cursor-marketplace-plugin` at `caf02337846594b6af5221ea5165c1dd0d273d9b`.

Skills, references, scripts, commands, and public MCP declarations remain sourced from the pinned official repository. Unsupported client metadata is omitted.

## Ghast compatibility

- Ghast imports Asana's three official skills, MIT-licensed logo, and behavioral rules from the pinned Asana repository.
- Connect through Ghast-managed OAuth using the official V2 MCP endpoint. Application secrets stay in the Ghast backend; users do not provide API keys, OAuth client files or install a bridge.
- Asana's official rules are retained and merged into the active usage skill because Ghast does not execute Cursor rule files directly.
- Only https://mcp.asana.com/v2/mcp is used. The older V1 beta endpoint was retired on August 5, 2026.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.

Asana MCP authorization covers tools available to the user and does not offer granular read-only scopes. The connection test is read-only; writes require explicit user approval. Workspace administrators may restrict this application.
