# Shopify

Shopify developer tools for OpenAI Codex — search Shopify docs, generate and validate GraphQL, Liquid, and UI extension code. Skill scripts send usage telemetry (queries, code, model/client identifiers) to shopify.dev by default; set OPT_OUT_INSTRUMENTATION=true to disable.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/Shopify/Shopify-AI-Toolkit` at `cc5af6505c27939222072449278f6356857cb064`.

Skills, references, scripts, commands, and public MCP declarations remain sourced from the pinned official repository. Unsupported client metadata is omitted.

## Ghast compatibility

- Shopify's skill-local telemetry hook paths use Ghast's host-resolved <SKILL_DIR> placeholder instead of the Claude-only CLAUDE_PLUGIN_ROOT variable.
- Official Shopify scripts send documented usage telemetry by default; users can set OPT_OUT_INSTRUMENTATION=true.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
