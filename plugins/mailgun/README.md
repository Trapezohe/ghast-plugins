# Mailgun for Ghast

## 简介 / Overview

通过 Mailgun 官方 MCP 管理发信域名、邮件模板、投递指标与退订抑制流程。

Manage sending domains, email templates, delivery metrics and suppression workflows with Mailgun’s official MCP.

## 连接 / Connection

需要 Node.js 20.20.2 或更高版本及 npx。在 Ghast 连接凭据中填写按需授权的 Mailgun API Key。官方服务默认美国区域；欧盟账号应先在本地 MCP 环境配置中设置 MAILGUN_API_REGION=eu。 需要支持 stdio credentialEnv 的 Ghast 版本。服务商可能读取本地 .env 文件，请避免冲突配置。

Requires Node.js 20.20.2 or later and npx. Enter a scoped Mailgun API key in Ghast connection credentials. The official server defaults to US. EU accounts must set MAILGUN_API_REGION=eu in their local MCP environment configuration before connecting. Requires a Ghast build with stdio credentialEnv support. The provider may load a local .env file; avoid conflicting configuration.

- MCP: `npx -y @mailgun/mcp-server@2.1.2`
- [官方文档 / Provider documentation](https://documentation.mailgun.com/docs/mailgun/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/447686?v=4
