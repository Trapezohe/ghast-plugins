# circleback

Search authorized Circleback meetings, transcripts, action items, calendar
events, emails, people, companies, tags, and support content through
Circleback's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, catalog metadata, and a generic meeting-context
icon. It does not copy or redistribute Circleback's hosted MCP
implementation, private Codex connector, public client rules or schemas,
meeting or email data, recordings, OAuth credentials, branded artwork, or
marketplace icon.

Circleback's official Help Center article is pinned at article ID
`13249081`, update timestamp
`2026-07-10T17:59:35Z`, and normalized Markdown SHA-256
`95ffb254cd36f1a475a63e3a7626e1dd5c27a8e19714244a892cae1969b99bb1` after volatile signed image URLs are
removed. Its ordered 11-tool names have SHA-256
`f4db1318c4bf90e4aebd1145657d67714da96162ca010eef8e0af9b9a96979a9`.

Circleback's May 31, 2026 release announcing downloadable recording links for
MCP and CLI is pinned at canonical release-object SHA-256
`63146071c6c9813bd6a9bf5463b570d376a8d2e3a3f7678eeef3fa5b47ed32e5`.

The official protected-resource metadata is pinned at canonical JSON SHA-256
`00a8e855d323feb76754d0c1bba1a10e5027a9b5e1cf62474ce9f87495c4851d`, and the authorization-server metadata at
`1d48ae9d33e75a07db7a1d34105d60eff60bbebd36ff8e09883d832667731c37`. Circleback's official Claude Code
declaration at revision `a610634c95ab310accf20a0cabdf0fa7ab784fa3` independently
corroborates the endpoint. Its official OpenClaw tool catalog is pinned at
revision `d2657b48614936554f41c99f1183fc67ed17867b` and exact SHA-256
`a4637f0519777ee80ac3662bbbd7224bd36d8e16c19f6c36e8c6e1b2a616ec93`. Those public client repositories had no
license file at the audited revisions, so none of their rules, schemas, or
source files are redistributed.

Codex capability evidence is pinned to OpenAI's plugin snapshot revision
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying the private app ID or
marketplace artwork.

## Ghast compatibility

- Ghast connects directly to `https://circleback.ai/api/mcp` using Streamable HTTP and
  Circleback browser OAuth.
- The service declares the broad `user` scope, Dynamic Client Registration,
  authorization-code and refresh-token grants, public clients, optional
  `client_secret_post`, and PKCE S256.
- On August 13, 2026, an unauthenticated MCP initialize request returned HTTP
  401 with Circleback's protected-resource challenge and exact
  `Request unauthenticated.` response. One disposable loopback public client
  registered with HTTP 201 and no client secret, and its PKCE authorization
  request reached Circleback's login page. The response provided no
  registration management URI or access token, so the audit client could not
  be deleted through RFC 7592 management.
- The current official catalog exposes 11 read-oriented tools:
  `SearchMeetings`, `ReadMeetings`, `SearchTranscripts`,
  `GetTranscriptsForMeetings`, `SearchActionItems`,
  `SearchCalendarEvents`, `SearchEmails`, `FindProfiles`, `FindCompanies`,
  `ListTags`, and `SearchSupportArticles`.
- These tools cover the Codex app's meeting notes, action items, transcripts,
  people, companies, calendar, email, and "Have I met anyone from Initech"
  workflow through Circleback's official public MCP transport.
- Circleback's newer published product surface also exposes tag and support
  search and can return a downloadable recording link in meeting details.
  Recordings are highly sensitive and should be retrieved only on an explicit,
  authorized request.
- The current public catalog is read-only. Calendar and email tools search
  existing content; they do not create or modify events, send email, or change
  action-item status.
- Authenticated tools/list and private workspace operations were not run
  because no user Circleback account, meetings, email, calendar, or recording
  data was used during the audit. Exact schemas remain service-dependent.
- The included skill narrows private-data retrieval, preserves meeting,
  timestamp, speaker, identity, and filter provenance, separates generated
  notes from source facts, protects recordings, and prevents search results
  from being described as external changes.
- A generic meeting-context icon is used because no licensed Circleback
  catalog artwork is included in the adapter.

The MIT license in this package applies only to the Ghast-authored adapter.
Circleback accounts, plans, hosted service behavior, meeting and message data,
recordings, permissions, connected accounts, AI-generated notes, trademarks,
privacy policy, and terms remain controlled by Circleback.
