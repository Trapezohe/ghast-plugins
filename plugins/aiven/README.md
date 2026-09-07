# Aiven for Ghast

## 简介 / Overview

管理 Aiven 数据服务，包括 PostgreSQL 与 Kafka，并查看指标、日志和配置。

Manage Aiven data services, including PostgreSQL and Kafka, and inspect metrics, logs and configuration.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Aiven OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Aiven OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.aiven.live/mcp`
- [官方文档 / Provider documentation](https://aiven.io/docs/tools/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://aiven.io/favicons/apple-touch-icon.png
