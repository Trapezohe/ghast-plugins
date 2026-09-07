# Tallyfy for Ghast

## 简介 / Overview

通过 Tallyfy 管理工作流任务、业务流程与审批。

Manage workflow tasks, business processes and approvals through Tallyfy.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Tallyfy OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Tallyfy OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.tallyfy.com/`
- [官方文档 / Provider documentation](https://tallyfy.com/products/pro/integrations/mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://tallyfy.com/favicon.svg

验证涵盖官方端点、认证元数据与本地安装/卸载；未使用真实账号验证业务读写。

Validation covers the official endpoint, auth metadata and local install/removal. Business reads and writes with real accounts have not been tested.
