# Deel for Ghast

## 简介 / Overview

通过 Deel 官方 MCP 访问员工、合同、休假与薪酬相关工具。

Access workforce, contract, time-off and payroll tools through Deel’s official MCP.

## 连接 / Connection

在 Deel 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 在 Deel 的 More > Developer > Apps 中生成仅包含所需权限的个人访问令牌，并填入 Ghast 连接凭据。本包使用官方支持的 PAT 方式。匿名可见工具不能证明已获得员工数据权限；受保护工具取决于 Token 与账号权限。

Create a Deel API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. Generate a personal access token under More > Developer > Apps in your Deel dashboard with only the scopes required by your work. Enter it in Ghast connection credentials. This package uses the officially supported PAT method. Anonymous tools do not prove access to your workforce data; protected tool availability depends on your token and permissions.

- MCP: `https://api.letsdeel.com/mcp`
- [官方文档 / Provider documentation](https://developer.deel.com/mcp/authorization)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.deel.com/apple-icon.png?d2b410d8d6714d15


## Browser authorization / 浏览器授权

`deel` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. The service advertises dynamic registration or client metadata documents. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。服务公开提供动态注册或客户端元数据文档支持。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [deel resource metadata](https://api.letsdeel.com/.well-known/oauth-protected-resource/mcp) · [authorization metadata](https://api.letsdeel.com/.well-known/oauth-authorization-server)
