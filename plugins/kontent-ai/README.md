# Kontent.ai for Ghast

## 简介 / Overview

通过 Kontent.ai 官方 MCP 管理结构化内容、内容模型、素材、多语言版本和发布工作流。

Use Kontent.ai’s official MCP to manage structured content, models, assets, language variants and publishing workflows.

## 连接 / Connection

需要 Node.js 20 或更新版本以及 npx。在 Ghast 凭据输入框填写 Management API Key 和环境 ID。仅授予任务所需权限；内容模型修改需要 Manage content model 权限。官方包固定为 0.39.0 版本。已用测试凭据验证工具发现，未测试真实账号内容或发布操作。

Requires Node.js 20 or later and npx. Enter your Management API key and environment ID in Ghast’s credential fields. Grant only the permissions needed for the requested work; content model changes require the Manage content model permission. The official package is pinned to version 0.39.0. Tool discovery was tested with fixture credentials; no real account content or publishing operation was tested.

- MCP: `npx -y @kontent-ai/mcp-server@0.39.0 stdio`
- [官方文档 / Provider documentation](https://kontent.ai/learn/docs/ai/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/104572275?v=4
