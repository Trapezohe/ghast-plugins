# MongoDB for Ghast

## 简介 / Overview

浏览 MongoDB 集合、检查结构、执行查询并分析数据库性能。

Explore MongoDB collections, inspect schemas, run queries and analyze database performance.

## 连接 / Connection

需要 Node.js 22.13+ 或 24+ 与 npx。在 Ghast 连接设置中填写 MongoDB 数据库连接串，并使用具备任务所需权限的数据库用户。本包配置数据库直连，不配置 Atlas 管理 API 凭据。需要支持 credentialEnv 的 Ghast 版本；旧版本无法配置此连接。

Requires Node.js 22.13+ or 24+ and npx. Enter your MongoDB connection string in Ghast connection settings. Use a database user with the permissions needed for your task. This package configures direct database access, not Atlas Administration API credentials. Requires a Ghast build with credentialEnv support; older builds cannot configure this connection.

- MCP: `npx -y mongodb-mcp-server@2.1.1`
- [官方文档 / Provider documentation](https://www.mongodb.com/docs/mcp-server/local-mcp/configuration/options/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.mongodb.com/assets/images/global/favicon.ico
