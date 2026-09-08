# OneSignal for Ghast

## 简介 / Overview

连接 OneSignal 官方 OAuth MCP，处理消息通知、受众、模板与送达分析（公开测试版）。

Connect OneSignal’s official OAuth MCP for messaging, audiences, templates and delivery analytics (open beta).

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 OneSignal OAuth 授权；受账号权限与服务配额限制。 采用当前服务商自有入口及动态客户端注册，不使用旧 Smithery 入口；无需 REST API Key，也未配置借用的 OAuth Client ID。公开测试期间，应用访问可能需服务商启用。OAuth 已验证到 S256 PKCE 网页跳转；未测试 Token 交换、账号工具发现或消息送达。可在 OneSignal 的 Connected apps 中撤销授权。

Connect in Ghast and complete OneSignal OAuth in the provider browser page. Account permissions and service quotas apply. Uses the current provider-hosted endpoint with dynamic client registration, not the old Smithery endpoint. No REST API key or borrowed OAuth client ID is configured. Open-beta app access may require provider enablement. OAuth reached an S256 PKCE browser redirect; token exchange, account tool discovery and message delivery were not tested. Revoke authorization in OneSignal Connected apps when needed.

- MCP: `https://api.onesignal.com/mcp/oauth`
- [官方文档 / Provider documentation](https://documentation.onesignal.com/docs/en/model-context-protocol)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/11823027?v=4
