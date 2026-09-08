# Anytype for Ghast

## 简介 / Overview

通过 Anytype 官方本地 MCP 连接器搜索和整理空间、对象、列表及知识资料。

Search and organize Anytype spaces, objects, lists and knowledge through Anytype’s official local MCP connector.

## 连接 / Connection

需要 Node.js、npx，以及正在运行并启用 API 的 Anytype 桌面应用。在 Anytype 设置 > API Keys 创建密钥，从官方生成的配置中复制 OPENAPI_MCP_HEADERS 的 JSON 对象，填入 Ghast 的同名连接凭据字段，保留 Authorization 和 Anytype-Version。仅填写该 JSON 对象，不要填写整个 MCP 配置。默认 API 地址为 http://127.0.0.1:31009；anytype-cli 或自定义 API 地址可通过本地 MCP 环境配置 ANYTYPE_API_BASE_URL 设置。启动时会读取当前应用的 API 描述。需要支持 stdio credentialEnv 的 Ghast 版本。

Requires Node.js, npx and a running Anytype desktop app with its API enabled. Create an API key in Anytype App Settings > API Keys. Copy the OPENAPI_MCP_HEADERS JSON object from the official generated configuration into the Ghast credential field of the same name, including Authorization and Anytype-Version. Use the JSON object only, not the entire MCP configuration. The default API address is http://127.0.0.1:31009. For anytype-cli or a custom API address, set ANYTYPE_API_BASE_URL in local MCP environment configuration. The server loads the running app’s API schema at startup. Requires Ghast stdio credentialEnv support.

- MCP: `npx -y @anyproto/anytype-mcp@1.2.10`
- [官方文档 / Provider documentation](https://github.com/anyproto/anytype-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://anytype.io/apple-touch-icon.png
