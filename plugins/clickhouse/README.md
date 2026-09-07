# ClickHouse Cloud for Ghast

## 简介 / Overview

探索 ClickHouse Cloud 数据与分析上下文，辅助 SQL 查询、指标分析和报表工作。

Explore ClickHouse Cloud data and analytical context and assist with SQL-based reporting.

## 连接 / Connection

通过浏览器 OAuth 连接 ClickHouse Cloud，数据访问受账号和服务配置限制。

Connect ClickHouse Cloud using browser OAuth. Access is limited by the connected account and configured services.

- MCP endpoint: `https://mcp.clickhouse.cloud/mcp`
- [Provider documentation / 官方文档](https://github.com/ClickHouse/agentic-data-stack/blob/main/librechat.yaml)
- 安装后在 Ghast 插件详情连接服务；安装成功不代表账号授权或业务调用成功。
- Install in the Ghast plugin store, then connect in the detail page. Installation does not prove account authorization or task execution.
- 本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 插件、私有连接器 ID 或账号凭据。
- Independently authored for Ghast using the provider's public MCP service. No Codex packages, private connector IDs or credentials are included.
- 如需撤销授权，请同时检查服务商账号的授权设置。To revoke provider access, also review connected applications in your provider account.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Service names and brand assets belong to their respective owners. 品牌标识归相应权利人所有。

Brand logo source: https://cdn.simpleicons.org/clickhouse/181818
