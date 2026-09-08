# Microsoft Work IQ for Ghast

## 简介 / Overview

通过微软官方 Work IQ MCP 检索和处理 Microsoft 365 邮件、会议、文件与 Teams 工作上下文。需要租户配置和自有 Entra 应用。

Search and work with Microsoft 365 mail, meetings, files and Teams context through Microsoft’s official Work IQ MCP. Requires tenant setup and your own Entra app.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Microsoft Work IQ OAuth 授权；受账号权限与服务配额限制。 需要自有 Microsoft Entra 多租户应用，配置 WorkIQAgent.Ask 委托权限并取得租户管理员同意。按原生公共客户端登记 Ghast 显示的准确回调地址，在 Ghast 填入该应用的 Client ID；此公共客户端的 Client Secret 留空。本包不内置 Microsoft 或 Copilot 的客户端身份，也不支持动态注册。管理员还需启用 Work IQ，配置适用的 Copilot Credits 计费与用户访问。Ghast 使用服务端发现的 organizations 登录地址与权限范围，请使用用户所属租户账号登录，会话过期后重新连接。需要 Ghast 静态 OAuth 配置支持。包验证未访问租户数据，也未验证最终令牌交换。

Connect in Ghast and complete Microsoft Work IQ OAuth in the provider browser page. Account permissions and service quotas apply. Requires your own Microsoft Entra multitenant app registration with delegated WorkIQAgent.Ask permission and tenant admin consent. Register the exact Ghast callback URI for a native public client, enter that app’s Client ID in Ghast, and leave Client Secret empty for that public client. No Microsoft or Copilot client identity is bundled; dynamic registration is unsupported. The tenant administrator must enable Work IQ and configure applicable Copilot Credits billing and user access. Ghast uses the server-discovered organizations authority and scope; sign in with the user’s home tenant, and reconnect if the session expires. Requires Ghast static OAuth configuration support. Tenant data and final token exchange have not been exercised in package validation.

- MCP: `https://workiq.svc.cloud.microsoft/mcp`
- [官方文档 / Provider documentation](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/overview)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/microsoft.svg
