# SurrealDB for Ghast

## 简介 / Overview

管理 SurrealDB Cloud 实例、查询数据库并检查用量与诊断信息。

Manage SurrealDB Cloud instances, query databases and inspect usage and diagnostics.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 SurrealDB OAuth 授权；受账号权限与服务配额限制。 本插件连接托管 Cloud 服务，数据库操作要求实例运行且版本为 SurrealDB 3.1 或更高；受角色权限与云服务计费限制。

Connect in Ghast and complete SurrealDB OAuth in the provider browser page. Account permissions and service quotas apply. This is the hosted Cloud connector. Database operations require a running instance on SurrealDB 3.1 or later; roles and cloud service charges apply.

- MCP: `https://mcp.surrealdb.com`
- [官方文档 / Provider documentation](https://surrealdb.com/docs/build/ai-agents/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://surrealdb.com/assets/static/favicon.C76EUDBN.svg
