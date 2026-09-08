# Deepnote

Search, inspect, create, edit, link, and run Deepnote projects and notebooks through Deepnote's official hosted MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/deepnote/codex-plugin` at `46088505120f7056ccf2fed2f0b1039bd732ad54`.

Five workflow skills and the SVG icon are copied from Deepnote's pinned Apache-2.0 repository. Ghast translates the repository's bearer-token declaration into its native Profile Vault header syntax. Because that source snapshot predates the current hosted service's expanded toolset, Ghast also adds one clearly identified current-service and safety skill derived from Deepnote's official MCP documentation.

## Ghast compatibility

- The Codex private app mapping is replaced by Deepnote's official https://deepnote.com/mcp endpoint. Its API-key authentication is translated to Ghast's encrypted Profile Vault as Bearer $VAULT:deepnote-api-key.
- Deepnote's current official MCP documentation lists 24 tools, including block updates and reordering, notebook run history, cached integration structure, integration writes, notebook duplication, and official project URL generation.
- The five developer-authored source skills remain byte-for-byte. A Ghast-authored deepnote-current-service skill records the newer official tool surface and safety boundaries without presenting that text as Deepnote source.
- The service advertises OAuth, but arbitrary localhost dynamic-client callbacks are not accepted. This package retains Deepnote's API-key path so it does not depend on an unverified Ghast OAuth callback allowlist.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.


## Browser authorization / 浏览器授权

`deepnote` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. The service advertises dynamic registration or client metadata documents. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。服务公开提供动态注册或客户端元数据文档支持。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [deepnote resource metadata](https://deepnote.com/.well-known/oauth-protected-resource/mcp) · [authorization metadata](https://deepnote.com/.well-known/oauth-authorization-server/mcp/oauth)
