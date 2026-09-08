# Wingify for Ghast

## 简介 / Overview

通过 Wingify 官方全局 MCP 连接分析实验、活动报表、热力图与会话录屏。

Analyze Wingify experiments, campaign reports, heatmaps and session recordings through its official global MCP connection.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Wingify OAuth 授权；受账号权限与服务配额限制。 本包当前仅支持官方全局端点。读取数据选择 Browse，创建实验选择 Design，仅在需要时选择 Publish/Admin。官方文档中的欧洲和亚洲端点当前声明全局 OAuth 资源标识，未通过 Ghast 严格资源校验，因此未收录。区域账号使用全局连接前需向服务商确认。已验证全局端点 PKCE 授权跳转，未测试账号报表或活动修改。

Connect in Ghast and complete Wingify OAuth in the provider browser page. Account permissions and service quotas apply. This package currently supports the official global endpoint only. Choose Browse for reading, Design for creating experiments, or Publish/Admin only when required. The documented EU and Asia endpoints currently advertise the global OAuth resource identifier and fail Ghast’s strict resource validation; they are not included. Do not use this global connection for a regional account without provider confirmation. Verification reached the global PKCE redirect before consent; account reports and campaign changes were not tested.

- MCP: `https://mcp.wingify.ai/mcp`
- [官方文档 / Provider documentation](https://help.wingify.com/hc/en-us/articles/58792565345305-Connect-Wingify-with-AI-Tools-using-Wingify-s-MCP-Server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/762041?v=4
