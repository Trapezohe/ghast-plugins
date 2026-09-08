# Adobe Express Developer for Ghast

## 简介 / Overview

通过 Adobe 官方原生开发者 MCP 检索 Express 插件文档，并获取 SDK TypeScript 类型定义。

Search Adobe Express add-on documentation and retrieve official SDK TypeScript definitions with Adobe’s native developer MCP.

## 连接 / Connection

需要 Node.js >=18 和 npx。无需用户凭据，使用 Adobe 包内公开的文档客户端标识。服务获取开发文档及 SDK 类型，不访问账号内容。官方 SDK 类型依赖可独立于固定版本的 MCP 包更新。验证发现 2 个工具，已成功获取 iframe-ui 类型定义及图片导入文档。

Requires Node.js >=18 and npx. No user credentials are required: the package uses Adobe’s bundled public documentation-client identifier. The server retrieves developer documentation and SDK types, not account content. Its official SDK types dependency can update independently of the pinned MCP package. Verification discovered 2 tools and successfully fetched iframe-ui definitions and image-import documentation.

- MCP: `npx -y @adobe/express-developer-mcp@1.0.0`
- [官方文档 / Provider documentation](https://developer.adobe.com/express/add-ons/docs/guides/getting-started/local-development/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/476009?v=4
