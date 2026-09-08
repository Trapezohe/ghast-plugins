# Pendo for Ghast

## 简介 / Overview

通过 Pendo 官方区域 MCP 服务分析产品使用、访客活动与引导内容表现。

Analyze product usage, visitor activity and guide performance using Pendo’s official regional MCP services.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Pendo OAuth 授权；受账号权限与服务配额限制。 订阅管理员需在 AI access 中启用 MCP 只读工具，写入工具另行按需启用。仅连接订阅所在区域；五个区域的 S256 OAuth 跳转均已验证，未测试账号授权与分析操作。

Connect in Ghast and complete Pendo OAuth in the provider browser page. Account permissions and service quotas apply. A subscription admin must enable MCP read tools in AI access; write tools are separately optional. Connect only the regions where your subscriptions are hosted. All five regional S256 OAuth redirects were verified. Account authorization and analytics operations were not tested.

- MCP (pendo): `https://app.pendo.io/mcp/v0/shttp`
- MCP (pendo-us1): `https://us1.app.pendo.io/mcp/v0/shttp`
- MCP (pendo-eu): `https://app.eu.pendo.io/mcp/v0/shttp`
- MCP (pendo-japan): `https://app.jpn.pendo.io/mcp/v0/shttp`
- MCP (pendo-australia): `https://app.au.pendo.io/mcp/v0/shttp`
- [官方文档 / Provider documentation](https://support.pendo.io/hc/en-us/articles/41102236924955-Connect-to-the-Pendo-MCP-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/5685215?v=4
