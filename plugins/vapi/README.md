# Vapi for Ghast

## 简介 / Overview

通过 Vapi 官方 MCP 管理语音助手，查看通话和电话号码，并执行经授权的语音工作流。

Manage Vapi voice assistants, inspect calls and phone numbers, and perform authorized voice workflows with the official MCP server.

## 连接 / Connection

在 Vapi 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a Vapi API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://mcp.vapi.ai/mcp`
- [官方文档 / Provider documentation](https://docs.vapi.ai/sdk/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://vapi.ai/icon.svg?icon.05txosa6z_gu8.svg
