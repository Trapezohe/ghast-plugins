# Stellar Raven for Ghast

## 简介 / Overview

通过 Stellar Development Foundation 官方 Raven MCP 检索 Stellar 文档、生态数据与开发指南。

Search Stellar documentation, ecosystem data and development playbooks through the Stellar Development Foundation’s official Raven MCP.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Stellar Raven OAuth 授权；受账号权限与服务配额限制。 通过浏览器完成登录与授权，无需提供底层服务 API Key。Raven 由 Stellar Development Foundation 运营，整合官方文档及生态来源。验证已生成服务商 PKCE OAuth 授权跳转，未完成用户授权，也未验证账号工具、目录操作执行或 Token 刷新。

Connect in Ghast and complete Stellar Raven OAuth in the provider browser page. Account permissions and service quotas apply. Use the browser sign-in and consent flow; no underlying service API keys are needed. Raven is operated by the Stellar Development Foundation and combines official documentation with ecosystem sources. Verification generated the provider PKCE OAuth redirect before consent. Account tools, catalog execution and token refresh were not tested.

- MCP: `https://raven.stellar.org/mcp`
- [官方文档 / Provider documentation](https://raven.stellar.org/docs)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/7386716?v=4
