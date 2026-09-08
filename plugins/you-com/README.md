# You.com for Ghast

## 简介 / Overview

通过 You.com 官方 MCP 搜索网页、提取内容并使用研究工具，也可连接免登录搜索服务。

Search the web, retrieve content and use research tools through You.com’s official MCP, with an optional free search connection.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 You.com OAuth 授权；受账号权限与服务配额限制。 主连接使用 OAuth；可选的免费连接无需登录，受服务商每日限额限制，工具集合与账号连接不同，不提供完整研究与账号功能。

Connect in Ghast and complete You.com OAuth in the provider browser page. Account permissions and service quotas apply. The main connection uses OAuth. The optional free connection needs no login and is subject to provider daily limits; its tool set differs from the authenticated service. It does not provide the full research or account tool set.

- MCP: `https://api.you.com/mcp`
- MCP: `https://api.you.com/mcp?profile=free`
- [官方文档 / Provider documentation](https://you.com/docs/build-with-agents/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/229386092?v=4
