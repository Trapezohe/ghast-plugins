# Tally for Ghast

## 简介 / Overview

通过 Tally 官方 MCP 服务构建表单并分析提交记录（Beta）。

Build forms and analyze submissions through Tally’s official MCP server (Beta).

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Tally OAuth 授权；受账号权限与服务配额限制。 服务商将 MCP 标记为 Beta。已验证 OAuth 发现及 S256 跳转，未测试账号登录与表单操作。

Connect in Ghast and complete Tally OAuth in the provider browser page. Account permissions and service quotas apply. The provider marks MCP as Beta. OAuth discovery and S256 redirect were verified; account sign-in and form operations were not tested.

- MCP: `https://api.tally.so/mcp`
- [官方文档 / Provider documentation](https://developers.tally.so/api-reference/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://developers.tally.so/mintlify-assets/_mintlify/favicons/tally/GwnFY1zAokn6LpcE/_generated/favicon/android-chrome-192x192.png
