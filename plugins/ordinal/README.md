# Ordinal for Ghast

## 简介 / Overview

通过 Ordinal 官方 OAuth MCP 连接器起草和排期社媒帖子、分析表现并管理审批。

Draft and schedule social posts, analyze performance and manage approvals with Ordinal’s official OAuth MCP connector.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Ordinal OAuth 授权；受账号权限与服务配额限制。 已验证 OAuth 发现及 S256 授权跳转；未测试账号登录与业务操作。 使用新的用户 OAuth 入口，不使用已迁移的工作区 API Key MCP。

Connect in Ghast and complete Ordinal OAuth in the provider browser page. Account permissions and service quotas apply. OAuth discovery and the S256 authorization redirect were verified; account sign-in and business operations were not tested. Uses the new user OAuth endpoint, not the retired workspace API-key MCP.

- MCP: `https://app.tryordinal.com/mcp`
- [官方文档 / Provider documentation](https://docs.tryordinal.com/mcp/introduction)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.tryordinal.com/apple-icon.png
