# Glean

Search enterprise documents, Slack, email, code, people, meetings, memory, and organization-specific tools through Glean's official Codex plugin and local MCP adapter.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/gleanwork/agent-plugins` at `9e7bd95e8debca50088f4ac0262b68689d36d7df`.

All 20 packaged skills, the local OAuth MCP adapter, official Glean icon, and MIT license are rebuilt from Glean's v3.3.0 source-of-truth repository. Ghast changes no Glean business logic or skill guidance. It rebuilds the bundle with fast-uri 3.1.5 because Glean's release lock still selected 3.1.4, which is affected by CVE-2026-18446.

## Ghast compatibility

- The original OpenAI marketplace entry is a private app connector. This port instead uses Glean's newer, public, developer-authored Codex plugin, including its local setup and OAuth adapter plus direct promotion of search, read_document, employee_search, chat, memory, and user_activity tools.
- The local adapter discovers a Glean tenant from a work email or accepts GLEAN_MCP_SERVER_URL, normalizes it to Glean's gateway endpoint, stores credentials under the user's local Glean data directory, and never packages account tokens.
- The source release is rebuilt under Node 24. The only source tree change is a structured npm override from fast-uri 3.1.4 to patched 3.1.5; all 195 upstream MCP tests, type checking, three-target plugin validation, and a Ghast protocol smoke test must pass.
- Hono, ip-address, undici, js-yaml, and nanoid appear only in the source dependency graph or build tooling and are absent from the shipped single-file runtime bundle.
- Actual tools and data depend on the user's Glean tenant, administrator configuration, connectors, permissions, agents, and MCP Gateway policy.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
