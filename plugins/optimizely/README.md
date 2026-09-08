# Optimizely CMS for Ghast

## 简介 / Overview

连接 Optimizely 官方 CMS SaaS MCP，查看内容类型、审查内容并执行已授权的网站内容工作流。

Connect Optimizely’s official CMS SaaS MCP to inspect content types, audit content and perform authorized site content workflows.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Optimizely CMS OAuth 授权；受账号权限与服务配额限制。 需要 Opti ID 账号、已启用且连接 CMS SaaS 的 Opal 实例，并具有两者的访问权限。OAuth 时选择目标 Opal 实例，它可能关联多个 CMS 实例。无需单独创建 API Token。已验证到服务商 PKCE 授权跳转，未测试 Token 交换、账号内容或发布。

Connect in Ghast and complete Optimizely CMS OAuth in the provider browser page. Account permissions and service quotas apply. Requires an Opti ID account, an enabled Opal instance linked to CMS SaaS, and permission to both. Select the intended Opal instance during OAuth; it can expose multiple linked CMS instances. No separate API token is needed. Verification reached the provider PKCE redirect before consent; token exchange, account content and publishing were not tested.

- MCP: `https://cms.mcp.opal.optimizely.com/mcp`
- [官方文档 / Provider documentation](https://docs.developers.optimizely.com/content-management-system/v1.0.0-CMS-SaaS/docs/configure-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/1274132?v=4
