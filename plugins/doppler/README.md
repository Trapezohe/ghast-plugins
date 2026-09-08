# Doppler for Ghast

## 简介 / Overview

通过 Doppler 官方实验版 MCP 处理项目、环境、配置和限定权限范围的密钥。

Use Doppler’s official experimental MCP to work with projects, environments, configs and scoped secrets.

## 连接 / Connection

需要 Node.js 20 或更新版本以及 npx。在 Ghast 凭据输入框填写有效且已限定权限范围的 Doppler Token。官方包固定为 1.0.5，启动 MCP 前会向 Doppler 验证 Token；无效 Token 会中止启动。可用工具受 Token 范围影响。本包提供正常工具集，API 负责执行 Token 权限限制；使用只读 Token 时写入工具仍可能显示。已通过本地回环模拟 API 验证启动和 128 个工具发现，真实 API 拒绝测试凭据。未测试真实账号访问、密钥或写入。服务商将此服务器标为实验版，仅面向开发、测试和评估。

Requires Node.js 20 or later and npx. Enter a valid, narrowly scoped Doppler token in Ghast’s credential field. The official package is pinned to 1.0.5 and validates the token against Doppler before starting MCP; invalid tokens stop startup. Available tools depend on token scope. This package exposes the normal tool surface, while the API enforces token permissions; write tools may remain visible with a read-only token. Local startup and discovery of 128 tools were verified against a loopback fixture API. The real API rejected fixture credentials. Real account access, secrets and writes were not tested. The provider labels this server experimental, for development, testing and evaluation.

- MCP: `npx -y @dopplerhq/mcp-server@1.0.5`
- [官方文档 / Provider documentation](https://github.com/DopplerHQ/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/34022344?v=4
