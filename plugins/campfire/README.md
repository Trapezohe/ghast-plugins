# Campfire for Ghast

## 简介 / Overview

通过 Campfire 官方 MCP 服务查询会计记录、预算、收入合同与财务报表。

Query accounting records, budgets, revenue contracts and financial statements through Campfire’s official MCP service.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Campfire OAuth 授权；受账号权限与服务配额限制。 已验证 OAuth 发现及 S256 授权跳转；未测试账号登录与业务操作。

Connect in Ghast and complete Campfire OAuth in the provider browser page. Account permissions and service quotas apply. OAuth discovery and the S256 authorization redirect were verified; account sign-in and business operations were not tested.

- MCP: `https://api.meetcampfire.com/mcp`
- [官方文档 / Provider documentation](https://docs.campfire.ai/guides/ai-integration)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://docs.campfire.ai/mintlify-assets/_mintlify/favicons/campfire/DSHwJCk0-i0ASSwR/_generated/favicon/android-chrome-192x192.png
