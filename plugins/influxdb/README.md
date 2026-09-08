# InfluxDB for Ghast

## 简介 / Overview

通过 InfluxDB 3 官方 MCP 查询时序数据、发现表结构和管理数据库，并连接独立的官方文档服务。

Connect to InfluxDB 3 through its official MCP for time-series queries, schema discovery and database administration, with a separate documentation service.

## 连接 / Connection

需要 Node.js >=20.11 和 npx。在 Ghast 连接字段中将 influxdb-product-type 设置为 core、enterprise、cloud-serverless、cloud-dedicated 或 clustered。Core、Enterprise 和 Serverless 需要实例 URL 与数据库 Token；Dedicated 需要集群 ID，加数据库 Token，或账号 ID 与管理 Token；Clustered 需要实例 URL，加数据库或管理 Token。标为可选的字段会按产品类型有条件必填，由官方服务验证组合。Token 仅填写在 Ghast 凭据中。默认 operator 模式按 Token 权限提供管理工具；若需要只读安装，在本地 MCP 配置中设置 INFLUX_MCP_TOOL_PROFILE=readonly。需要 Ghast 支持 credentialEnv 和 optionalCredentials。独立的 influxdb-docs 文档服务通过服务商使用的 Kapa 平台进行 Google 或 GitHub OAuth 授权。 本地验证以 Core 配置启动官方 MCP 并发现 27 个工具；本地模拟 HTTP 服务验证了 Bearer 请求头与 401 错误传递，未访问真实数据库。文档 OAuth 验证到授权页面跳转，未完成用户授权。

Requires Node.js >=20.11 and npx. In Ghast connection fields, set influxdb-product-type to core, enterprise, cloud-serverless, cloud-dedicated or clustered. Core, Enterprise and Serverless require your instance URL and database token. Dedicated requires a cluster ID plus either a database token, or an account ID and management token. Clustered requires its instance URL plus a database or management token. Fields marked optional are conditionally required by the selected product; the official server validates these combinations. Enter tokens only in Ghast credentials. The operator profile exposes administration tools according to token permissions. For a read-only installation, set INFLUX_MCP_TOOL_PROFILE=readonly in local MCP configuration. Requires Ghast credentialEnv and optionalCredentials support. The separate influxdb-docs service uses Google or GitHub OAuth through the provider’s Kapa-hosted documentation service. Local verification started the official MCP with Core configuration and discovered 27 tools. A local fixture HTTP server confirmed the bearer header and 401 propagation; no real database was accessed. Documentation OAuth reached the provider redirect before consent.

- MCP: `npx -y @influxdata/influxdb3-mcp-server@1.4.1`
- MCP: `https://influxdb-docs.mcp.kapa.ai`
- [官方文档 / Provider documentation](https://github.com/influxdata/influxdb3_mcp_server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/5713248?v=4
