# Sentry

Ghast-maintained investigation workflows connected directly to Sentry's official
hosted MCP at `https://mcp.sentry.dev/mcp` through native Streamable HTTP and
OAuth. Source: https://mcp.sentry.dev/

## Migration from the earlier package

This version replaces the OpenAI-derived Python API script and workflow with
Ghast-authored instructions and Sentry's own MCP service. Existing shell tokens
are not imported. Installation does not grant account access: connect Sentry
separately from the plugin detail page.

The official server supports investigation and management tools. This package
is not a transport-level read-only connection or a deterministic redaction
proxy. The workflow limits investigation to reads, requires explicit scope for
writes, and omits sensitive event data from its summaries. Available records,
tools and actions depend on account permissions and the live service.

## Language and logo

English and Chinese introductions are separate manifest fields, selected by
Ghast's interface language.

Logo: https://avatars.githubusercontent.com/u/1396951?v=4
The source is Sentry's official `getsentry` GitHub organization, which links to
https://sentry.io. Sentry retains ownership of its brand asset. The MIT license
covers Ghast-authored text and configuration only.

Local install checks do not establish successful authenticated issue queries.
OAuth discovery and redirect tests stop before account consent and token exchange.
