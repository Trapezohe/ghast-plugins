# Teamwork for Ghast

## 简介 / Overview

在 Teamwork 中管理客户项目、任务、工时与客服工作流。

Manage client projects, tasks, time logs and help desk workflows in Teamwork.

## 连接 / Connection

使用官方 @teamwork/get-bearer-token 工具或 Teamwork 应用登录流程取得 Bearer Token，再填入 Ghast 连接凭据。这是 Teamwork OAuth 访问令牌，不是用于 Basic 认证的个人 API Key。详见 https://github.com/Teamwork/mcp/blob/main/docs/usage/teamwork-cli.md#get-a-bearer-token 。不要在聊天中发送令牌，访问受账号权限限制。

Use the official @teamwork/get-bearer-token helper or Teamwork app login flow to obtain a Bearer token, then enter it in Ghast connection credentials. This is a Teamwork OAuth access token, not a personal Basic-auth API key. See https://github.com/Teamwork/mcp/blob/main/docs/usage/teamwork-cli.md#get-a-bearer-token . Never paste tokens in chat. Access follows your account permissions.

- MCP: `https://mcp.ai.teamwork.com`
- [官方文档 / Provider documentation](https://github.com/Teamwork/mcp/blob/main/docs/usage/other-platforms.md)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn-website.teamwork.com/offload/app/uploads/2019/03/04183535/cropped-favicon-180x180.png


## Browser authorization / 浏览器授权

`teamwork` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. The service advertises dynamic registration or client metadata documents. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。服务公开提供动态注册或客户端元数据文档支持。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [teamwork resource metadata](https://mcp.ai.teamwork.com/.well-known/oauth-protected-resource) · [authorization metadata](https://teamwork.com/.well-known/oauth-authorization-server)
