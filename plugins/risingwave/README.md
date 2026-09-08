# RisingWave for Ghast

## 简介 / Overview

通过 RisingWave 官方 MCP 查询流式 SQL、检查表结构与作业，并管理已授权的数据库资源。

Connect through RisingWave’s official MCP to query streaming SQL, inspect schemas and jobs, and manage authorized database resources.

## 连接 / Connection

需要 uv 与 Python 3.12；首次连接时 uv 可能下载 Python 和已固定版本的依赖。在 Ghast 加密凭据中填写 PostgreSQL 协议的 RisingWave 连接串，并配置所需的 TLS 参数。本包包含提交 c148f80dae9070782bd4393c4a4b729e863e4718 的未修改官方源码，通过 stdio 运行，不安装数据库，也不要求 Cloud 账号。权限由数据库账号决定。首次依赖初始化可能较慢；如首次客户端连接超时，初始化结束后可重新连接。 实际启动发现 150 个工具，内置文档搜索成功。对不可用本地测试地址的查询在 15 秒后超时；未验证真实数据库查询或写入。

Requires uv and Python 3.12. uv may download Python and the pinned dependencies on first connection. Enter your PostgreSQL-compatible RisingWave connection string in Ghast encrypted credentials, including your chosen TLS settings. This package contains unchanged official source at commit c148f80dae9070782bd4393c4a4b729e863e4718. It starts over stdio from plugin data storage and does not install a database or require a Cloud account. The configured database account determines permissions. Initial dependency setup may take time; reconnect after setup if the first client attempt times out. Actual startup exposed 150 tools and bundled documentation search succeeded. A query against an unavailable local fixture endpoint timed out after 15 seconds; no real database query or write was verified.

- MCP: `uv run --no-project --no-config --python 3.12 --with fastmcp==4.0.3 --with risingwave-py==0.0.2 --with psycopg2-binary==2.9.12 python ${PLUGIN_ROOT}/upstream/src/main.py`
- [官方文档 / Provider documentation](https://github.com/risingwavelabs/risingwave-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/77175557?v=4
