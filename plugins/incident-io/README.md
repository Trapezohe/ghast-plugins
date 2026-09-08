# incident.io for Ghast

## 简介 / Overview

通过 incident.io 官方远程 MCP 处理事故、告警、值班安排与升级响应信息。

Work with incidents, alerts, on-call schedules and escalation context using incident.io’s official remote MCP.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 incident.io OAuth 授权；受账号权限与服务配额限制。 组织管理员需要启用 Settings > MCP，可用性取决于套餐与权限。验证到服务商 OAuth 授权页面跳转，未完成授权或验证账号工具及事故操作。

Connect in Ghast and complete incident.io OAuth in the provider browser page. Account permissions and service quotas apply. An organization administrator must enable Settings > MCP. Availability depends on your plan and permissions. Verification reached the provider OAuth redirect before consent; no account tools or incident operations were tested.

- MCP: `https://mcp.incident.io/mcp`
- [官方文档 / Provider documentation](https://docs.incident.io/ai/remote-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/76436871?v=4
