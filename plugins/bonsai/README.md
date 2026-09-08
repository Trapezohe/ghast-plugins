# Bonsai for Ghast

## 简介 / Overview

连接 Bonsai 官方 MCP 测试版，在账号权限内管理任务、项目、CRM 资料、工时与发票。

Connect Bonsai’s official MCP beta to manage tasks, projects, CRM records, time entries and invoices within your account permissions.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Bonsai OAuth 授权；受账号权限与服务配额限制。 官方托管 MCP 处于测试版。OAuth 支持自动注册客户端，无需 API Key。访问继承公司角色权限，而非可选 scope；工具可见性和字段访问随角色变化。当前 MCP 能力尚未列出支付与报表。已验证到 PKCE 授权跳转，未测试 Token 交换、账号记录与财务操作。

Connect in Ghast and complete Bonsai OAuth in the provider browser page. Account permissions and service quotas apply. The official hosted MCP is in beta. OAuth supports automatic client registration; no API key is required. Access inherits your company role rather than selectable scopes, and tool visibility and field access follow that role. Payments and reports are not currently listed as MCP capabilities. Verification reached a PKCE redirect before consent; token exchange, account records and financial operations were not tested.

- MCP: `https://mcp.hellobonsai.com/mcp`
- [官方文档 / Provider documentation](https://docs.hellobonsai.com/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/67db1ca556342937e18be8b9/686550dfde2bc90752fbc987_Icon-512%20(1).png
