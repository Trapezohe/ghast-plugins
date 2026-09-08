# Everhour for Ghast

## 简介 / Overview

连接 Everhour 官方 MCP，管理计时器、工时记录、时间表，查询项目并跟踪团队工作。

Connect Everhour’s official MCP for timers, time entries, timesheets, project lookup and team work tracking.

## 连接 / Connection

在 Everhour 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 x-api-key 请求头。不要在聊天中发送凭据，使用受服务配额限制。 从 Everhour > My Profile > API key 获取个人 API Key，填入 Ghast 连接输入框，不要发送到聊天中。访问受账号权限和服务套餐约束。官方端点在初始化时以 403 Access denied 拒绝测试凭据；未测试已认证工具发现、时间表读取或计时器写入。

Create a Everhour API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the x-api-key header; do not paste credentials into chat. Service quotas apply. Copy your personal API key from Everhour > My Profile > API key into the Ghast connection field. Keep it out of chat. Access follows your account permissions and service plan. The official endpoint rejected fixture credentials at initialization with 403 Access denied; authenticated tool discovery, timesheets and timer writes were not tested.

- MCP: `https://api.everhour.com/mcp`
- [官方文档 / Provider documentation](https://support.everhour.com/article/618-connecting-with-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://everhour.com/assets/images/apple-touch-icon.png


## Browser authorization / 浏览器授权

`everhour` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. The service advertises dynamic registration or client metadata documents. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。服务公开提供动态注册或客户端元数据文档支持。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [everhour resource metadata](https://api.everhour.com/.well-known/oauth-protected-resource/mcp) · [authorization metadata](https://api.everhour.com/.well-known/oauth-authorization-server)
