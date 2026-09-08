# Google Ads for Ghast

## 简介 / Overview

通过 Google 官方只读 MCP 查询 Ads 账号、广告系列表现与 GAQL 元数据。

Query Google Ads accounts, campaign performance and GAQL metadata through Google’s official read-only MCP.

## 连接 / Connection

需要安装 uv（uvx）和 Python 3.10 或更高版本，在 Cloud 项目中启用相应 Google API。为具有目标账号访问权的身份配置 Google 应用默认凭据，再将凭据 JSON 文件的绝对路径及项目 ID 填入 Ghast。文件保留在本机，输入框需要路径而非 JSON 内容；不要在聊天中发送凭据，并使用系统文件权限保护它。本插件使用明确指定的文件，不提供一键浏览器 OAuth，也不负责凭据续期。 另需填写 Google Ads Developer Token，访问能力受其级别和登录身份权限限制。 本地启动发现 3 个工具；使用无效测试凭据文件读取时返回认证错误。未读取或修改真实账号数据。

Install uv (uvx) and Python 3.10 or later. Enable the relevant Google APIs in your Cloud project. Configure Google Application Default Credentials for an identity with access to the requested account, then enter the absolute credentials JSON file path and project ID in Ghast. The file stays on your computer; this field takes a path, not JSON contents. Do not send credentials in chat. Protect the file using OS permissions. This plugin uses that explicit file and does not provide one-click browser OAuth or manage its renewal. Also enter your Google Ads developer token. Its access level and the authenticated identity govern account access. Local startup exposed 3 tools. A read using an invalid fixture credentials file returned an authentication error. No real account data was read or changed.

- MCP: `uvx --from git+https://github.com/googleads/google-ads-mcp.git@88f0467b9e536c562941fa52a94dd02b193c8fa4 google-ads-mcp`
- [官方文档 / Provider documentation](https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.gstatic.com/images/branding/productlogos/ads/v5/192px.svg
