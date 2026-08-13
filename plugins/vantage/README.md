# vantage

Analyze and govern multi-cloud costs, usage, forecasts, budgets, alerts, reports, recommendations, tags, dashboards, and FinOps workflows through Vantage's official hosted MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/vantage-sh/vantage-mcp-server` at `74fd3ddccc5c2e735d68a364e3f28467c0ba2a60`.

The official Vantage logo and MIT license come from the pinned Vantage MCP repository. The remote server remains operated by Vantage; Ghast adds only the direct HTTP declaration, safety guidance, documentation, and catalog metadata.

## Ghast compatibility

- Vantage's official documentation states that its ChatGPT app, remote MCP, and self-hosted MCP use the same unified open-source codebase with feature parity. Ghast connects directly to the provider-recommended remote endpoint.
- The pinned source exposes 122 tools: 67 read-only and 55 write-capable tools, with 37 marked destructive. Coverage includes costs, providers, accounts, forecasts, anomalies, recommendations, budgets, alerts, reports, dashboards, tags, workspaces, audit logs, and governance resources.
- OAuth is the default and supports public clients, dynamic registration, authorization-code and refresh-token grants, and PKCE. Vantage also supports a user-managed API token for clients that cannot complete OAuth.
- The adapter packages no Vantage server runtime or npm dependencies. Vantage account access, RBAC, API limits, service behavior, and hosted dependency security remain controlled by Vantage.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
