# Dropbox for Ghast

## 简介 / Overview

搜索与整理 Dropbox 文件，管理分享链接、文件版本和文件收集请求。

Search, organize and work with Dropbox files, sharing links, revisions and file requests.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Dropbox OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Dropbox OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.dropbox.com/mcp`
- [官方文档 / Provider documentation](https://help.dropbox.com/integrations/connect-dropbox-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cfl.dropboxstatic.com/static/metaserver/static/images/favicon.ico

## Ghast 接入设置 / Ghast setup

Ghast 不在 Dropbox 公开的受信任 DCR 客户端名单中。请在 Dropbox App Console 创建 Scoped access / Full Dropbox 应用，启用所需权限，登记 Ghast 回调 URL，然后在 Ghast 填写 App key（Client ID）、App secret 和所需 scopes。不要套用 Codex 的客户端身份。此 MCP 服务为 Beta。

Ghast is not on Dropbox’s published trusted DCR client list. Create a Scoped access / Full Dropbox app in App Console, enable the required permissions and register Ghast’s callback URL. Configure App key as Client ID, App secret and required scopes in Ghast. Do not reuse Codex client identity. The MCP service is beta.

验证涵盖官方端点认证响应、认证元数据和本地安装/卸载；未完成真实账号授权或业务调用。

Validation covers official endpoint auth responses, auth metadata and local install/removal. Real-account authorization and business calls have not been completed.
