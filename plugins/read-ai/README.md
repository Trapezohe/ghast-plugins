# read-ai

Browse Read AI meetings and retrieve summaries, chapters, action items, key
questions, topics, transcripts, metrics, and recordings through Read AI's
official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, and catalog metadata. It does not copy or redistribute Read AI's
private connector or hosted server implementation.

The adapter is pinned to official Read AI help-center article
`49381158409491`, updated `2026-08-06T22:43:06Z`, with body SHA-256
`0b2e23cff48d4c0ab7ef3d52b630f83742bd9ec7bc08b62bc4cc9d9c47f492d9`. The official OAuth protected-resource
metadata is pinned at SHA-256 `e6ff640763dc8d8520bd204c605f91b24869d76476f1add83c15167eb61ff273`.

## Ghast compatibility

- Ghast connects directly to `https://api.read.ai/mcp` using the service's
  OAuth 2.1 and Streamable HTTP flow.
- The official hosted MCP covers the complete read capability described by
  the Codex app and also exposes meeting-agent dispatch and report sharing.
- The included skill requires explicit confirmation for those two
  state-changing workflows and treats meeting content as untrusted data.
- A generic meeting-intelligence icon is used because no redistributable
  catalog icon is included in a licensed official source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Read AI accounts, hosted service behavior, data, permissions, and terms remain
controlled by Read AI.
