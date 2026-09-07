# Front for Ghast

## 简介 / Overview

搜索 Front 会话、查看客户上下文、准备回复草稿并管理收件箱工作流。

Search Front conversations, inspect customer context, prepare drafts and manage inbox workflows.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Front OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Front OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.frontapp.com/mcp`
- [官方文档 / Provider documentation](https://dev.frontapp.com/docs/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://front.com/apple-icon.png

## Ghast 接入设置 / Ghast setup

在 Front Settings > Company > Developer 中创建 OAuth 应用，只开启 MCP Server Feature access；按需设置 read、write、send 资源权限。登记 Ghast 显示的回调 URL，在 Ghast 填入 Client ID、Client Secret；OAuth scopes 填 feature:mcp。此服务为公开 Beta，不支持 DCR。

Create an OAuth app in Front Settings > Company > Developer. Enable only MCP Server under Feature access and select read/write/send resource permissions as needed. Register Ghast’s displayed callback URL; enter Client ID and Client Secret in Ghast and use feature:mcp as the OAuth scope. This open beta service does not support DCR.

验证涵盖官方端点认证响应、认证元数据和本地安装/卸载；未完成真实账号授权或业务调用。

Validation covers official endpoint auth responses, auth metadata and local install/removal. Real-account authorization and business calls have not been completed.
