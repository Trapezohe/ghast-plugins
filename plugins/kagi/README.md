# Kagi for Ghast

## 简介 / Overview

通过 Kagi 官方 MCP 搜索网页、新闻、图片、视频和播客，并提取页面内容。

Search the web, news, images, videos and podcasts with Kagi’s official MCP, and extract page content.

## 连接 / Connection

在 Kagi 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 使用服务商托管端点和 Kagi API Key，不使用浏览器会话或 OAuth 登录。使用受 API 计费和配额限制。已发现 kagi_search_fetch 和 kagi_extract；测试密钥搜索被拒绝，返回 Token 签名错误。未测试付费搜索或已认证的内容提取。

Create a Kagi API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. Uses the provider-hosted endpoint and a Kagi API key, not a browser session or OAuth login. API billing and quotas apply. Discovery returned kagi_search_fetch and kagi_extract; a fixture-key search was rejected with a token-signature error. No paid search or authenticated extraction was tested.

- MCP: `https://mcp.kagi.com/mcp`
- [官方文档 / Provider documentation](https://github.com/kagisearch/kagimcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/92134518?v=4
