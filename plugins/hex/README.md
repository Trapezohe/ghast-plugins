# Hex for Ghast

## 简介 / Overview

搜索 Hex 项目，并通过 Hex Threads 会话探索和分析数据。

Search Hex projects and explore data through Hex Threads conversations.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Hex OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Hex OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://app.hex.tech/mcp`
- [官方文档 / Provider documentation](https://learn.hex.tech/docs/api-integrations/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://hex.tech/favicon.svg

需要 Team 或 Enterprise 套餐及 Explorer 或更高角色；服务处于 Beta。默认连接 app.hex.tech，EU、HIPAA 和独立租户需要专用域名。

Requires Team or Enterprise and Explorer role or higher. The service is beta. The default is app.hex.tech; EU, HIPAA and single-tenant workspaces require their specific domain.

验证包括官方端点认证响应、OAuth 发现和本地安装/卸载；未使用真实账号验证业务调用。

Validation covers official endpoint auth responses, OAuth discovery and local install/removal. Business calls using a real account have not been tested.
