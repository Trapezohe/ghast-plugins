# Intercom

Search and analyze Intercom conversations, contacts, companies, Help Center articles, and tickets through Intercom's official hosted MCP service and official CLI.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/intercom/claude-plugin-external` at `62773a7d4b8aac31545d6888fe6479be3bc53804`.

The customer-analysis skills and MIT license are copied from Intercom's pinned official plugin repository. Ghast connects directly to Intercom's US or EU hosted OAuth MCP service and uses the separately installed official @intercom/cli only for the ticket reads that the hosted MCP does not expose. No Intercom server code, CLI runtime, private Codex connector mapping, logo, or marketplace artwork is packaged.

## Ghast compatibility

- The Codex private app mapping is replaced by Intercom's official hosted MCP endpoints. The current 13-tool service covers conversation and contact search and retrieval, company reads, Help Center article reads, and article create or update operations.
- The Codex snapshot also names tickets. Intercom's hosted MCP currently has no ticket tools, so this port uses the official @intercom/cli 0.9.0 raw API command for read-only POST /tickets/search and GET /tickets/{ticket_id} calls documented by Intercom's official OpenAPI 2.16 source.
- The official CLI remains user-managed and is never bundled or silently installed. Its current 0.9.0 dependency graph contains the high-severity GHSA-xcpc-8h2w-3j85 adm-zip denial-of-service advisory with no compatible npm fix, so installation requires informed user approval and ticket work avoids all ZIP-processing commands.
- The official plugin's Messenger installation skill is outside the Codex connector's declared support-data scope and is intentionally excluded.
- A generic support-workflow icon is used because Intercom's licensed plugin repository does not publish catalog artwork and its separate MCP repository does not grant a license for the included logos.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
