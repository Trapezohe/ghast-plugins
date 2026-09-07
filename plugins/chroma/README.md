# Chroma for Ghast

## 简介 / Overview

管理 Chroma Cloud 集合与文档、执行向量查询并检查存储数据。

Manage Chroma Cloud collections and documents, run vector queries and inspect stored data.

## 连接 / Connection

需要 uv、uvx 与 Python 3.12（uv 可自动准备 Python）。在 Ghast 连接设置中填写 Chroma Cloud 租户、数据库名称与 API Key。本包连接 Chroma Cloud，需要支持 credentialEnv 的 Ghast 版本；旧版本无法配置连接。嵌入操作可能下载模型，或需要另行配置嵌入服务。

Requires uv with uvx and Python 3.12 (uv can provision Python). Enter your Chroma Cloud tenant, database name and API key in Ghast connection settings. This package targets Chroma Cloud. Requires a Ghast build with credentialEnv support; older builds cannot configure the connection. Embedding operations may download models or require a separately configured embedding provider.

- MCP: `uvx --python 3.12 chroma-mcp==0.2.6 --client-type cloud`
- [官方文档 / Provider documentation](https://github.com/chroma-core/chroma-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.trychroma.com/img/favicon.ico
