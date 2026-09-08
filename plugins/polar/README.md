# Polar for Ghast

## 简介 / Overview

连接 Polar 官方生产与沙箱 MCP 服务，处理支付、产品和订阅工作流。

Connect Polar’s official production and sandbox MCP services for payment, product and subscription workflows.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Polar OAuth 授权；受账号权限与服务配额限制。 生产与沙箱分别连接。两个官方入口均已验证到 S256 PKCE 网页授权跳转；未测试账号授权、Token 交换或支付操作。

Connect in Ghast and complete Polar OAuth in the provider browser page. Account permissions and service quotas apply. Production and sandbox connect separately. Both official endpoints reached S256 PKCE browser redirects. Account authorization, token exchange and payment operations were not tested.

- Sandbox MCP: `https://mcp.polar.sh/mcp/polar-sandbox`
- MCP: `https://mcp.polar.sh/mcp/polar-mcp`
- [官方文档 / Provider documentation](https://polar.sh/docs/integrate/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/105373340?v=4
