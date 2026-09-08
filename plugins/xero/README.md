# Xero for Ghast

## 简介 / Overview

连接 Xero 官方 MCP，处理会计记录、发票、联系人、财务报表和工资办公流程。

Connect Xero’s official MCP for accounting records, invoices, contacts, financial reports and payroll workflows.

## 连接 / Connection

需要 Node.js 18 或更高版本。为一个组织创建并授权 Xero Custom Connection，将 Client ID 和 Client Secret 填入 Ghast 连接输入框。按连接创建日期遵循官方权限范围要求；本包采用服务端默认范围。不要在聊天中发送凭据。Custom Connection 适用于澳大利亚、新西兰、英国和美国的组织，需要额外月度订阅；开发时可免费使用 Demo Company。这不是 Ghast 一键 OAuth 应用。 官方服务端使用测试凭据成功启动并列出 51 个工具。测试读取返回 invalid_client 错误文本，未设置 isError 标志，因此需同时检查错误内容与协议状态。工具发现不代表账号授权成功；未测试真实会计数据或写入操作。当前资格和计费规则见 https://developer.xero.com/documentation/guides/oauth2/custom-connections/ 。

Use Node.js 18 or later. Create and authorize a Xero Custom Connection for one organization, then enter its Client ID and Client Secret in Ghast connection fields. Follow the official scope requirements for the connection creation date; this package uses the server’s default scopes. Do not send credentials in chat. Custom Connections are available for organizations in Australia, New Zealand, the UK and the US, with an additional monthly subscription; a Demo Company can be used free for development. This is not a Ghast one-click OAuth application. The official server started with fixture credentials and exposed 51 tools. A fixture read returned invalid_client as plain error text without an isError flag; inspect error content as well as protocol status. Discovery does not prove account authorization; no real accounting data or writes were tested. See https://developer.xero.com/documentation/guides/oauth2/custom-connections/ for current eligibility and pricing.

- MCP: `npx -y @xeroapi/xero-mcp-server@0.0.17`
- [官方文档 / Provider documentation](https://github.com/XeroAPI/xero-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/242786?v=4
