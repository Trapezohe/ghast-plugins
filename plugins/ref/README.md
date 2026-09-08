# Ref for Ghast

## 简介 / Overview

通过 Ref 精准检索和阅读技术文档。

Search and read focused technical documentation with Ref.

## 连接 / Connection

在 Ref 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 x-ref-api-key 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a Ref API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the x-ref-api-key header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://api.ref.tools/mcp`
- [官方文档 / Provider documentation](https://docs.ref.tools/context/install/index)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://docs.ref.tools/mintlify-assets/_mintlify/favicons/ref/dS8wJGyZzUbcN0Fx/_generated/favicon/android-chrome-192x192.png


## Browser authorization / 浏览器授权

`ref` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. The service advertises dynamic registration or client metadata documents. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。服务公开提供动态注册或客户端元数据文档支持。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [ref resource metadata](https://api.ref.tools/.well-known/oauth-protected-resource/mcp) · [authorization metadata](https://ref.scalekit.com/.well-known/oauth-authorization-server/resources/res_100246322321295106)
