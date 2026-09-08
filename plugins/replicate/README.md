# Replicate for Ghast

## 简介 / Overview

通过 Replicate 官方 MCP 查找、比较并运行 AI 模型。

Discover, compare and run AI models on Replicate through its official MCP server.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Replicate OAuth 授权；受账号权限与服务配额限制。 使用服务商文档指定的 SSE 端点。浏览器授权页会要求提供你自己的 Replicate API Token，仅在服务商页面填写。运行模型会消耗账号额度。

Connect in Ghast and complete Replicate OAuth in the provider browser page. Account permissions and service quotas apply. Uses the provider’s documented SSE endpoint. The browser authorization page asks for your own Replicate API token; enter it only on the provider page. Model execution consumes your account credits.

- MCP: `https://mcp.replicate.com/sse`
- [官方文档 / Provider documentation](https://replicate.com/docs/reference/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://static.replicateassets.com/fe/b383623d83cbf572f53447104233fdd3297736b8/favicon-CKiqAkf2.png
