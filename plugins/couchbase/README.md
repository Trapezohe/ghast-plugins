# Couchbase for Ghast

## 简介 / Overview

通过 Couchbase 官方 MCP 检查数据结构、查询文档并分析集群健康情况。

Inspect Couchbase schemas, query documents and analyze cluster health with the official MCP server.

## 连接 / Connection

需要 uv/uvx、Python 3.12 和 Couchbase 7.6+ Operational 集群。在 Ghast 连接凭据中填写连接字符串、数据库用户名与密码。TLS 使用 couchbases://，按部署要求配置 Capella 网络访问。默认只读，日志输出至 stderr。 需要支持 stdio credentialEnv 的 Ghast 版本。

Requires uv/uvx, Python 3.12 and a Couchbase 7.6+ operational cluster. Enter the connection string, database username and password in Ghast connection credentials. Use couchbases:// for TLS, and configure Capella network access as appropriate. Starts read-only and logs to stderr. Requires a Ghast build with stdio credentialEnv support.

- MCP: `uvx --python 3.12 couchbase-mcp-server==1.0.1.post1 --read-only-mode=true --log-sinks=stderr`
- [官方文档 / Provider documentation](https://mcp-server.couchbase.com/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/605755?v=4
