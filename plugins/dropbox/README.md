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

在插件详情点击连接，通过 Dropbox 网页授权。Ghast 后台保管应用凭据，用户无需创建应用或填写 App key、App secret、API key。授权范围包含账号信息读取、文件读取与写入、分享读取与写入、文件请求读取与写入。团队管理与永久删除权限未申请。

Click Connect in plugin details and authorize through Dropbox. Ghast manages application credentials on the backend; users do not create apps or enter keys or secrets. Requested permissions cover account information, file read/write, sharing read/write and file request read/write. Team administration and permanent deletion permissions are not requested.

当前应用仍为 Development，已启用最多 500 名开发用户用于审核准备。正式域名 OAuth、Ghast 连接、重连和根目录只读对话已通过；Production 审核尚未批准，公开客户端仍受发布状态限制。断开后，可在 Dropbox 已连接应用设置中撤销授权。

The app remains in Development with up to 500 development users enabled for review preparation. Production-domain OAuth, Ghast connection, reconnect and a real read-only root-directory conversation passed. Production approval is pending; public client availability remains gated. Revoke authorization in Dropbox connected apps settings after disconnecting.
