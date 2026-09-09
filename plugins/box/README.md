# Box for Ghast

## 简介 / Overview

连接 Box 账号，搜索并读取有权访问的文件和文件夹。

Search and read Box files and folders with a connected Box account.

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

在支持 Box 托管授权的 Ghast 客户端中，点击“连接账号”并在 Box 网页授权。OAuth 应用密钥由 Ghast 后台保管，用户不需要填写 Client ID、Client Secret 或 API key。当前接入范围为读取用户有权访问的文件和文件夹，不请求写入、Box AI、签名或管理权限。

In a Ghast client that supports managed Box OAuth, click Connect account and authorize in Box. Ghast's backend holds the application secret; users do not enter a Client ID, Client Secret, or API key. The current integration requests read access to files and folders available to the user, without write, Box AI, signature, or administrative scopes.

Box 组织策略可能要求管理员先启用未发布的 OAuth 应用及 MCP 工具。正式可用状态由后台控制；未通过连接与真实只读任务验收时不宣称可用。

Box organization policy may require an administrator to enable unpublished OAuth apps and MCP tools. Backend readiness controls availability; application registration alone does not establish a working connection or a successful read-only task.
