# Brevo for Ghast

## 简介 / Overview

在 Brevo 中管理联系人、邮件活动、模板、CRM 记录与营销分析。

Manage contacts, email campaigns, templates, CRM records and marketing analytics in Brevo.

## 连接 / Connection

在 Brevo 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a Brevo API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://mcp.brevo.com/v1/brevo/mcp`
- [官方文档 / Provider documentation](https://help.brevo.com/hc/en-us/articles/27978590646802-What-is-Model-Context-Protocol-MCP)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://corp-backend.brevo.com/wp-content/uploads/2025/07/Brevo_logo.svg

创建密钥时需要启用 Create MCP server API key 选项；普通 API Key 无法替代专用 MCP Key。

Enable Create MCP server API key when creating the key; an ordinary API key is not a substitute.

验证涵盖官方端点、认证元数据与本地安装/卸载；未使用真实账号验证业务读写。

Validation covers the official endpoint, auth metadata and local install/removal. Business reads and writes with real accounts have not been tested.


## Browser authorization / 浏览器授权

`brevo` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. The service advertises dynamic registration or client metadata documents. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。服务公开提供动态注册或客户端元数据文档支持。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [brevo resource metadata](https://mcp.brevo.com/.well-known/oauth-protected-resource/v1/brevo/mcp) · [authorization metadata](https://mcp.brevo.com/.well-known/oauth-authorization-server/oauth)
