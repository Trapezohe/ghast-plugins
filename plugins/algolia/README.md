# Algolia for Ghast

## 简介 / Overview

查看与管理 Algolia 搜索工作流，并通过 DocSearch 检索公开开发文档。

Inspect and manage Algolia search workflows and search public developer documentation with DocSearch.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Algolia OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Algolia OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.algolia.com/mcp`
- MCP: `https://mcp.algolia.com/1/docsearch/mcp`
- [官方文档 / Provider documentation](https://www.algolia.com/doc/guides/model-context-protocol/productivity-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.algolia.com/files/live/sites/algolia-assets/files/icons/algolia-logo-for-favicon.svg

Algolia Productivity MCP 需先在控制台启用并登录授权；DocSearch 为公开文档检索，无需账号。

Enable Productivity MCP in the dashboard and authorize your account. DocSearch searches public documentation without account access.

DocSearch official reference: https://docsearch.algolia.com/docs/mcp/overview/
