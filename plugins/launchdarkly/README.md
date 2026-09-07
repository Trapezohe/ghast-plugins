# LaunchDarkly for Ghast

## 简介 / Overview

在 LaunchDarkly 中管理功能开关、AgentControl 配置与可观测数据。

Manage feature flags, AgentControl configurations and observability data in LaunchDarkly.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 LaunchDarkly OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete LaunchDarkly OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.launchdarkly.com/mcp/launchdarkly`
- [官方文档 / Provider documentation](https://launchdarkly.com/docs/home/getting-started/mcp-hosted)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://launchdarkly.com/apple-icon.png?8354b0c15ee5b065
