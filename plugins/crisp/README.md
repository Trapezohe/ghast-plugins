# Crisp for Ghast

## 简介 / Overview

查看 Crisp 工作区的客户对话、联系人与帮助中心文章。

Review customer conversations, contacts and helpdesk articles in your Crisp workspace.

## 连接 / Connection

在 Crisp 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 在 Crisp 设置 > 工作区设置 > 高级配置中生成 MCP Server Token，使用该授权值，不要直接填写 REST 密钥对。重新生成已有 Token 可能影响其他集成，应使用合适的现有 Token，或先与其负责人协调。

Create a Crisp API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. Generate a MCP Server Token under Crisp Settings > Workspace Settings > Advanced configuration. Use the MCP token authorization value, not a raw REST key pair. Regenerating existing tokens can affect other integrations, so reuse an appropriate existing token or coordinate with its owner.

- MCP: `https://api.crisp.chat/mcp/`
- [官方文档 / Provider documentation](https://docs.crisp.chat/guides/mcp-server/quickstart/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://crisp.chat/favicons/favicon-256x256.png
