# outreach

Research Outreach prospects, accounts, opportunities, sequences, emails,
meetings, and tasks, draft evidence-grounded follow-ups, and safely perform
explicitly approved revenue actions through Outreach's official hosted MCP.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, metadata, and a generic revenue-workflow icon.
It does not redistribute Outreach's hosted MCP implementation, private Codex
connector, OAuth credentials, customer data, email or meeting content,
trademarks, branded artwork, or marketplace icons.

Outreach's official developer overview, authentication, tool catalog, usage,
and best-practices pages are pinned as normalized visible text at SHA-256
`ddcf07a9cb4baef7c0337a0f0bf237809535ae017432f7a1028d687cf292cc14`,
`20538caa1c3b70647b4ddeee5eba8f288433b437b7ab73773cecc778961ba707`,
`fad773e5a468697731a676743d55964df942ded00ebdccd6d35fc6fa37169221`,
`9e73047f86230c889213eec88f69bccac9f891708fcc7d7f3dd66e6737bcc3df`, and
`c2870b9eeee9d4fd4e0b1c3d1f50af701748656979f449479945c26b41f53406`. The official support overview and
CLI configuration guide are pinned at
`f83338c8a6e6671106cef532b6165247f16ffa969897fe41ed0318d0f48e920d` and
`b4b690b5b41008f5ef57be26b910633e5c9c5efdb26ce9319d50a7518755c238`.

The ordered 41-tool catalog has canonical JSON SHA-256
`71d9d8bf5845ee81cdf7a0ca3360f2c71cd6f149c9d821cb980d074df592346d` and its normalized annotation classification has
SHA-256 `85f99674e518973f57bee95e2d199f9d7cff30f1f87c61f43bc503e7eb368bd9`. Protected-resource and
authorization-server metadata are pinned at
`bd349848c7a718d0ea132a97dcbfcea714ab1daef720b9ac87f5b03caf7bbea5` and
`7815bab596279d352d7496c86841b77def068210397640e1b99a61de8357dcf8`.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app ID or artwork.
No official public source repository for Outreach's hosted MCP server was
found, so the service implementation is not packaged.

## Ghast compatibility

- Ghast connects directly to `https://api.outreach.io/mcp` over Streamable HTTP.
- Outreach publishes OAuth 2.1 authorization code and refresh-token grants,
  Dynamic Client Registration, PKCE S256, the `prospects.all` scope, and
  `client_secret_post` token authentication for dynamically registered
  clients.
- The latest official catalog documents 27 read and discovery tools, 11
  non-idempotent writes, and three read-only schema tools. It covers account,
  prospect, opportunity, sequence, task, email, calendar, Kaia meeting, user,
  team, organization, lookup, schema, creation, enrollment, removal, delete,
  and AI question workflows.
- This covers and extends the Codex prompts for finding stalled prospects,
  reviewing sequence and recent engagement context, and drafting grounded
  follow-ups. The official service also creates records and tasks, enrolls or
  removes prospects, deletes selected records, and records account or
  opportunity Q&A history.
- The included skill requires exact record resolution and explicit
  confirmation for every write. It treats sequence enrollment as a real
  outbound effect and the answer-question tools as durable history writes.
- Outreach's documentation is moving quickly. The developer overview still
  says 32 tools while the newer catalog lists 41. A separate support article
  mentions sequence create and delete, and a sample page mentions
  `prepare_for_meeting`, but those names are absent from the pinned 41-tool
  catalog and are not promised by this adapter.
- The newer catalog says all tools advertise `openWorldHint: false`, while an
  older annotation page says all Outreach tools use `openWorldHint: true`.
  The skill conservatively treats every call as an external hosted-service
  operation regardless of that inconsistent hint.
- On August 13, 2026, missing and invalid Bearer initialize requests returned
  HTTP 401 with the official protected-resource challenge and body SHA-256
  values `86e0f2f1c60752c28de1e2c761991301a23f02efcef982213973d01b3637bfc9` and
  `5020d4621be8ed817535e7421502c14951f26cd40c0a55a28bbc91ad9beec6b3`.
- A disposable loopback OAuth client registered with HTTP 201, received the
  documented confidential-client fields, and reached Outreach's official web
  authorization page with PKCE. The normal importer does not repeat this
  side-effecting registration probe or retain its client secret.
- Authenticated `tools/list`, organization data, email and meeting retrieval,
  AI question history, record creation, task creation, enrollment, removal,
  and deletion were not exercised because no user Outreach account or data
  was supplied.
- Access requires an active licensed user, an enabled organization, the
  Amplify add-on with active credits, Outreach RBAC permissions, and any
  administrator create or delete policy. Service and API throttle limits
  remain authoritative.
- A generic revenue-workflow icon is used because no licensed catalog artwork
  is included in a public official MCP source repository.

The MIT license in this package applies only to the independently authored
Ghast adapter. Outreach accounts, subscriptions, hosted service behavior,
customer and conversation data, permissions, credits, trademarks, privacy
policy, acceptable-use policy, and terms remain controlled by Outreach.
