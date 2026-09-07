# Zapier for Ghast

## 简介 / Overview

从 Ghast 运行你在 Zapier MCP 服务中配置的动作。

Run the actions configured in your Zapier MCP server from Ghast.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Zapier OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Zapier OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.zapier.com/api/v1/connect`
- [官方文档 / Provider documentation](https://docs.zapier.com/mcp/home)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://zapier.com/favicon.ico

这是 Zapier 平台自身的官方连接器，下游应用由 Zapier 集成，不等同于这些应用厂商的原生连接器，也不计作独立 Ghast 插件。

This is Zapier’s official platform connector. Downstream app integrations are supplied by Zapier, not represented as those providers’ native connectors or counted as separate Ghast plugins.

验证涵盖官方端点、认证元数据与本地安装/卸载；未使用真实账号验证业务读写。

Validation covers the official endpoint, auth metadata and local install/removal. Business reads and writes with real accounts have not been tested.
