# SingleStore for Ghast

## 简介 / Overview

通过 SingleStore 官方 MCP 探索 Helios 工作区、数据库、笔记本、任务与用量。

Explore SingleStore Helios workspaces, databases, notebooks, jobs and usage with the official MCP server.

## 连接 / Connection

需要 uv/uvx 与 Python 3.12。在 Ghast 连接凭据填写 SingleStore Helios 管理 API Key。本包使用官方 API Key 接入路径。固定 MCP Python SDK 1.29.1，因为该服务仍使用 FastMCP 1.x 接口，无法在 SDK 2.x 下启动。 需要支持 stdio credentialEnv 的 Ghast 版本。

Requires uv/uvx and Python 3.12. Enter a SingleStore Helios management API key in Ghast connection credentials. The package uses the official API-key path. MCP Python SDK 1.29.1 is pinned because this server still uses FastMCP 1.x APIs and cannot start with SDK 2.x. Requires a Ghast build with stdio credentialEnv support.

- MCP: `uvx --python 3.12 --with mcp==1.29.1 singlestore-mcp-server==0.4.19 start`
- [官方文档 / Provider documentation](https://docs.singlestore.com/cloud/ai/singlestore-mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.singlestore.com/icons/icon-512x512.png?v=277b9cbbe31e8bc416504cf3b902d430
