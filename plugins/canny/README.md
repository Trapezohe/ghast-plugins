# Canny for Ghast

## 简介 / Overview

通过 Canny 官方 MCP 分析产品反馈与客户影响，并管理 Ideas；需要启用 Canny Ideas 的 Pro 或 Business 套餐。

Analyze product feedback and customer impact, and manage Ideas through Canny’s official MCP. Requires Pro or Business with Canny Ideas.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Canny OAuth 授权；受账号权限与服务配额限制。 需要 Pro 或 Business 套餐、启用 Canny Ideas，并由工作区 Owner 首先连接；之后成员按自身角色权限授权。已验证 Ghast OAuth 发现及 S256 跳转，未使用其他应用的客户端凭据；未测试账号登录与业务操作。

Connect in Ghast and complete Canny OAuth in the provider browser page. Account permissions and service quotas apply. Requires Pro or Business, Canny Ideas enabled, and a workspace Owner to connect first. Subsequent teammates use their own role permissions. Ghast OAuth discovery and S256 redirect were verified without using client credentials from another app; account sign-in and business operations were not tested.

- MCP: `https://api.canny.io/api/mcp/v1`
- [官方文档 / Provider documentation](https://help.canny.io/en/articles/13063190-canny-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/23064785?v=4
