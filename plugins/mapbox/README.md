# Mapbox for Ghast

## 简介 / Overview

通过 Mapbox 官方托管 MCP 查找地址与地点、规划路线并生成地图可视化。

Find addresses and places, plan routes and create map visualizations through Mapbox’s official hosted MCP.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Mapbox OAuth 授权；受账号权限与服务配额限制。 使用 Mapbox 官方托管入口。已验证 OAuth 发现及 S256 跳转，未测试账号授权与地图业务操作；受 Mapbox 账号权限和使用配额限制。

Connect in Ghast and complete Mapbox OAuth in the provider browser page. Account permissions and service quotas apply. Uses Mapbox’s official hosted endpoint. OAuth discovery and S256 redirect were verified; account authorization and mapping operations were not tested. Mapbox account permissions and usage limits apply.

- MCP: `https://mcp.mapbox.com/mcp`
- [官方文档 / Provider documentation](https://docs.mapbox.com/api/guides/mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/600935?v=4
