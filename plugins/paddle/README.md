# Paddle for Ghast

## 简介 / Overview

通过 Paddle 官方工具处理计费、订阅与收入运营，分别连接生产环境、沙盒和开发文档。

Use official Paddle tools for billing, subscriptions and revenue workflows, with separate live, sandbox and documentation connections.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Paddle OAuth 授权；受账号权限与服务配额限制。 生产连接使用 Paddle OAuth，初始为用户角色允许的读取权限，可在 Paddle 的 Connectors > MCP 中调整权限。沙盒不支持 OAuth，请在 Ghast 凭据框填写沙盒专用 API Key。文档服务由 Paddle 使用 Kapa.ai 托管，需要独立的 Google 或 GitHub 登录，查阅文档无需 Paddle 账号。这是同一插件中的三个连接，生产与沙盒环境不可混用。

Connect in Ghast and complete Paddle OAuth in the provider browser page. Account permissions and service quotas apply. The live server uses Paddle OAuth, initially limited to reads allowed by the user role; manage connection permissions in Paddle Connectors > MCP. The sandbox server uses its own sandbox API key in Ghast’s credential field and does not support OAuth. The documentation server is hosted for Paddle by Kapa.ai and uses a separate Google or GitHub sign-in; no Paddle account is needed for documentation. These are three connections in one plugin, not interchangeable environments.

- MCP: `https://mcp.paddle.com/mcp`
- MCP: `https://sandbox-mcp.paddle.com/mcp`
- MCP: `https://paddlehq.mcp.kapa.ai`
- [官方文档 / Provider documentation](https://developer.paddle.com/sdks/ai/paddle-mcp/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/6573820?v=4
