# Postmark for Ghast

## 简介 / Overview

通过 Postmark 官方 MCP 管理事务邮件、模板、投递诊断与 Webhook。

Manage transactional email, templates, delivery diagnostics and webhooks through Postmark’s official MCP.

## 连接 / Connection

需要 Node.js 20 或更高版本及 npx。在 Ghast 连接凭据中填写 Postmark Server Token（不是 Account Token）、已验证发信地址与消息流 ID（通常为 outbound）。官方服务启动时会验证 Token，请保持验证开启。 需要支持 stdio credentialEnv 的 Ghast 版本。服务商可能读取本地 .env 文件，请避免冲突配置。

Requires Node.js 20 or later and npx. Enter a Postmark Server Token (not an Account Token), a verified sender email and your message stream ID (commonly outbound) in Ghast connection credentials. The official server validates the token at startup. Keep startup verification enabled. Requires a Ghast build with stdio credentialEnv support. The provider may load a local .env file; avoid conflicting configuration.

- MCP: `npx -y @activecampaign/postmark-mcp@2.1.1`
- [官方文档 / Provider documentation](https://postmarkapp.com/lp/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://postmarkapp.com/images/apple-touch-icon.png
