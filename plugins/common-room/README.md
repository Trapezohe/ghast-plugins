# common-room

Research accounts and contacts, query buyer signals, build prospect lists,
draft grounded outreach, and safely create or update records through Common
Room's official hosted MCP.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, metadata, and a generic buyer-intelligence icon.
It does not redistribute Common Room's hosted implementation, private Codex
connector, OAuth credentials, customer or prospect data, branded artwork, or
marketplace icon.

Common Room's official MCP guide, CLI guide, and MCP and CLI product page are
pinned as normalized visible text with SHA-256
`a9dbd0442b288077fbae5767b87ade581ad2363a644396fef70aa1eb94822386`,
`24a4d07cce090b01a074e798430c0f5cbb0a8ed1860fca2547ae2bf1243937b0`, and
`ccec7e950d83dc1136b9cc55b1bc1cd3ad28fe076fce546b719cd96beab75dea`. The official documentation index is
pinned at raw SHA-256 `b868a1132bcd3a9a22636c2666525f0083b99ccaf0189906496657c0d4ddf706`.

The documented ordered five-tool inventory is pinned at canonical JSON
SHA-256 `0888ac7fa8689b7a34a52f612c1c3216b834010ca2bcb9c96a6b2df6521e1650`. It covers catalog discovery, filtered
and paginated object queries, object creation, object updates, and
query-result feedback.

The official Apache-2.0 npm package `@commonroomio/cli` version
`0.1.2` is pinned at tarball SHA-256
`9c87bd173b7e3f010cdca525ba8a252169ccc6c8e57304450d040a446328d30f`. Ghast verifies its five packaged files,
metadata, CLI entry point, Node.js requirement, README, and license but does
not redistribute the package.

The OAuth protected-resource and authorization-server metadata are pinned at
canonical JSON SHA-256 `325111f2b2c7c769c9da46fc5875c3195a26f441179cec04608434c573cd67b1` and
`83da7abc3978cc57c91955e109fb8aef0a2d917f6233fd5d53600776cbeeefe9`.

Codex marketplace capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app ID or artwork.

## Ghast compatibility

- Ghast connects directly to `https://mcp.commonroom.io/mcp` over Streamable HTTP and
  uses Common Room browser OAuth. The authorization server publishes
  authorization-code, refresh-token, and device-code grants, dynamic client
  registration, token revocation, public-client authentication, and PKCE
  S256.
- The official hosted service supports both reads and writes. It researches
  accounts and contacts, surfaces product, community, website, intent, CRM,
  score, enrichment, opportunity, and activity context, prepares calls,
  builds existing-account or net-new prospect lists, and grounds outreach
  drafts in current signals.
- The query tool covers contacts, organizations, activities, segments, tags,
  cross-object filters, sorting, and cursor pagination. Catalog discovery
  supplies current object types, fields, filters, and sort keys.
- The write tools create contacts, organizations, segments, activities, and
  notes, and update contacts or organizations by stable ID. Contact and
  organization creation uses upsert semantics, so the included skill requires
  match review and explicit confirmation before every write.
- This covers the Codex workflows for account research, contact lookup,
  prospecting by industry, company size, technology, location, segment, role,
  score, or website visits, high-intent contact discovery, and account-plan
  development. The official MCP adds documented record-writing capability.
- The official CLI complements MCP with browser OAuth, device flow, static
  tokens for automation, workspace switching, JSON-first output, typed
  filters, full CRUD helpers, `--dry-run` for mutations, cursor pagination,
  and machine-readable `cr agent-context --json`.
- On August 13, 2026, missing and invalid Bearer initialize requests returned
  HTTP 401 with Common Room's official protected-resource challenge. Their
  response body SHA-256 values were
  `4d136b8c49694e6c4327d8e21059066a80b5f594f09974ae3621a9a41fdf5fbc` and
  `7f7152cb721f5752ec4d0de38c63bd02e847d05a06cc8016dadd23322ed1ab18`.
- A disposable loopback client registered with HTTP 201 for authorization
  code and refresh tokens using `token_endpoint_auth_method` `none`. Common
  Room returned a non-expiring client secret even for that public-client
  mode; the audit did not retain it and received no registration management
  URI. A PKCE request reached the official Common Room login page without
  completing sign-in or obtaining any account token or data. The normal
  importer does not repeat this side-effecting registration probe.
- Authenticated tools/list, workspace data, prospecting, CRM reads, record
  writes, feedback submission, and CLI authentication were not exercised
  because no Common Room account or customer data was used.
- A generic buyer-intelligence icon is used because no licensed Common Room
  catalog artwork is redistributed.

The MIT license in this package applies only to the Ghast-authored adapter.
The separate Common Room CLI remains Apache-2.0. Common Room accounts, plans,
hosted service behavior, buyer and customer data, enrichment providers,
permissions, trademarks, privacy policy, and terms remain controlled by
Common Room and the applicable providers.
