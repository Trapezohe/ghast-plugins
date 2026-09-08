# Feishu / Lark for Ghast

## 简介 / Overview

通过飞书／Lark 官方 OpenAPI MCP 处理文档、多维表格、群聊、日历与任务。

Work with documents, Base tables, chats, calendars and tasks through the official Feishu / Lark OpenAPI MCP.

## 连接 / Connection

需要 Node.js >=20、npx 及你自己的飞书／Lark 应用。在 Ghast 连接凭据中填写 APP_ID、APP_SECRET，并在开放平台申请相关权限及资源访问。USER_ACCESS_TOKEN 为可选项，仅用户身份访问时需要，应通过自己应用的官方授权流程取得。服务使用 auto 身份模式，启用默认、日历及任务预设。默认域名为 open.feishu.cn；国际版 Lark 用户需要在本地 MCP 环境配置中设置 LARK_DOMAIN=https://open.larksuite.com。需要支持 stdio credentialEnv 与 optionalCredentials 的 Ghast 版本。从 ghast.1 更新后，由于受保护的进程配置已变化，需要重新填写应用凭据。

Requires Node.js >=20, npx and your own Feishu/Lark application. Enter APP_ID and APP_SECRET in Ghast connection credentials. Grant the required application scopes and resource access in the developer console. USER_ACCESS_TOKEN is optional and only needed for user-identity access; obtain it through your own app’s official authorization flow. The server uses auto token mode and the default, calendar and task presets. Default API domain is open.feishu.cn; international Lark users must set LARK_DOMAIN=https://open.larksuite.com in local MCP environment configuration. Requires Ghast stdio credentialEnv and optionalCredentials support. After updating from ghast.1, re-enter the app credentials because the protected process configuration has changed.

- MCP: `npx -y @larksuiteoapi/lark-mcp@0.5.1 mcp -t preset.default,preset.calendar.default,preset.task.default`
- [官方文档 / Provider documentation](https://github.com/larksuite/lark-openapi-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/54944174?v=4
