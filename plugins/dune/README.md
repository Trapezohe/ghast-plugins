# Dune for Ghast

## 简介 / Overview

检索链上数据集，执行 Dune SQL 并分析链上活动。

Research on-chain datasets and execute Dune SQL analytics.

## 连接 / Connection

在 Dune 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 x-dune-api-key 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a Dune API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the x-dune-api-key header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://api.dune.com/mcp/v1`
- [官方文档 / Provider documentation](https://dune.com/blog/dune-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://mintlify.s3.us-west-1.amazonaws.com/dune/_generated/favicon/apple-touch-icon.png?v=3


## Browser authorization / 浏览器授权

`dune` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. The service advertises dynamic registration or client metadata documents. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。服务公开提供动态注册或客户端元数据文档支持。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [dune resource metadata](https://api.dune.com/.well-known/oauth-protected-resource) · [authorization metadata](https://dune.com/.well-known/oauth-authorization-server/oauth/mcp)
