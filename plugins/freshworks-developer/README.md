# Freshworks Developer for Ghast

## 简介 / Overview

查看 Freshworks 自定义应用及版本，并管理应用包提交流程。

Inspect Freshworks custom apps and versions and manage app package submission workflows.

## 连接 / Connection

在 Freshworks Developer 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a Freshworks Developer API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://mcp.freshworks.dev/mcp`
- [官方文档 / Provider documentation](https://developers.freshworks.com/docs/agentic-dev-tools/mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://developers.freshworks.com/docs/favicon.ico

## Ghast 接入设置 / Ghast setup

从 Freshworks Application Management Portal 的设置中获取 Developer API Key，填入 Ghast 连接凭据。此服务管理开发者应用包，不是 Freshdesk/Freshservice 业务工单连接器。

Obtain the Developer API Key from Application Management Portal settings and enter it in Ghast. This service manages developer app packages; it is not a Freshdesk/Freshservice support-ticket connector.

验证涵盖官方端点认证响应、认证元数据和本地安装/卸载；未完成真实账号授权或业务调用。

Validation covers official endpoint auth responses, auth metadata and local install/removal. Real-account authorization and business calls have not been completed.
