# jam

Inspect, analyze, organize, comment on, and manage Jam bug recordings,
screenshots, video frames, transcripts, logs, network requests, user events,
metadata, folders, and recording links through Jam's official hosted MCP.

## Official hosted MCP adapter

This package contains only Ghast-authored configuration, safety instructions,
metadata, documentation, and a generic icon. It does not redistribute Jam's
hosted implementation, private Codex connector, OAuth credentials, recordings,
workspace data, or branded artwork.

Jam's official MCP and PAT guides are pinned at SHA-256 `16753f7a8592c82f484aa98a4ffefef1f785511d49c195f2f89022f8a0b0d9fb`
and `ed4cde60e15dc2cb5651dee2bbc82d892f62068821e8ef07a0d546666d335450`. The ordered 30-tool inventory is pinned at
canonical JSON SHA-256 `f3534b1291c8ca0252a6899674281e53798c673cdee8a001276ef13f93534d7a`. Protected-resource and
authorization-server metadata are pinned at `675651395646d616e5b85b89ddff52cc4ae4e631f360f232883fbf564f294905` and
`959ac141c62eb7a5fec54780b9e5a9966bb90c3468013f553cf1b0df5fdf28e2`. Codex evidence is pinned to OpenAI snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private connector ID or artwork.

## Ghast compatibility

- Ghast connects directly to `https://mcp.jam.dev/mcp` and uses Jam OAuth. The service
  supports dynamic registration, authorization code, refresh tokens, public
  clients, and PKCE S256.
- The 30 documented tools cover Jam details, console and network context,
  screenshots, video frames and analysis, transcripts, events, metadata,
  search, members, folders, comments, reactions, organization, archives,
  recording domains, and recording links.
- This is a functional superset of the Codex request to explain what a bug
  report shows, with evidence-preserving debugging and implementation-planning
  guidance.
- On August 13, 2026, missing and invalid credentials returned HTTP 401 with
  the official scopes and resource challenge. A disposable public OAuth client
  registered successfully and was immediately deleted. No Jam account,
  recording, comment, folder, or recording link was accessed or changed.
- OAuth requests `mcp:read` and `mcp:write`; the included skill requires
  explicit confirmation for every write. Headless clients may instead use
  Jam's documented expiring, workspace-scoped PATs.
- Jam recordings can contain secrets, customer data, voices, screens, logs,
  request payloads, and identifiers. Some analysis tools use Google Gemini;
  Jam states that customer data is opted out of training and de-identified.
- A generic bug-recording icon is used because no redistributable catalog
  artwork is included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Jam accounts, hosted behavior, recordings, permissions, trademarks, and terms
remain controlled by Jam.
