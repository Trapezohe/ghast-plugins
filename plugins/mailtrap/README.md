# Mailtrap for Ghast

## 简介 / Overview

通过 Mailtrap 官方 MCP 测试沙箱邮件、管理模板与检查邮件投递流程。

Test email in sandboxes, manage templates and inspect delivery workflows using Mailtrap’s official MCP.

## 连接 / Connection

需要 Node.js 与 npx。在 Ghast 连接凭据中填写 Mailtrap API Token 和账号 ID。发信地址、沙箱 ID 通过工具参数传入；账号 Token 不提供组织管理权限。 需要支持 stdio credentialEnv 的 Ghast 版本。服务商可能读取本地 .env 文件，请避免冲突配置。

Requires Node.js and npx. Enter your Mailtrap API token and account ID in Ghast connection credentials. Pass sender and sandbox IDs in tool arguments. Account tokens do not grant organization administration. Requires a Ghast build with stdio credentialEnv support. The provider may load a local .env file; avoid conflicting configuration.

- MCP: `npx -y mcp-mailtrap@0.9.0`
- [官方文档 / Provider documentation](https://github.com/mailtrap/mailtrap-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://mailtrap.io/app/themes/mailtrap/images/favicon/apple-touch-icon.png
