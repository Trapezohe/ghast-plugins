# Box for Ghast

## 简介 / Overview

搜索与管理 Box 文件和文件夹，并使用可用的 Box AI 文档工具。

Search and manage Box files and folders and use available Box AI document tools.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Box OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Box OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.box.com`
- [官方文档 / Provider documentation](https://developer.box.com/guides/box-mcp/setup)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.box.com/apple-touch-icon.png?tktzid

## Ghast 接入设置 / Ghast setup

在 Box 管理后台的 Integrations 中，为未列出的 MCP 客户端新增 Integration Credentials，开启 Content Actions，并将 Ghast 显示的回调 URL 登记到 Redirect URI。然后在 Ghast 插件连接页填写 Client ID 和 Client Secret，再完成授权。

In Box Admin Console > Integrations, create Integration Credentials for an unlisted MCP client, enable Content Actions and register the callback URL shown by Ghast. Enter Client ID and Client Secret in Ghast, then authorize.

验证涵盖官方端点认证响应、认证元数据和本地安装/卸载；未完成真实账号授权或业务调用。

Validation covers official endpoint auth responses, auth metadata and local install/removal. Real-account authorization and business calls have not been completed.
