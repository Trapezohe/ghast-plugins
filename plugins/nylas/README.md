# Nylas for Ghast

## 简介 / Overview

通过 Nylas 官方 MCP，在应用所属区域操作已连接的邮件、日历、联系人与会议记录助手。

Use Nylas’s official MCP to work with connected email, calendars, contacts and meeting Notetakers in your application region.

## 连接 / Connection

在 Nylas 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 需要已连接的 Nylas 账号授权（grant）。仅连接与应用数据驻留区域匹配的美国或欧洲服务，另一项保持未连接。这是 Nylas 自身服务，并非 Google 或 Microsoft 的直连连接器。两个区域入口均拒绝了无效测试 API Key；未测试认证后的工具发现与业务操作。

Create a Nylas API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. A connected Nylas account grant is required. Connect only the US or EU server matching your application data-residency region; leave the other disconnected. This is Nylas’s own service, not a direct Google or Microsoft connector. Both regional endpoints rejected an invalid fixture API key; authenticated tool discovery and business operations were not tested.

- MCP (US): `https://mcp.us.nylas.com`
- MCP (EU): `https://mcp.eu.nylas.com`
- [官方文档 / Provider documentation](https://developer.nylas.com/docs/dev-guide/mcp/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/4219865?v=4
