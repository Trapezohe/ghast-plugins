# Remote for Ghast

## 简介 / Overview

连接 Remote 官方 MCP，查询人员、薪资和休假数据，并执行获授权的员工自助操作。

Connect Remote’s official MCP to explore workforce, payroll and leave data and perform authorized employee self-service.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Remote OAuth 授权；受账号权限与服务配额限制。 使用 Remote 雇主或员工账号连接，工具可见性遵循账号权限，无需手动配置 OAuth Scope 或 API Key。生产与沙箱分别连接，两者已验证到 S256 PKCE 网页授权跳转；未测试 Token 交换、员工数据读取或自助写入。

Connect in Ghast and complete Remote OAuth in the provider browser page. Account permissions and service quotas apply. Use your Remote employer or employee account. Tool visibility follows account permissions; no manual OAuth scopes or API key are required. Production and sandbox are separate connections. Both reached S256 PKCE browser redirects; token exchange, employee data and self-service writes were not tested.

- Sandbox MCP: `https://mcp.remote-sandbox.com/mcp`
- MCP: `https://mcp.remote.com/mcp`
- [官方文档 / Provider documentation](https://developer.remote.com/docs/quick-start-guide-2)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/88157212?v=4
