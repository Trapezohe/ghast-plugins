# Plaid Dashboard for Ghast

## 简介 / Overview

连接 Plaid 官方 Dashboard MCP，诊断生产集成、分析 Link 转化并查询使用指标。

Connect Plaid’s official Dashboard MCP for production integration diagnostics, Link conversion analysis and usage metrics.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Plaid Dashboard OAuth 授权；受账号权限与服务配额限制。 团队须至少获批一个 Plaid 产品的生产访问权限。Dashboard 服务仅处理生产数据，目前处于持续开发阶段，服务商支持有限。Ghast 浏览器 OAuth 已验证到 S256 PKCE 跳转；未测试账号授权、Token 交换或诊断工具。本插件未配置文档中另述的 client_credentials 流程。

Connect in Ghast and complete Plaid Dashboard OAuth in the provider browser page. Account permissions and service quotas apply. Requires team approval for Production access to at least one Plaid product. This Dashboard service works only with Production data and is under active development with limited provider support. Ghast browser OAuth reached an S256 PKCE redirect; account authorization, token exchange and diagnostic tools were not tested. The separately documented client_credentials flow is not configured by this plugin.

- MCP: `https://api.dashboard.plaid.com/mcp/`
- [官方文档 / Provider documentation](https://plaid.com/docs/resources/mcp/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/3579888?v=4
