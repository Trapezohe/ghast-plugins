# datadog

Investigate Datadog logs, metrics, traces, monitors, incidents, dashboards, services, and widgets through Datadog's official hosted MCP server and Datadog-derived setup workflows.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/datadog-labs/cursor-plugin` at `71364156c14b27466f3d646c8924318154e2321a`.

Datadog's repository supplies the official plugin design and three setup, configuration, and toolset workflows. Ghast renders client-compatible versions of those workflows and a separate safety skill. The MCP declaration is generated from Datadog's official hosted-service documentation; no Datadog server code or private connector mapping is redistributed.

## Ghast compatibility

- Ghast adapts Datadog's three official setup, configuration, and toolset workflows from the pinned Apache-2.0 Cursor plugin. The generated skill text replaces Cursor-specific registration-file editing and UI instructions with Ghast environment and reload guidance.
- The Codex private app mapping is replaced by Datadog's official regional /v1/mcp endpoint through pinned mcp-remote@0.1.38. OAuth is the default authentication path.
- DD_MCP_DOMAIN selects one of seven verified public Datadog MCP regions. US1 is the default. DD_MCP_TOOLSETS defaults to core,widgets and can select other documented toolsets.
- Optional DD_API_KEY and DD_APPLICATION_KEY values are expanded inside mcp-remote and are never stored in the plugin or inserted into process arguments.
- A Ghast-authored Datadog usage skill adds prompt-injection defenses and explicit confirmation boundaries for write, execution, deletion, retention, billing, and security tools.
- A generic observability icon is used because the official Cursor plugin does not publish a catalog icon.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
