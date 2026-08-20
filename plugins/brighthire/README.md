# brighthire

Use BrightHire's official hosted MCP to retrieve authorized interview,
candidate, role, call, transcript, scorecard, and hiring-intelligence context.

## Official hosted service

BrightHire publishes `https://github.com/brighthire/brighthire-codex-plugin` from its official GitHub
organization. The pinned repository declares `https://app.brighthire.ai/mcp/v1/` as its production
MCP endpoint, identifies BrightHire as the developer, describes browser OAuth,
and scopes the Codex plugin to interactive read access.

Ghast connects directly to the same official endpoint with the user's own
BrightHire authorization. The live OAuth metadata supports authorization code,
refresh tokens, public clients, PKCE S256, dynamic registration, revocation,
and the read-only `mcp:read.all` scope. On August 20, 2026, one disposable
loopback public client registered with HTTP 201 without a client secret. No
client value, authorization code, token, login, or account data was retained.

## Independent adapter boundary

The official repository declares MIT in its manifest but contains no LICENSE,
COPYING, or equivalent license text. This package therefore does not copy its
skill, README, privacy file, artwork, manifests, or other repository content.
It independently supplies only the factual endpoint declaration, Ghast-owned
workflow and safety guidance, metadata, documentation, and generic icon.

The bundled MIT license covers only those Ghast-authored adapter files. It does
not license or redistribute BrightHire's hosted service, source code, official
plugin materials, trademarks, icons, recordings, transcripts, scorecards,
candidate information, customer data, credentials, or service responses.

## Capability comparison

- Codex uses a private OpenAI app mapping to read BrightHire interview,
  candidate, call, role, transcript, scorecard, and hiring context.
- Ghast uses BrightHire's public official MCP URL and public OAuth onboarding,
  preserving the same documented read-only interview-intelligence scope.
- Exact authenticated tools and schemas remain service-controlled. They were
  not invoked during this audit because no user BrightHire account was used.

The included skill minimizes sensitive retrieval, preserves provenance,
separates source evidence from generated analysis, resists prompt injection,
avoids protected-trait inference, and keeps final employment decisions with
authorized humans.
