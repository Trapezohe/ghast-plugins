# Telnyx for Ghast

## 简介 / Overview

通过 Telnyx 官方 MCP 查询 API 操作，管理语音、消息和电话号码资源。

Discover Telnyx API actions and manage voice, messaging and phone-number resources through the official MCP server.

## 连接 / Connection

在 Telnyx 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 公开工具发现可能无需凭据；账号 API 调用需要 Telnyx API Key。内嵌 MCP 应用视图需要客户端支持。

Create a Telnyx API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. Public tool discovery may work without credentials; account API calls require your Telnyx API key. Embedded MCP app views require client support.

- MCP: `https://api.telnyx.com/v2/mcp`
- [官方文档 / Provider documentation](https://developers.telnyx.com/docs/development/mcp/remote-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://telnyx.com/favicon.ico
