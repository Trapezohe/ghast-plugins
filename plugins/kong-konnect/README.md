# Kong Konnect for Ghast

## 简介 / Overview

通过 Kong Konnect 官方 MCP 检查 API 网关、服务、路由与性能。

Inspect API gateways, services, routes and performance with Kong Konnect’s official MCP.

## 连接 / Connection

在 Kong Konnect 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 默认美国区域；其他区域请先按官方区域端点表修改本地 MCP 服务地址。使用 Konnect PAT 或 System Access Token，不是 Kong Gateway Admin API 凭据。

Create a Kong Konnect API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. Defaults to the US region. For another region, update the local MCP server URL using the provider regional endpoint table before connecting. Use a Konnect PAT or System Access Token, not a Kong Gateway Admin API credential.

- MCP: `https://us.mcp.konghq.com/`
- [官方文档 / Provider documentation](https://developer.konghq.com/konnect-platform/konnect-mcp/installation/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://konghq.com/favicon-180.png
