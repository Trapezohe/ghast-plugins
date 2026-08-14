# ranked-ai

Analyze and manage Ranked AI SEO projects through Ranked AI's official hosted
MCP server.

## Official service

Ranked AI publishes `https://app.ranked.ai/api/mcp/sse` for ChatGPT, Claude,
Cursor, and other MCP clients. The current official overview lists tools for
project metrics, keyword rankings, AI visibility, audits, backlinks, content,
local heatmaps, sitemap indexing, keyword and prompt management, content
approval and revisions, report generation, and audit execution.

The official text labels the inventory as 10 read plus 8 write tools, but its
table currently contains 9 read and 8 write names. This adapter pins the 17
actually listed names and records the discrepancy instead of inventing an
eighteenth tool.

## Capability comparison

- Codex: manage traditional and AI-search keywords, rankings, audits,
  backlinks, reports, and related project data through a private connector.
- Ghast: connect directly to Ranked AI's official hosted MCP with standard
  browser OAuth and use all 17 currently listed official tools.
- The official MCP is a functional superset of the Codex description because
  it also documents AI visibility, content workflows, heatmaps, sitemap
  indexing, prompt management, report creation, and audit execution.

## Verification and licensing

The importer pins the OpenAI marketplace evidence, Ranked AI's official MCP
overview, setup, tool reference, rate-limit guide, changelog, endpoint
metadata, OAuth metadata, and anonymous initialization boundary. Dynamic
client registration and routing to the official login page can be checked
with the optional `--verify-registration` flag. Authenticated tool listing
and customer-data calls require a user account and were not executed. The
setup guide says the MCP has read and write access, but endpoint discovery
advertises only `read:projects` and OAuth metadata lists only `read:*` scopes;
actual write authorization therefore remains an account-level verification.

The MIT license in this package covers only the Ghast-authored endpoint
declaration, workflow guidance, metadata, documentation, and generic SEO icon.
It does not license or redistribute Ranked AI's hosted implementation, private
Codex connector, service data, credentials, documentation, logos, trademarks,
or customer content. Account access, subscriptions, usage limits, service
behavior, and terms remain controlled by Ranked AI.
