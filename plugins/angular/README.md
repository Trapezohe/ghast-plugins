# Angular for Ghast

## 简介 / Overview

使用 Angular 官方 CLI MCP 工具分析工作区、查询文档、运行开发服务器及构建流程。

Use Angular’s official CLI MCP tools for workspace analysis, documentation, development servers and build workflows.

## 连接 / Connection

需要 npx，以及 Node.js ^22.22.3、^24.15.0 或 >=26.0.0，无需账号或 Token。工具要求工作区路径时应提供目标 Angular 项目路径。项目操作需要已有 Angular 工作区及其依赖。启用官方默认工具；如需只读或离线模式，可在本地配置相应选项。本插件配置关闭 CLI 使用统计。

Requires npx and Node.js ^22.22.3, ^24.15.0 or >=26.0.0. No account or token is required. Supply the intended Angular workspace path when a tool requests it. Project operations require an existing Angular workspace and its dependencies. Default official tools are enabled; optional read-only/local-only modes can be configured locally. CLI analytics is disabled in this plugin configuration.

- MCP: `npx -y @angular/cli@22.1.7 mcp`
- [官方文档 / Provider documentation](https://angular.dev/ai/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://angular.dev/assets/icons/safari-pinned-tab.svg
