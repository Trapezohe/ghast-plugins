# dovetail

Search, inspect, synthesize, and explicitly create Dovetail projects,
research data, highlights, docs, channels, themes, people, tags, fields, and
files through Dovetail's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, catalog metadata, documentation, and a generic icon. It does
not copy or redistribute Dovetail's hosted MCP implementation, private Codex
connector, API tokens, workspace data, branded artwork, or marketplace icon.

Dovetail's official public source repository is pinned at
`88a7389ccca718f9eff2f680ecb3f34713500866`. The importer verifies its MIT license, README,
package metadata, server source, retry helper, and exact eight-tool
self-hosted inventory. The official `v0.3` release points to
commit `12693784710f41aa74d806af5eeca34b1a7f6fa7`; its `index.js` and source-map SHA-256
values are `c987beead25788b0633068e0ff119b4f7400abe46e626af3c374da819fd9a458` and
`85fd2fe964819e85aba61d653d1745faf0cca5c01942301c1bbf76ebcde385d3`.

The official hosted MCP documentation is pinned at SHA-256
`03cb4a1b08e5fd3f5dab5be749f609800207577323b1d0d40280873b3b0b24e8`. Its ordered 40-tool inventory is pinned at
canonical JSON SHA-256 `124bd35e14d30bd540280db8c1cda89b3fe6503094a7b0f90fa60f2999c2ef39`. The self-hosted and
authorization guides are pinned at `7c8024e857d2a966e9f1a86926571a21e508d15537d1ba7a375fc25815370533` and
`d3dadee1e7ec111357158fb4d43a7e27c2c37835d9611f31d3c6665d037a1ba6`.

Protected-resource and authorization-server metadata are pinned at canonical
JSON SHA-256 `a08555b9f481613bc5e821cc36994f6fd064e7d55576702c2356f49412fac393` and
`932023b5c8380a31395f75be234832dfaa878e586cbfb7bbe2b5c7f2533d4694`. Codex capability evidence is pinned to
OpenAI plugin snapshot `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its
private app identifier or artwork.

## Ghast compatibility

- Ghast connects directly to `https://dovetail.com/api/mcp` over Streamable HTTP and
  sends the user-owned API token from the `dovetail-api-token` vault entry as
  an Authorization Bearer header.
- Dovetail documents that API tokens are opaque `api.` values, expire after
  30 days, and can be manually revoked. The token is not stored in this
  package.
- The hosted catalog exposes 40 tools for workspace search, projects,
  templates, folders, research data, highlights, docs and comments,
  channels and themes, users, contacts, tags, custom fields, and files.
- Eight documented create tools cover projects, folders, research data,
  transcript highlights, docs, comments, channel data, and tags. The
  included skill requires exact-target review and explicit confirmation for
  every create.
- This is a functional superset of the Codex app description. It supports
  finding relevant projects, notes or research data, docs, themes, customer
  evidence, friction points, and renewal context, while preserving source
  IDs and distinguishing evidence from inference.
- Dovetail's public self-hosted repository exposes only eight older read-only
  tools and uses insight endpoints that the current API documentation marks
  deprecated in favor of docs. Ghast uses the recommended hosted endpoint
  rather than presenting the self-hosted release as the complete current
  capability.
- The hosted endpoint advertises OAuth authorization-code and refresh-token
  grants, but Dovetail's MCP documentation says it supports neither Dynamic
  Client Registration nor Client-Initiated Metadata Discovery and publishes
  no client ID or secret for third-party clients. Ghast therefore uses the
  official custom-header API-token path.
- On August 13, 2026, missing and invalid API-token initialize requests
  returned HTTP 401 with the official Dovetail protected-resource challenge.
  Authenticated tools/list and real workspace operations were not run because
  no Dovetail account or token was supplied.
- Research transcripts, customer evidence, contacts, comments, files,
  presigned download URLs, and unpublished findings can be sensitive. The
  skill bounds retrieval, disclosure, file access, and state-changing calls.
- A generic research-workspace icon is used because the official public
  source repository does not include redistributable catalog artwork.

The MIT license in this package applies only to the Ghast-authored adapter.
Dovetail accounts, hosted service behavior, workspace data, API access,
permissions, trademarks, and terms remain controlled by Dovetail.
