# statsig

Inspect and manage Statsig experiments, feature gates, dynamic configs, segments, metrics, results, audit logs, and dashboards through official skills and the official Statsig MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/statsig-io/agent-skills` at `e720bbb3fc7bb4f5d50ad6175e050138ddb1a1c6`.

Skills, references, scripts, commands, and public MCP declarations remain sourced from the pinned official repository. Unsupported client metadata is omitted.

## Ghast compatibility

- The Codex private app mapping is replaced by Statsig's official Console-key MCP endpoint through pinned mcp-remote@0.1.38.
- The MCP bridge expands STATSIG_CONSOLE_API_KEY inside its own process, so the secret is not written into the plugin.
- The experimental statsig-create-cloud-metric skill is excluded because its curl example expands an API key into a process argument; core Codex capabilities remain covered and the official dashboard skill is retained.
- A generic experimentation icon is used because the official skills repository does not publish a catalog icon.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
