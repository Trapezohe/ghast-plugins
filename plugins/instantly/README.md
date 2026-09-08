# Instantly for Ghast

## 简介 / Overview

通过 Instantly 官方 MCP 管理邮件活动、销售线索、发件账号与效果数据。

Manage email campaigns, leads, sending accounts and performance through Instantly’s official MCP.

## 连接 / Connection

在 Instantly 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 x-instantly-api-key 请求头。不要在聊天中发送凭据，使用受服务配额限制。 需要具备目标操作权限范围的 API v2 Key 及开放 API 访问的账号。将 Key 填入 Ghast 连接凭据，使用官方 x-instantly-api-key 请求头。

Create a Instantly API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the x-instantly-api-key header; do not paste credentials into chat. Service quotas apply. Requires an API v2 key with the scopes needed by your workflow and an account with API access. Enter it in Ghast connection credentials; the official x-instantly-api-key header is used.

- MCP: `https://mcp.instantly.ai/mcp`
- [官方文档 / Provider documentation](https://developer.instantly.ai/mcp/authentication)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/63860c8c65e7bef4a1eeebeb/63f62e4d1df86f1bf7f133d5_cleaned_rounded.png


## Browser authorization / 浏览器授权

`instantly` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. The service advertises dynamic registration or client metadata documents. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。服务公开提供动态注册或客户端元数据文档支持。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [instantly resource metadata](https://mcp.instantly.ai/.well-known/oauth-protected-resource) · [authorization metadata](https://api.instantly.ai/.well-known/oauth-authorization-server)
