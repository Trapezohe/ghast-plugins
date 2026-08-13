# signnow

Create, inspect, send, track, update, view, and download SignNow documents,
templates, signing invites, and embedded e-signature workflows through
SignNow's official hosted MCP server.

## Official hosted open-source MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It connects to SignNow's
hosted deployment but does not copy or redistribute the server source,
private Codex connector, account data, signed documents, or marketplace
artwork.

The server implementation is published by the official `signnow` GitHub
organization under MIT at `https://github.com/signnow/sn-mcp-server`. This adapter is pinned to
the verified `v3.1.0` commit `80c7de587367d611fc5c689a625b5a34fc5cd35e`. Its
LICENSE, README, package metadata, dependency lock, server wiring, and
principal tool-registration files are checked byte-for-byte by the importer.
The PyPI wheel is pinned at SHA-256 `8a5f6d72bf6fd5baa24abc158492b74d29f1085d1e9af0c7801ef28ac9ddd291` and the source
distribution at `08a153cb23d271e01a7a68e070490c4402feca890b1e812ebc74b8b4a382792d`.

The OAuth protected-resource metadata is pinned at canonical JSON SHA-256
`84a8494032e9f8d8d540d7e33242bf13e96582a6820aeac4a4ab4fdd604a113c` and the authorization-server metadata at
`3e4b92f71627b72d1bfe11b09098c579f40030ce04dc261a0e270464f32251b2`.

## Ghast compatibility

- Ghast connects directly to `https://mcp-server.signnow.com/mcp` using Streamable HTTP and
  SignNow OAuth. The service declares dynamic client registration,
  authorization-code and refresh-token grants, public clients, and PKCE S256.
- The pinned official v3.1.0 source exposes 25 tools. Their sorted names have
  SHA-256 `3cb78b951b857a3b39c38ffbf7ed5b0000a6973f827f8ed44d9de20dfd5199e2`; the observed canonical name and
  annotation inventory has SHA-256 `1fb65b7db7da4430fa74857439a35277e0e884576ad15ad04fa39a338e7134b3`.
- Those tools cover template and document listing, document creation from
  templates, text-field prefill, email and embedded signing, embedded sending
  and editing, invite status, download and signing links, reminders,
  cancellation, recipient replacement, upload, template creation, contacts,
  rename, document view, and SignNow's bundled skill library.
- This is a strict capability superset of the Codex app description: create
  documents from templates, prefill them, send signature requests, track
  invite status, manage templates, and retrieve signed files are all present.
- The official source test suite passed 919 tests with 1 skipped and 84.16%
  coverage on August 13, 2026. Ruff source checks, mypy strict mode, and both
  import-linter architecture contracts also passed.
- A source-runtime MCP probe returned protocol `2025-06-18` and all 25 tools.
  Its `serverInfo.version` was `3.4.7`, which is the installed FastMCP version
  rather than SignNow's v3.1.0 release. This upstream metadata defect is
  recorded rather than treated as the SignNow release version.
- Endpoint discovery, OAuth metadata, dynamic registration, and
  unauthenticated protocol behavior were verified without an account.
  Authenticated hosted tool listing and real document operations were not run.
- The endpoint advertises wildcard `*` and `offline_access` scopes rather than
  a separately verified read-only scope. The skill therefore requires fresh
  state and explicit confirmation for every write or externally usable link.
- A generic document-signing icon is used instead of SignNow marketplace
  artwork.

The MIT license in this package applies to the Ghast-authored adapter.
SignNow's source repository has its own MIT license. SignNow accounts, plans,
hosted service behavior, document data, permissions, trademarks, privacy
policy, and terms remain controlled by airSlate Inc.
