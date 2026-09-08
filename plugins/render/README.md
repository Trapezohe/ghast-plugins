# Render

Skills for deploying, debugging, monitoring, and migrating apps on Render.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/renderinc/render-codex-plugin` at `14032768453fd21c57f7e3a9c0e7659a2c7dce9d`.

Skills, references, scripts, commands, and public MCP declarations remain sourced from the pinned official repository. Unsupported client metadata is omitted.

## Ghast compatibility

- The pre-registered Codex OAuth client id is not reused. Ghast follows Render's official generic-client setup and sends a user-managed Render API key from the encrypted Profile Vault.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.


## Browser authorization / 浏览器授权

`render` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. Ghast must configure a registered OAuth application before managed login is available. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。正式一键登录仍需 Ghast 配置已注册的 OAuth 应用。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [render resource metadata](https://mcp.render.com/.well-known/oauth-protected-resource/mcp) · [authorization metadata](https://api.render.com/.well-known/oauth-authorization-server)
