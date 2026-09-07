# StarRocks for Ghast

## 简介 / Overview

浏览 StarRocks 数据结构、执行 SQL 并根据分析查询生成图表。

Explore StarRocks schemas, run SQL and create charts from analytical queries.

## 连接 / Connection

需要 uv/uvx 和 Python 3.12。Ghast 启动官方 mcp-server-starrocks==0.4.0 包。在 Ghast 连接凭据中按服务商格式 user:password@host:9030/database 填写 STARROCKS_URL，并使用具备所需操作权限的数据库账号。需要可访问的 StarRocks FE 服务，以及支持 stdio credentialEnv 的 Ghast 版本。

Requires uv/uvx and Python 3.12. Ghast launches the official mcp-server-starrocks==0.4.0 package. Enter STARROCKS_URL in Ghast connection credentials using the provider format user:password@host:9030/database. Use a database account scoped to the required operations. A reachable StarRocks FE service is required. Requires a Ghast build with stdio credentialEnv support.

- MCP: `uvx --python 3.12 --with fastmcp==2.14.5 mcp-server-starrocks==0.4.0`
- [官方文档 / Provider documentation](https://github.com/StarRocks/mcp-server-starrocks)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.starrocks.io/21782839.fs1.hubspotusercontent-na1.net/hubfs/21782839/dark_logo.svg

FastMCP is pinned to 2.14.5 because StarRocks 0.4.0 imports the FastMCP 2.x ToolResult module, which is absent in 3.x. 固定 FastMCP 2.14.5，以兼容 StarRocks 0.4.0 使用的 2.x ToolResult 模块。

The SVG viewport isolates the brand mark from the official full logo without changing its paths. SVG 视口仅截取官方完整 Logo 的品牌图形，未修改图形路径。
