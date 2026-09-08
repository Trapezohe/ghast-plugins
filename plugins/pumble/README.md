# Pumble for Ghast

## 简介 / Overview

连接 Pumble 官方 MCP，查找工作区对话、总结讨论串并执行已授权的协作操作。

Connect Pumble’s official MCP to find workspace conversations, summarize threads and perform authorized collaboration actions.

## 连接 / Connection

在 Pumble 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 token 请求头。不要在聊天中发送凭据，使用受服务配额限制。 在 Pumble 的 Workspace settings > Configure apps 中从零创建应用，选择所需用户或机器人权限并安装。将 App key 填入 x-app-token 凭据字段，将用户 Token 或机器人 Token 填入 token 字段。这是两个独立值，不使用其他客户端的 OAuth 凭据。可用操作受权限范围和工作区权限约束。官方端点在初始化时以 Invalid token claims 拒绝测试凭据；未测试已认证工具发现或真实消息。

Create a Pumble API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the token header; do not paste credentials into chat. Service quotas apply. In Pumble Workspace settings > Configure apps, create an app from scratch, select the needed user/bot scopes and install it. Enter its App key in the x-app-token credential field and either its user token or bot token in the token field. These are separate values, not OAuth credentials borrowed from another client. Scope and workspace permissions control available actions. The official endpoint rejected fixture credentials during initialization with Invalid token claims; authenticated tool discovery and real messages were not tested.

- MCP: `https://mcp.pumble.com/mcp`
- [官方文档 / Provider documentation](https://pumble.com/help/integrations/automation-workflow-integrations/how-to-use-the-pumble-mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://pumble.com/assets/images/favicons/apple-touch-icon.png
