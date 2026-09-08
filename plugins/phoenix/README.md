# Arize Phoenix for Ghast

## 简介 / Overview

通过 Phoenix 官方 MCP 查看项目、调用追踪、会话和实验，管理提示词与评测数据集。

Inspect Phoenix projects, traces, sessions and experiments, and manage prompts and evaluation datasets through the official MCP server.

## 连接 / Connection

需要 Node.js 和 npx。从实例设置复制完整 Phoenix API 实例地址至 PHOENIX_ENDPOINT，将对应 API Key 填入 PHOENIX_API_KEY。地址须包含实例提供的云空间路径，不能用通用官网地址代替。本插件面向需要认证的实例，使用明确填写的连接字段，不自动发现 .env.phoenix 文件。需要支持 stdio credentialEnv 的 Ghast 版本。

Requires Node.js and npx. Copy the complete Phoenix API instance endpoint from your instance settings into PHOENIX_ENDPOINT, and its API key into PHOENIX_API_KEY. Include any cloud space path shown by your instance; a generic website URL does not identify your API instance. This plugin supports authenticated instances and uses explicit connection fields instead of discovering .env.phoenix files. Requires Ghast stdio credentialEnv support.

- MCP: `npx -y @arizeai/phoenix-mcp@4.3.7`
- [官方文档 / Provider documentation](https://arize.com/docs/phoenix/sdk-api-reference/typescript/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://raw.githubusercontent.com/Arize-ai/phoenix/main/api_reference/source/_static/logo.png
