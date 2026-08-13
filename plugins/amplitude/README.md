# Amplitude

Analyze Amplitude charts, dashboards, experiments, session replays, feedback, accounts, reliability, AI agents, taxonomy, and instrumentation through Amplitude's official skills and hosted MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/amplitude/mcp-marketplace` at `90c0a8e658db547ab63a2210e84be07c23ce4cd0`.

All 32 packaged skill trees are copied byte-for-byte from Amplitude's pinned MIT repository. Four feature-gated legacy chart and experiment skill variants are omitted because Ghast does not evaluate Amplitude's private feature-flag frontmatter; their current consolidated replacements are included. The hosted MCP service remains operated by Amplitude.

## Ghast compatibility

- The Codex private app mapping is replaced by Amplitude's official US or EU hosted MCP endpoint through pinned mcp-remote@0.1.38 and dynamic OAuth registration.
- AMPLITUDE_MCP_REGION selects us or eu from a strict allowlist; US is the default.
- The source repository contains 36 skills. Ghast includes the 32 current variants and excludes analyze-chart, create-chart, analyze-experiment, and monitor-experiments because Amplitude marks them for removal when its current consolidated chart and experiment tools are enabled.
- Some retained skills depend on account entitlements and server-side feature flags. The what-would-lenny-do skill also requires the separate lennysdata MCP server and explicitly remains inactive when that server is absent.
- A generic analytics icon is used because the official marketplace repository does not publish a catalog icon.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
