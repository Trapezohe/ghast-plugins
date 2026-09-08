# Adobe Analytics for Ghast

## 简介 / Overview

连接 Adobe 官方 Analytics 与 Customer Journey Analytics MCP 服务，查询报表、分析趋势并管理分析组件。

Connect Adobe’s official Analytics and Customer Journey Analytics MCP servers to query reports, explore trends and manage analytics components.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Adobe Analytics OAuth 授权；受账号权限与服务配额限制。 按需分别连接两个服务，通过 Adobe ID 网页授权并选择目标 IMS 组织。管理员需为用户分配包含 MCP Access 的产品配置文件及底层产品权限；产品管理员同样需要这些权限。本包使用交互式 OAuth，不采用另外的服务到服务凭据流程。两个端点均已验证到 Adobe 的 S256 PKCE 授权页面，未测试用户同意授权、Token 交换、账号工具发现、报表或组件修改。

Connect in Ghast and complete Adobe Analytics OAuth in the provider browser page. Account permissions and service quotas apply. Connect each desired service separately using Adobe ID browser authorization, selecting the intended IMS organization. An administrator must assign the user a product profile with MCP Access as well as the underlying product permissions; this also applies to product administrators. This package uses interactive OAuth, not the separate server-to-server credential flow. Both endpoints reached Adobe’s S256 PKCE authorization page before consent. Token exchange, account tool discovery, reports and component changes were not tested.

- MCP: `https://aa-mcp.adobe.io/mcp`
- Customer Journey Analytics MCP: `https://cja-mcp.adobe.io/mcp`
- [官方文档 / Provider documentation](https://developer.adobe.com/analytics-mcp/docs/guides/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/36018178?v=4
