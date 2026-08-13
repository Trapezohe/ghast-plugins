# apollo

Prospect for people and companies, enrich leads, load reviewed contacts into outreach sequences, and query sales analytics through Apollo.io's official skills and hosted MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/apolloio/apollo-mcp-plugin` at `2adde980e45f421b7e9383d92870455627936bce`.

All four workflow skills, the MCP declaration, and license come from Apollo.io's pinned MIT repository. Ghast changes only the Claude-specific MCP tool namespace and three explicit credit, personal-data, and sequence-mutation safety boundaries. The hosted MCP service remains operated by Apollo.io.

## Ghast compatibility

- The Codex private app mapping is replaced by Apollo.io's official https://mcp.apollo.io/mcp Streamable HTTP service with browser OAuth.
- Twenty Claude-specific tool references are mechanically rewritten from mcp__claude_ai_Apollo_MCP__* to Ghast's mcp__apollo__* namespace; tool suffixes and arguments are unchanged.
- Ghast requires explicit confirmation before credit-consuming enrichment, defaults personal-email revelation to false unless the user explicitly requests it, and requires fresh confirmation before removing or stopping sequence contacts.
- The public OAuth metadata currently advertises 67 scopes. The four packaged skills exercise 12 confirmed tools, while the hosted service may expose additional tools subject to Apollo permissions, credits, plan, and future service changes.
- A generic prospecting icon is used because the official repository does not publish a redistributable catalog icon.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
