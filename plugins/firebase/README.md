# Firebase for Ghast

## 简介 / Overview

通过 Google 官方 MCP 开发与管理 Firebase 项目、检查应用配置并部署服务。

Develop and manage Firebase projects, inspect app configuration and deploy services through Google’s official MCP.

## 连接 / Connection

需要 Node.js >=20 及 npx，使用官方 firebase-tools@15.29.0 包。通过 Firebase CLI（firebase login）或官方 MCP 登录工具登录，使用 Firebase CLI 账号。开始任务前检查并更新 MCP 环境，选择正确的项目目录与当前项目。可用工具受登录状态、项目配置、云权限、计费与配额限制。

Requires Node.js >=20 and npx. Uses the official firebase-tools@15.29.0 package. Sign in through Firebase CLI (firebase login) or the official MCP login tool. This uses your Firebase CLI account, not a Ghast OAuth app. Inspect and update the MCP environment to select the intended project directory and active project before work. Available tools depend on authentication and project configuration; cloud permissions, billing and quotas apply.

- MCP: `npx -y firebase-tools@15.29.0 mcp`
- [官方文档 / Provider documentation](https://firebase.google.com/docs/ai-assistance/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.gstatic.com/devrel-devsite/prod/v5e941f15ff6710591bee254538202655020220785b40a3f4d932e94adb9f6037/firebase/images/touchicon-180.png
