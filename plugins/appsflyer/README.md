# AppsFlyer for Ghast

## 简介 / Overview

分析广告归因、安装量、ROAS、用户终身价值与营销表现。

Analyze campaign attribution, installs, ROAS, lifetime value and marketing performance.

## 连接 / Connection

在 AppsFlyer 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 使用 Security Center 中创建的 AppsFlyer MCP Token；当前服务为 Beta。

Create a AppsFlyer API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. Use an AppsFlyer MCP token from Security Center. The service is in beta.

- MCP: `https://mcp.appsflyer.com/auth/mcp`
- [官方文档 / Provider documentation](https://support.appsflyer.com/hc/en-us/articles/36349070304785--Beta-AppsFlyer-MCP)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.appsflyer.com/wp-content/uploads/2025/11/cropped-54649.-New-Website-favicon-192x192.png


## Browser authorization / 浏览器授权

`appsflyer` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. The service advertises dynamic registration or client metadata documents. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。服务公开提供动态注册或客户端元数据文档支持。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [appsflyer resource metadata](https://mcp.appsflyer.com/.well-known/oauth-protected-resource/auth/mcp) · [authorization metadata](https://mcp.appsflyer.com/.well-known/oauth-authorization-server)
