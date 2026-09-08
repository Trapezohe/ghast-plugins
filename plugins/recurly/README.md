# Recurly Compass for Ghast

## 简介 / Overview

使用 Recurly 官方 Compass MCP 搜索文档、查询 API 参考并获取集成编码指引。

Use Recurly’s official Compass MCP for documentation search, API references and integration coding guidance.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Recurly Compass OAuth 授权；受账号权限与服务配额限制。 早期访问要求 Recurly 站点启用 MCP 功能且用户具备相应权限。服务商当前提供文档和编码指引，因此这是知识连接器，不是实时账单操作连接器。OAuth 已验证到 S256 PKCE 网页跳转；未测试 Token 交换或已授权工具。服务商 Token 过期后需重新连接。

Connect in Ghast and complete Recurly Compass OAuth in the provider browser page. Account permissions and service quotas apply. Early access requires a Recurly site with the MCP feature flag enabled and appropriate user permissions. The provider documents documentation and coding agents; this is a knowledge connector, not a live billing operations connector. OAuth reached an S256 PKCE browser redirect; token exchange and authenticated tools were not tested. Reconnect when the provider token expires.

- MCP: `https://mcp.recurly.com/mcp`
- [官方文档 / Provider documentation](https://docs.recurly.com/recurly-subscriptions/docs/compass-public-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/144605?v=4
