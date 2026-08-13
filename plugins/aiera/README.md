# aiera

Search and analyze Aiera corporate events, transcripts, filings, company publications, equities, financials, broker research, Third Bridge content, and trusted web results through Aiera's official MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/aiera-inc/aiera-mcp` at `882acfc09c5e5c1eed82b6e2a64e8780503ec099`.

The runtime executes Aiera's MIT-licensed standalone MCP package at pinned tag v1.2.1 and commit 882acfc09c5e5c1eed82b6e2a64e8780503ec099. The catalog icon and all 47 tool implementations come from that official repository. Ghast adds only the audited launcher and one usage skill because the upstream repository does not publish a portable agent skill.

## Ghast compatibility

- The Codex private app connector is replaced by Aiera's official standalone stdio MCP package and the user's own AIERA_API_KEY.
- The launcher fixes Aiera's source revision, official PyPI index, August 8, 2026 dependency cutoff, and the direct runtime versions recorded in the upstream uv.lock.
- Aiera declares mcp>=1.14.0 without an upper bound. The current resolver selects incompatible mcp 2.0.0, so Ghast pins upstream's mcp 1.25.0 lock version to preserve the official server API.
- Only https://graphql.aiera.com/api is allowed as AIERA_BASE_URL, preventing an environment override from sending the Aiera API key to another host.
- Every tool is read-only in the official registry, but the server sends tool name, parameters, response, error state, and duration to Aiera's collect-mcp-log endpoint after each invocation. The usage skill and README disclose this.
- The official README still says 24 tools; the pinned v1.2.1 source registry and live MCP tools/list both contain 47.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
