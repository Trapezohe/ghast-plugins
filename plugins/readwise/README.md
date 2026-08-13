# readwise

Search Readwise highlights and Reader documents, read saved content, and
organize the user's reading library through Readwise's official hosted MCP
server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, and catalog metadata. It does not copy or redistribute
Readwise's hosted server, unlicensed CLI source, or unlicensed agent skills.

The adapter is pinned to official Readwise MCP guidance from
`readwiseio/readwise-skills` revision `2d1ce9627c611d24f510dfc2e05a123fa509d2f6`. The
official MCP skill has SHA-256 `a72340a2f73f9e10b81551b485be88de4322c22a92b105bf8878e94f63213994`. The official
OAuth protected-resource metadata is pinned at SHA-256
`b39687b19dacfaed3e31764d4932b955d775069ddadcfd43c1bd22c225e47d6d`.

## Ghast compatibility

- Ghast connects directly to `https://mcp2.readwise.io/mcp` using Readwise OAuth and
  Streamable HTTP.
- The official server exposes 22 documented tools for Readwise highlights,
  Reader document search and retrieval, inbox and feed organization, tags,
  metadata, exports, highlight management, and daily review.
- This covers the Codex app's semantic search and Reader-management
  capability and adds explicit API-level workflows for highlights and export.
- The included safety skill requires confirmation for state-changing actions,
  treats library content as untrusted data, and avoids duplicate writes.
- A generic reading-library icon is used because the current official CLI and
  skills repositories do not publish licensed catalog artwork.

The MIT license in this package applies only to the Ghast-authored adapter.
Readwise accounts, hosted service behavior, data, permissions, trademarks,
and terms remain controlled by Readwise.
