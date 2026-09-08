# Unleash for Ghast

## 简介 / Overview

通过 Unleash 官方 MCP 服务查看功能开关、评估变更并管理实例中的灰度发布。

Inspect feature flags, evaluate changes and manage rollouts on your Unleash instance with its official MCP server.

## 连接 / Connection

需要 Node.js >=20 和 npx。在 Ghast 凭据字段填写自己的 Unleash 实例基础 URL（不含 /api）和个人访问 Token。默认项目与环境可选，未填写时在工具调用中明确范围。需要 Ghast 支持 credentialEnv 和 optionalCredentials。 验证发现 11 个工具，通过本地模拟实例确认 Authorization 请求头与 401 错误传递，未访问真实 Unleash 实例。

Requires Node.js >=20 and npx. Enter your own Unleash instance base URL (without /api) and a personal access token in Ghast credentials. Project and environment defaults are optional; if omitted, specify scope in tool calls. Requires Ghast credentialEnv and optionalCredentials support. Verification discovered 11 tools and confirmed the Authorization header and 401 propagation using a local simulated instance. No real Unleash instance was accessed.

- MCP: `npx -y @unleash/mcp@0.4.1 --log-level error`
- [官方文档 / Provider documentation](https://docs.getunleash.io/integrate/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/23053233?v=4
