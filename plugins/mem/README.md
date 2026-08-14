# mem

Search, read, create, update, organize, trash, and restore Mem notes,
attachments, recordings, and collections through Mem Labs' official hosted
MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, catalog metadata, and a generic notebook icon.
It does not copy or redistribute Mem's hosted implementation, private Codex
connector, app ID, service source, user data, credentials, trademarks, branded
artwork, or marketplace icon.

The official overview, setup, supported-tools, and security documents are
pinned at SHA-256 values `d24c792129dd3bdec5cd4425eafeb91cf3203f427b7eedcfe82c217ebae3285e`, `f45d563657916fefe2e2c5f8524994046798ebcdcf1febe9f34fd992c2472e0e`,
`68ae9610531560adc9bfb157727125ce3f3fdd1357ef6fbbcecb2b22f45d288e`, and `1b5f1d2bfde3f581d48fa544ba558e81d6b485597858f853fd8a2db8e788110f`. The documentation index and
OpenAPI document are pinned at `ec2d7f2a57ba001c6a160c0ac9ee09b76dcffdd040630bde4dae1df6e57ab4e6` and
`0626dda2118650b5fd17d9803fa2410677daedd02d934930157000e6003bf448`.

OAuth protected-resource, authorization-server, and OpenID metadata are pinned
at canonical JSON SHA-256 `d1a5188d322aa3532cec4ea004d9f78ae1b58007ee3bd4d835b128124eb8c3f4`,
`059bdc244a84b7f1f6fbc0f0bfe2272a8029f436d9e342eea0a28b4c87eb65ee`, and `6c61e00850ba1e817e754a8cd5d0d2b165cdd2f511c77b754057f7e106a8a587`. The current 23-tool public schema
is pinned at canonical SHA-256 `092589b5e1c61a46e228b09e4d2088c3105329af1d3edc5084c8678cb2d13f28`.

## Ghast compatibility

- Ghast connects directly to `https://mcp.mem.ai/mcp` over Streamable HTTP and Mem OAuth.
  The service publishes dynamic client registration, public clients,
  authorization-code and refresh-token grants, and PKCE S256.
- The 23 official tools cover note search, semantic related-note lookup,
  listing, creation, full-body versioned updates, timestamp correction, trash
  and restore, attachment search and reading, temporary downloads, focused
  attachment questions, audio transcripts, and collection management.
- This covers the Codex app's notebook search, chat capture, living-document
  editing, collection organization, meeting synthesis, research, PKM, and
  note-based task workflows. Attachment and recording tools extend the short
  Codex description.
- On August 14, 2026, an unauthenticated initialize returned HTTP 401 and the
  official OAuth challenge. Public tool schemas were readable with an invalid
  token, while a random note read returned an authorization error. No account,
  note, attachment, recording, collection, credential, or user data was used.
- A one-time disposable loopback public client registered with HTTP 201 and
  no client secret. Routine imports do not repeat registration or retain a
  client ID.
- A generic notebook-search icon is used because no licensed Mem catalog art
  is included in a public official source repository.

The MIT license in this package applies only to the independently authored
Ghast adapter. Mem accounts, hosted service behavior, APIs, data, permissions,
trademarks, privacy policy, and terms remain controlled by Mem Labs.
