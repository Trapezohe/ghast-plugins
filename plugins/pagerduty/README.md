# PagerDuty for Ghast

## 简介 / Overview

查看 PagerDuty 事件、服务与值班信息，并管理事件响应。

Inspect incidents, services and on-call context and manage incident response in PagerDuty.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 PagerDuty OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete PagerDuty OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.pagerduty.com/mcp`
- [官方文档 / Provider documentation](https://support.pagerduty.com/main/docs/pagerduty-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.pagerduty.com/favicon/prod/favicon.png

在 PagerDuty 创建 OAuth 应用，登记 Ghast 显示的回调 URL，在插件连接页配置 Client ID、Client Secret 和所需 scopes 后授权。

Create a PagerDuty OAuth app, register the callback URL shown by Ghast, then configure Client ID, Client Secret and required scopes in the plugin connection page.

验证包括官方端点认证响应、OAuth 发现和本地安装/卸载；未使用真实账号验证业务调用。

Validation covers official endpoint auth responses, OAuth discovery and local install/removal. Business calls using a real account have not been tested.
