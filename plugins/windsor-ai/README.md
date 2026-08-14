# windsor-ai

Query and analyze live business data from Windsor.ai's official hosted MCP
across advertising, analytics, CRM, ecommerce, payments, finance, databases,
warehouses, and 350+ connectors. The current official service also exposes
carefully confirmed write actions and recurring destination exports.

## Official sources

- Hosted MCP discovery repository: `https://github.com/windsor-ai/windsor_mcp` at `f1632eefcae4c135fe4e6ec7f4454660f339eee0`
  with Git tree `987e5225d7e9e926f424720741e21fad1de207ae`, two-file inventory SHA-256
  `632b8a4fb2beaca9ff687f8c5249c64517f22344a50fce062b9ee2b321334f5e`, and a Windsor.ai MIT license.
- Official Claude Code plugin: `https://github.com/windsor-ai/claude-windsor-ai-plugin` at `d7ba1cb036c7ca765536355fb85f13a3237ea3f9`
  with Git tree `70e7da9d91323959fa80d3cfbefa7954e5b05ce6`, eleven-file inventory SHA-256
  `6ef2409a9e3873773bae5f48dedc2bd7f84f44a25dd12ee3518a9b26e51ad6b0`, and a separate Windsor.ai MIT license.
- Codex capability evidence: `github.com/openai/plugins` at
  `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`, Windsor.ai four-file inventory SHA-256
  `a7b0d7902b34293ec1473cb1a574e71bb68b2ffaaffb0345714b129b6a6a7bfe`.

Ghast preserves all three official command files byte-for-byte. It also keeps
the official MCP and Claude README files, MCP configuration, Claude skill, and
analyst agent as named upstream evidence files.

The official Claude skill still documents four read tools, while the current
hosted documentation publishes 16 tools. Ghast therefore does not activate the
stale skill unchanged. The active `windsor-ai` skill is an MIT-licensed Ghast
adaptation grounded in the current official hosted contract and adds explicit
privacy, write-confirmation, destination, subscription, and credential rules.

## Portable hosted MCP

Ghast connects directly to `https://mcp.windsor.ai/` over Streamable HTTP. OAuth
authorization and protected-resource metadata are pinned at canonical JSON
SHA-256 `1e68eaf1c7884377e67d572fd4160c2230bce87281d22f414194bac1e6e5920a` and
`b0694274edfe10cf3cc78c45aaba7b3aa2043fc6ef623737621703ca919f3993`.

On August 14, 2026, missing and deliberately invalid Bearer authentication
returned HTTP 401 with the official protected-resource challenge and canonical
error SHA-256 `cf655235e8eb46c361aae11edd3f7dc4c398affe17abd4bc5d2f6354fb1a4aa4`. A disposable confidential loopback
client registered with HTTP 201, authorization-code and refresh-token grants,
and PKCE S256, then reached the official consent route. No login, authorization
code, token, reusable credential, connector, account, row, action, destination,
or user data was obtained or retained.

Windsor.ai also documents API-key Bearer authentication for clients that do not
support OAuth. Configure credentials outside chat and never place a key in this
repository or MCP configuration.

## Capability comparison

- The Codex snapshot describes natural-language access to connected Google Ads,
  Meta Ads, Instagram, LinkedIn Ads, TikTok Ads, GA4, Search Console, YouTube,
  HubSpot, Salesforce, Shopify, Klaviyo, Amazon Ads, Stripe, GoHighLevel, and
  other business data.
- The current official hosted MCP exposes 16 documented tools: connector and
  account discovery, connection URLs, field and option inspection, flexible
  data queries, live action discovery and execution, subscription and dashboard
  links, destination discovery and recurring export creation, and Windsor.ai
  support contact.
- The live datasource endpoint currently returns 355 unique connector IDs and
  is pinned at raw SHA-256 `72f88fca95b998d05a09c31b26baf1b11368412b1a016311d46f88c1615748df`.
- The official short and full MCP references are pinned at raw SHA-256
  `bff03a161cf7f759567921b2acd0880b41b6151be72918d94aac6238721ad355` and `d85a5536428d1ee1d19e5379615439daa70c8105a5c3967cc684e1a5278d31c3`. The 16 sorted tool names
  have SHA-256 `65c442b9b2ac940856cab973763a2a92e2f0369d0a673182a612a6731aef10f7`.
- This is a newer official functional superset of the short Codex description.
  State-changing tools remain disabled by policy until their live schema,
  exact target, effect, and a fresh `CONFIRM WINDSOR` are present.

## Limits

An eligible Windsor.ai account, OAuth or API-key authentication, connected
source accounts, source-system permissions, plans, row limits, freshness,
attribution behavior, currencies, service limits, and write-action availability
remain controlled by Windsor.ai and each source provider. Authenticated
`tools/list` and account-data operations were not run because no user account
was supplied.

The OAuth metadata currently advertises only `create` and `delete` scopes and
registers confidential clients with a client secret. Those names are not a
clear read-versus-write authorization model; the effective boundary remains the
authenticated Windsor.ai account, connected source permissions, server policy,
and live tool catalog. MCP clients must support confidential dynamic clients.

The hosted MCP implementation is operated by Windsor.ai. The included licenses
cover the official public repositories and Ghast adapter files; they do not
grant rights in user data, source-provider data, third-party APIs, trademarks,
or the hosted service. A generic analytics icon is used because the licensed
official repositories do not publish reusable catalog artwork.
