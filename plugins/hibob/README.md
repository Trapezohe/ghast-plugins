# HiBob for Ghast

## 简介 / Overview

通过员工 OAuth 连接 HiBob 官方 MCP，处理人员、组织、休假与办公工作流。

Connect HiBob’s official MCP with employee OAuth for people, organization, time-off and workplace workflows.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 HiBob OAuth 授权；受账号权限与服务配额限制。 当前服务商版本采用已登录员工的 OAuth，并逐步向客户开放，取代部分旧页面仍展示的 Basic Auth 服务账号配置。此入口已返回官方 OAuth 资源元数据，并验证到 S256 PKCE 网页跳转；未测试 Token 交换、账号工具或人事操作。可用性与工具权限取决于 Bob 账号。

Connect in Ghast and complete HiBob OAuth in the provider browser page. Account permissions and service quotas apply. The current provider release uses signed-in employee OAuth and is rolling out to customers. It supersedes the older Basic Auth service-user setup still shown on some pages. This endpoint advertises the official OAuth resource and reached an S256 PKCE browser redirect. Token exchange, account tools and HR operations were not tested. Availability and tool access depend on your Bob account.

- MCP: `https://api.hibob.com/ai-mcp-public/mcp/public`
- [官方文档 / Provider documentation](https://apidocs.hibob.com/changelog/developer-docs-update-bob-mcp-server-now-uses-oauth)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://new.hibob.com/app/uploads/2026/05/cropped-HiBob-Logo-Icon-192x192.png

Official endpoint reference: https://www.hibob.com/platform/core/ai/mcp/ (authentication guidance superseded by the linked OAuth release).
