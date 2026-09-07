# Meilisearch for Ghast

## 简介 / Overview

通过 Meilisearch 官方 MCP 搜索文档并管理索引、相关性设置与索引任务。

Search documents and manage indexes, relevance settings and indexing tasks through Meilisearch’s official MCP.

## 连接 / Connection

需要 uv/uvx 与 Python 3.12。在 Ghast 连接凭据中填写 Meilisearch 实例地址及按操作范围授权的 API Key。虽然环境变量名为 MEILI_MASTER_KEY，日常搜索应使用受限 Key，避免使用主密钥。不要在聊天中发送凭据。 需要支持 stdio credentialEnv 的 Ghast 版本。

Requires uv/uvx and Python 3.12. Enter your Meilisearch instance URL and an API key scoped to the required operations in Ghast connection credentials. Despite the environment variable name MEILI_MASTER_KEY, avoid using the master key for routine search. Connection credentials should not be pasted into chat. Requires a Ghast build with stdio credentialEnv support.

- MCP: `uvx --python 3.12 meilisearch-mcp==0.7.0`
- [官方文档 / Provider documentation](https://www.meilisearch.com/integrations/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/43250847?v=4
