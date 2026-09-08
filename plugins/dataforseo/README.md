# DataForSEO for Ghast

## 简介 / Overview

通过 DataForSEO 官方 API 与文档工具研究关键词、搜索结果、外链和竞争对手。

Research keywords, search results, backlinks and competitors using DataForSEO’s official API and documentation tools.

## 连接 / Connection

使用 DataForSEO API Access 中的 API 登录名与 API 密码，而非网页账号密码。在 Ghast 凭据框填写完整 Authorization 值：Basic、一个空格，以及 API登录名:API密码 的 Base64 编码。不要将此值发送到聊天中。远程服务使用该 Basic 请求头调用 API，相关使用按服务商标准计费。

Use the API login and API password from DataForSEO API Access, not dashboard sign-in credentials. In the Ghast credential field, enter the full Authorization value: Basic followed by a space and the Base64 encoding of API-login:API-password. Keep this value out of chat. The hosted service uses this Basic header for API calls; API usage charges apply.

- MCP: `https://mcp.dataforseo.com/v3/mcp`
- [官方文档 / Provider documentation](https://dataforseo.com/seo-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://dataforseo.com/wp-content/uploads/2022/04/cropped-favicon_512-1-180x180.png
