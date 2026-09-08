# Checkly for Ghast

## 简介 / Overview

在 Checkly 中查看监控检查、测试结果与事件，并运行已有检查。

Inspect monitoring checks, test results and incidents, and trigger existing checks in Checkly.

## 连接 / Connection

在 Checkly 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a Checkly API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://api.checklyhq.com/mcp`
- [官方文档 / Provider documentation](https://www.checklyhq.com/docs/ai/mcp-server/setup/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.checklyhq.com/apple-touch-icon.png

使用当前 cu_ 用户 Key 或 sv_ 服务 Key，旧版 sk_ Key 不支持。Ghast 使用 API Key 接入。

Use a current cu_ user or sv_ service key. Legacy sk_ keys are unsupported. Ghast uses API-key access.

验证包括公开端点响应、认证发现和本地安装/卸载；未验证真实账号的业务读写。

Validation covers public endpoint responses, auth discovery and local install/removal. Business reads and writes using a real account have not been tested.


## Browser authorization / 浏览器授权

`checkly` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. The service advertises dynamic registration or client metadata documents. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。服务公开提供动态注册或客户端元数据文档支持。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [checkly resource metadata](https://api.checklyhq.com/.well-known/oauth-protected-resource/mcp) · [authorization metadata](https://auth.checklyhq.com/.well-known/oauth-authorization-server)
