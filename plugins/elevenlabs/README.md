# ElevenLabs for Ghast

## 简介 / Overview

通过 ElevenLabs 生成语音，并管理语音智能体、会话与知识资源。

Generate speech and manage voice agents, conversations and knowledge resources through ElevenLabs.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 ElevenLabs OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete ElevenLabs OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://api.us.elevenlabs.io/v1/mcp`
- [官方文档 / Provider documentation](https://elevenlabs.io/docs/eleven-agents/operate/hosted-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://elevenlabs.io/icon.svg?c23f5371fdd26632

验证范围为官方端点及认证元数据、Ghast 本地安装与卸载；未登录真实账号验证生成任务或账号写入。

Validation covers the official endpoint and auth metadata, plus Ghast local installation and removal. Real account generation and account writes have not been tested.

需要支持公开客户端身份文档（CIMD）的 Ghast 版本。使用官方通用服务的规范端点 api.us.elevenlabs.io；隔离数据驻留环境需要对应地区的官方端点与独立账号。

Requires a Ghast build supporting Client ID Metadata Documents (CIMD). Uses the canonical api.us.elevenlabs.io endpoint for the standard service. Isolated residency environments require their official regional endpoint and separate account.
