# Clockify for Ghast

## 简介 / Overview

连接 Clockify 官方 MCP 预览服务，进行时间记录、项目查询与报表分析；服务商文档仍标注即将推出。

Connect Clockify’s official MCP preview for time tracking, project lookup and reports; provider documentation still marks the service as coming soon.

## 连接 / Connection

在 Clockify 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 x-api-key 请求头。不要在聊天中发送凭据，使用受服务配额限制。 在 Clockify 的 Preferences > Advanced > Manage API keys 生成个人 API Key，填入 Ghast 连接凭据输入框。服务继承用户的工作区权限。公开文档仍标注 COMING SOON，但官方端点目前可以启动并列出 13 个工具；可用性与工具覆盖范围可能变化。测试 Key 读取个人信息返回明确的 401 无效凭据错误。未测试真实账号数据、计时器修改或报表。

Create a Clockify API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the x-api-key header; do not paste credentials into chat. Service quotas apply. Generate a personal API key in Clockify Preferences > Advanced > Manage API keys and enter it in Ghast’s connection credential field. The service inherits the user’s workspace permissions. The public documentation says COMING SOON, although the official endpoint currently starts and exposes 13 tools; availability and tool coverage may change. Fixture-key profile retrieval returned an explicit 401 invalid-key error. No real account data, timer changes or reports were tested.

- MCP: `https://api.clockify.me/mcp-server/mcp`
- [官方文档 / Provider documentation](https://clockify.me/help/integrations-and-add-ons/use-clockify-mcp-server-to-connect-to-ai-agent)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://clockify.me/apple-touch-icon.png
