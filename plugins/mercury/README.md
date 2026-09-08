# Mercury for Ghast

## 简介 / Overview

通过 Mercury 官方只读 MCP 连接器分析余额、交易、对账单与支出（Beta）。

Analyze balances, transactions, statements and spending with Mercury’s official read-only MCP connector (Beta).

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Mercury OAuth 授权；受账号权限与服务配额限制。 已验证 OAuth 发现及 S256 授权跳转；未完成账号登录或私有数据操作。

Connect in Ghast and complete Mercury OAuth in the provider browser page. Account permissions and service quotas apply. OAuth discovery and the S256 authorization redirect were verified; no account sign-in or private data operations were performed.

- MCP: `https://mcp.mercury.com/mcp`
- [官方文档 / Provider documentation](https://docs.mercury.com/docs/connecting-mercury-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/288747831?v=4
