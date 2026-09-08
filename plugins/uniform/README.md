# Uniform for Ghast

## 简介 / Overview

通过 Uniform 官方本地 MCP 包查看和管理项目组件、内容类型、模式、条目与页面组合。

Use Uniform’s official local MCP package to inspect and manage project components, content types, patterns, entries and compositions.

## 连接 / Connection

需要 Node.js 与 npx。在 Ghast 凭据输入框填写 Uniform 项目 ID 和已授权该项目的个人访问 Token 或服务账号 Key。本配置采用全局 Uniform API 地址，未配置区域地址。纯读取不消耗 AI 积分，使用大模型的操作会消耗积分。本次固定版本官方本地包发现 23 个工具，少于当前托管服务。启动和工具发现成功，测试密钥查询项目与语言列表返回 401，未测试真实项目内容或付费操作。

Requires Node.js and npx. Enter your Uniform project ID and a personal access token or service account key authorized for that project in Ghast’s credential fields. This configuration uses the global Uniform API hosts; it is not configured for regional hosts. Pure reads do not consume AI credits, but LLM-backed operations do. The pinned official local package exposes 23 tools in this verification, fewer than the current hosted service. Startup and tool discovery succeeded; fixture-key project and locale reads returned 401. No real project content or paid operation was tested.

- MCP: `npx -y @uniformdev/uniform-mcp@20.63.0`
- [官方文档 / Provider documentation](https://docs.uniform.app/docs/guides/cli/commands/ai)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/60941761?v=4
