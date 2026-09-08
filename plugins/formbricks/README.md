# Formbricks for Ghast

## 简介 / Overview

通过 Formbricks Cloud 官方 MCP 管理问卷、工作流与客户反馈。

Manage surveys, workflows and customer feedback through Formbricks Cloud’s official MCP.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Formbricks OAuth 授权；受账号权限与服务配额限制。 使用当前 Formbricks Cloud OAuth 入口；自托管实例需另行配置服务。访问受授权范围、工作区角色与产品权益限制。OAuth 发现和 S256 跳转已通过，未测试账号授权与业务操作。

Connect in Ghast and complete Formbricks OAuth in the provider browser page. Account permissions and service quotas apply. Uses the current Formbricks Cloud OAuth endpoint, not the separate Hub SDK package. Self-hosted installations require their own server configuration. Access is bounded by consent scopes, workspace roles and product entitlements. OAuth discovery and S256 redirect passed; account authorization and business operations were not tested.

- MCP: `https://app.formbricks.com/api/mcp`
- [官方文档 / Provider documentation](https://formbricks.com/docs/platform/mcp/overview)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/105877416?v=4
