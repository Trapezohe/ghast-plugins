# Turso for Ghast

## 简介 / Overview

通过 Turso 官方内置 MCP 检查本地 SQL 数据库、查询表，并执行已授权的数据或表结构变更。

Use Turso’s official built-in MCP to inspect local SQL databases, query tables and perform authorized data or schema changes.

## 连接 / Connection

先安装官方 Turso 数据库 CLI，并确保 PATH 中可找到 tursodb；已验证版本为 0.7.2。这里使用数据库程序 tursodb，而非另一个 turso Cloud CLI。默认数据库为插件数据目录中的 turso.db；可使用官方 open_database 工具选择已有数据库，并在操作前通过 current_database 确认。卸载或重置插件存储前，应备份有价值的本地数据。本地连接不需要账号 Token。 已核验官方 macOS arm64 发布包校验和；临时数据库实际通过建表、插入与 SELECT 测试，测试后已删除。

Install the official Turso database CLI and ensure tursodb is on PATH; version 0.7.2 was verified. This is the tursodb database executable, not the separate turso Cloud CLI. The default database is turso.db in this plugin’s data directory. Use the official open_database tool to select an existing database and verify current_database before operating on it. Keep backups of valuable local data before uninstalling or resetting plugin storage. No account token is required for this local connection. The official macOS arm64 release checksum was verified. A temporary database passed actual create-table, insert and SELECT operations and was removed after testing.

- MCP: `tursodb ${PLUGIN_DATA}/turso.db --mcp`
- [官方文档 / Provider documentation](https://github.com/tursodatabase/turso)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/139391156?v=4
