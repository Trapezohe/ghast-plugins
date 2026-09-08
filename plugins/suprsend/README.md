# SuprSend for Ghast

## 简介 / Overview

通过 SuprSend 官方 MCP 管理用户、租户和通知偏好，查询工作流列表与文档。

Manage SuprSend users, tenants and notification preferences, list workflows and search documentation through the official MCP server.

## 连接 / Connection

需要 Node.js >=18 和 npx。在 SuprSend Account Settings > Service Tokens 创建工作区服务 Token，并填入 SUPRSEND_SERVICE_TOKEN 连接凭据字段。默认 MCP 工具覆盖用户、对象、租户、偏好、工作流列表和文档。事件及工作流触发工具默认未启用，明确需要时才在本地配置官方 --events 或 --workflows 选项。其他 CLI 功能不会自动成为 MCP 工具。需要支持 stdio credentialEnv 的 Ghast 版本。

Requires Node.js >=18 and npx. Create a workspace service token under SuprSend Account Settings > Service Tokens and enter it in the SUPRSEND_SERVICE_TOKEN credential field. Default MCP tools cover users, objects, tenants, preferences, workflow listing and documentation. Event and workflow trigger tools are not enabled by default; configure the official --events or --workflows options locally only when explicitly needed. Other CLI features are not automatically exposed as MCP tools. Requires Ghast stdio credentialEnv support.

- MCP: `npx -y suprsend@1.0.1 start-mcp-server`
- [官方文档 / Provider documentation](https://docs.suprsend.com/reference/mcp-quickstart-cursor)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/62a87a4ff7326e1bc863e8f3/6a30f0a0bf5f14c49ace669a_SS_logo.png
