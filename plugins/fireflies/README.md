# fireflies

Search, summarize, analyze, organize, share, and create clips from meeting
transcripts through Fireflies' official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It does not copy or
redistribute Fireflies' hosted MCP implementation, private Codex connector,
service source code, meeting data, API credentials, branded icon, or
marketplace artwork.

The adapter is pinned to Fireflies' official MCP configuration guide with
SHA-256 `5c8c1927db3bc8b612843c3734a987ae6db4c66bbab0ccb6596b5cfaa516f697`, its complete tool reference with SHA-256
`b2b5c5e4c79d7b1d5f6425748b8728bf61539de0e22e234b04a729844ce8baeb`, and the release note that identifies 17 core plus
two experimental tools with SHA-256 `a06b5fd65d7e5b8f1350ccfe58b11a4b53fa78dcb1c4ca7a0949d26a7f7ca3a1`. The
ordered 19-tool inventory has SHA-256
`ab390890e91939cbbc164052e7b1c3851688fa7594249c0bba241cddefdb8ebd`.

The official protected-resource metadata is pinned at canonical JSON SHA-256
`8f44680d0fcb4ec738c3e3b087b5f940e5ea6c1446799a8d3a2f444612422eea`, and the authorization-server metadata at
`97aa931cc88ad684e8add800fef6a64b25f149e9880c850719995539e4076898`. The Codex capability evidence is pinned to
OpenAI's plugin snapshot revision `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without
copying its connector mapping or artwork.

## Ghast compatibility

- Ghast connects directly to `https://api.fireflies.ai/mcp` using Streamable HTTP and
  Fireflies OAuth. The service supports Dynamic Client Registration,
  authorization-code and refresh-token grants, public clients, and PKCE S256.
- The 19 official tools cover transcript search and retrieval, summaries,
  active meetings, analytics, meeting sharing and access revocation, title
  updates, channel organization, soundbite reads and creation, users, groups,
  contacts, and Enterprise automation logs.
- This is a superset of the Codex app's conversation-history summary
  workflow. The included skill resolves the organization or contact, retrieves
  bounded meeting history, preserves meeting IDs and dates, and separates
  Fireflies facts from assistant synthesis.
- `fireflies_search` and `fireflies_fetch` are experimental and may not be
  available to every account. Core structured transcript and summary tools
  provide a fallback.
- Meeting sharing, access revocation, title updates, channel moves, and
  soundbite creation require exact-target review and immediate explicit
  confirmation. The OAuth `profile` and `email` scopes are not granular write
  authorization.
- Fireflies also documents an API-key fallback through `mcp-remote`. OAuth is
  preferred; any API key must remain in host-managed secret storage.
- The hosted MCP implementation is not open source and is not redistributed.
  Documentation, the complete published tool catalog, OAuth metadata,
  disposable public-client registration, Codex capability evidence, and
  unauthenticated protocol behavior were verified without a Fireflies
  account. Authenticated tools/list and meeting-data operations were not run.
- A generic meeting-intelligence icon is used because no licensed catalog
  artwork is included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Fireflies accounts, subscriptions, hosted service behavior, meeting data,
permissions, recordings, trademarks, and terms remain controlled by
Fireflies.
