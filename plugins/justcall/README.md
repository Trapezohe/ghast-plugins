# JustCall for Ghast

## 简介 / Overview

通过 JustCall 官方 MCP 处理通话、消息、联系人、坐席状态、分析及已授权的销售沟通工作流。

Use JustCall’s official MCP for calls, messages, contacts, agent availability, analytics and authorized sales communication workflows.

## 连接 / Connection

在 JustCall 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 在 justcall-token 凭据输入框按 API_KEY:API_SECRET 格式填写自己的 API Key 与 API Secret，无需 Bearer 前缀，Ghast 会注入前缀和请求头。不要将凭据放入 URL 或聊天。官方服务使用测试凭据可发现 66 个工具，但只读 list_users 调用返回了 HTTP 401 文本且没有 isError 标志。因此发现工具不代表账号授权成功，未测试真实账号、消息或通话。

Create a JustCall API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. Enter your own API key and API secret together as API_KEY:API_SECRET in the justcall-token credential field, without the Bearer prefix; Ghast supplies the prefix and header. Never place credentials in a URL or chat. The official server exposed 66 tools with fixture credentials, but a read-only list_users call returned HTTP 401 as text without isError. Tool discovery therefore does not prove account authorization; no real account, message or call was tested.

- MCP: `https://mcp.justcall.host/mcp`
- [官方文档 / Provider documentation](https://developer.justcall.io/docs/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.justcall.io/assets-marketing/images/favicon.png
