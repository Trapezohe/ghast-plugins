# Qdrant for Ghast

## 简介 / Overview

向 Qdrant 存储知识，并通过语义搜索检索相关信息。

Store knowledge and retrieve relevant information from Qdrant using semantic search.

## 连接 / Connection

需要 uv、uvx 与 Python 3.12（uv 可自动准备 Python）。在 Ghast 连接设置中填写 Qdrant 集群 URL、API Key 与集合名称。官方服务使用 FastEmbed，首次使用可能下载默认 sentence-transformers/all-MiniLM-L6-v2 模型；集合必须与该模型的嵌入兼容。需要支持 credentialEnv 的 Ghast 版本；旧版本无法配置此连接。

Requires uv with uvx and Python 3.12 (uv can provision Python). Enter your Qdrant cluster URL, API key and collection name in Ghast connection settings. The official server uses FastEmbed and may download the default sentence-transformers/all-MiniLM-L6-v2 model on first use; the collection must match its embeddings. Requires a Ghast build with credentialEnv support; older builds cannot configure this connection.

- MCP: `uvx --python 3.12 mcp-server-qdrant==0.8.1`
- [官方文档 / Provider documentation](https://github.com/qdrant/mcp-server-qdrant)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://qdrant.tech/favicon/apple-touch-icon.png
