# GrowthBook for Ghast

## 简介 / Overview

通过 GrowthBook 官方 MCP 及配套流程指引管理功能开关并查看实验。

Manage feature flags and inspect experiments through GrowthBook’s official MCP and bundled workflow guidance.

## 连接 / Connection

需要安装 Node.js 和 npm，并在 Ghast 填写 GrowthBook API Key 或个人访问令牌。本配置连接 api.growthbook.io 的 GrowthBook Cloud；自托管实例需另行配置服务。凭据通过环境变量注入，不要在聊天中发送。 本地启动发现 4 个工具；无效测试凭据读取返回认证错误。未测试真实账号操作。

Install Node.js and npm, then enter a GrowthBook API key or personal access token in Ghast. This configuration connects to GrowthBook Cloud at api.growthbook.io; self-hosted instances need their own server configuration. Credentials are supplied through environment variables, never chat. Local startup exposed 4 tools; a read with invalid fixture credentials returned an authentication error. Real account operations were not tested.

- MCP: `npx -y @growthbook/mcp@2.1.0`
- [官方文档 / Provider documentation](https://github.com/growthbook/growthbook-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/65404594?v=4
