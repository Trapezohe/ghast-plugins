# Customer.io for Ghast

## 简介 / Overview

在 Customer.io 中查看客户旅程，管理活动、简报、分群与工作区数据。

Inspect customer journeys and manage campaigns, newsletters, segments and workspace data in Customer.io.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Customer.io OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Customer.io OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.customer.io/mcp`
- [官方文档 / Provider documentation](https://docs.customer.io/ai/mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://customer.io/favicon.svg

该包使用美国区域端点；欧盟工作区需使用官方 `https://mcp-eu.customer.io/mcp`。

This package targets the US region; EU workspaces require the official `https://mcp-eu.customer.io/mcp` endpoint.

验证涵盖官方端点、认证元数据与本地安装/卸载；未使用真实账号验证业务读写。

Validation covers the official endpoint, auth metadata and local install/removal. Business reads and writes with real accounts have not been tested.
