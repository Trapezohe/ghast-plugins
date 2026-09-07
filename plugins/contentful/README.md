# Contentful for Ghast

## 简介 / Overview

管理 Contentful 多语言内容、媒体素材与内容模型。

Manage multilingual content, assets and content models in Contentful.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Contentful OAuth 授权；受账号权限与服务配额限制。 默认使用全球端点。须在每个空间与环境安装并配置 Contentful MCP 应用，授权时选择对应环境；EU 区组织应改用官方 EU 端点。

Connect in Ghast and complete Contentful OAuth in the provider browser page. Account permissions and service quotas apply. Uses the global endpoint. Install and configure the Contentful MCP app in each space/environment and select those environments during OAuth. EU organizations must use the documented EU endpoint instead.

- MCP: `https://mcp.contentful.com/mcp`
- [官方文档 / Provider documentation](https://www.contentful.com/developers/docs/tools/mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.simpleicons.org/contentful
