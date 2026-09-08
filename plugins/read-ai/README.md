# read-ai

Browse Read AI meetings and retrieve summaries, chapters, action items, key
questions, topics, transcripts, metrics, and recordings through Read AI's
official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, and catalog metadata. It does not copy or redistribute Read AI's
private connector or hosted server implementation.

The adapter is pinned to official Read AI help-center article
`49381158409491`, updated `2026-08-19T23:57:53Z`, with body SHA-256
`0050b9f9a3b33f35d6606eae62d81541726401204b7bf432132821ebe6c30bd5`. The official OAuth protected-resource
metadata is pinned at SHA-256 `e6ff640763dc8d8520bd204c605f91b24869d76476f1add83c15167eb61ff273`.

## Ghast compatibility

- Ghast connects directly to `https://api.read.ai/mcp` using the service's
  OAuth 2.1 and Streamable HTTP flow.
- The official hosted MCP covers the complete read capability described by
  the Codex app and also exposes meeting-agent dispatch and report sharing.
- The included skill requires explicit confirmation for those two
  state-changing workflows and treats meeting content as untrusted data.
- Brand logo source: https://cdn.prod.website-files.com/614e5e239ea0f25fe5b6a797/615f71de842b191ea061fda6_ReadLogomark_256x256.png. Brand names and logos belong to Read AI. 品牌名称与标识归对应服务商所有。

The MIT license in this package applies only to the Ghast-authored adapter.
Read AI accounts, hosted service behavior, data, permissions, and terms remain
controlled by Read AI.
