# Pinecone for Ghast

## 简介 / Overview

管理 Pinecone 向量索引、写入记录、查询数据并搜索官方文档。

Manage Pinecone vector indexes, upsert records, query data and search official documentation.

## 连接 / Connection

需要 Node.js 22+ 与 npx。在 Ghast 插件连接设置中填写 Pinecone API Key，由 Ghast 注入官方本地 MCP 进程的 PINECONE_API_KEY 环境变量。需要支持 credentialEnv 的 Ghast 版本，旧版本无法配置此连接；受账号权限和服务计费限制。

Requires Node.js 22+ and npx. Enter your Pinecone API key in Ghast plugin connection settings. Ghast injects PINECONE_API_KEY into the official local MCP process. This requires a Ghast build with credentialEnv support; older builds cannot configure this connection. Account entitlements and usage charges apply.

- MCP: `npx -y @pinecone-database/mcp@0.3.0`
- [官方文档 / Provider documentation](https://docs.pinecone.io/guides/operations/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.pinecone.io/favicon.ico?favicon.16aah0kd0o17q.ico
