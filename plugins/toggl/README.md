# Toggl 2.0 for Ghast

## 简介 / Overview

在 Toggl 2.0 中管理任务、项目、工时记录与报表。

Manage tasks, projects, time entries and reports in Toggl 2.0.

## 连接 / Connection

需要 Node.js 20 或更高版本及 npx。Ghast 启动官方 @togglhq/mcp@1.6.13 包，发现并调用其 auth 工具以打开 Toggl 网页登录。服务商将会话保存到 ~/.toggl/focus-tools.json；调用其 logout 工具可移除当前 MCP 会话。本连接器面向 Toggl 2.0，权限受套餐与工作区角色限制。

Requires Node.js 20 or later and npx. Ghast launches the official @togglhq/mcp@1.6.13 package. Discover and call its auth tool to open Toggl browser login. The provider stores the session in ~/.toggl/focus-tools.json; use its logout tool to remove the active MCP session. This connector targets Toggl 2.0, with access controlled by your plan and workspace role.

- MCP: `npx -y @togglhq/mcp@1.6.13`
- [官方文档 / Provider documentation](https://docs.toggl.com/toggl-mcp-and-cl)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://public-assets.toggl.com/b/static/favicon-ef45c4a393ad528b7ba7b0bae3ce332a.svg
