# Brave Search for Ghast

## 简介 / Overview

通过 Brave 官方 Search API MCP 检索网页、新闻、图片、视频与地点信息。

Search the web, news, images, videos and places with Brave’s official Search API MCP server.

## 连接 / Connection

需要 Node.js 与 Brave Search API Key。在 Ghast 连接凭据框填写 Key，由 BRAVE_API_KEY 注入。服务在插件数据目录运行，不读取项目中的 .env；禁用外部 Key 文件发现，使用 Ghast 配置的凭据。

Requires Node.js and a Brave Search API key. Enter the API key in Ghast’s connection credential field; it is passed through BRAVE_API_KEY. Runs in the plugin data directory so it does not discover project .env files. API key file discovery is disabled to keep the configured Ghast credential authoritative.

- MCP: `npx -y @brave/brave-search-mcp-server@2.1.3 --transport stdio`
- [官方文档 / Provider documentation](https://github.com/brave/brave-search-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://brave.com/static-assets/images/cropped-brave_appicon_release-180x180.png
