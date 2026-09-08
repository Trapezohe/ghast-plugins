# Meteomatics for Ghast

## 简介 / Overview

通过 Meteomatics 官方 MCP 查询天气预报和历史数据，支持位置、能源、物流与气候分析。

Query weather forecasts and historical data for location, energy, logistics and climate analysis through Meteomatics’ official MCP.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Meteomatics OAuth 授权；受账号权限与服务配额限制。 在服务商网页使用 Meteomatics API 账号登录。可用数据集、模型和时间范围取决于账号订阅。OAuth 发现和 S256 跳转已通过，未测试账号授权与天气数据查询。

Connect in Ghast and complete Meteomatics OAuth in the provider browser page. Account permissions and service quotas apply. Sign in on the provider page using your Meteomatics API account. Available datasets, models and time ranges depend on the account subscription. OAuth discovery and S256 redirect passed; account authorization and weather queries were not tested.

- MCP: `https://mcp.meteomatics.com/mcp`
- [官方文档 / Provider documentation](https://www.meteomatics.com/en/api/data-connectors/mcp/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/34451437?v=4
