# Adobe Target for Ghast

## 简介 / Overview

连接 Adobe Target 官方公开测试版 MCP，处理实验、个性化、受众、优惠内容与活动流程。

Connect Adobe Target’s official public-beta MCP for experiments, personalization, audiences, offers and activity workflows.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Adobe Target OAuth 授权；受账号权限与服务配额限制。 服务商将此服务列为 Public Beta。需要有效 Adobe Target 许可及相应 Adobe 组织，网页登录时请选择正确组织。Observer 支持读取，Editor 增加创建，Approver 增加启用与停用能力，并受工作区权限约束。无需静态 API 凭据。已验证到 Adobe 的 S256 PKCE 授权页面；未测试用户同意授权、Token 交换、已认证工具或活动操作。

Connect in Ghast and complete Adobe Target OAuth in the provider browser page. Account permissions and service quotas apply. The provider lists this service as Public Beta. An active Adobe Target license and the appropriate Adobe organization are required. Select the correct organization during browser sign-in. Observer supports reading, Editor adds creation, and Approver adds activation/deactivation, subject to workspace permissions. No static API credentials are required. Verification reached Adobe’s S256 PKCE authorization page before consent; token exchange, authenticated tools and activity operations were not tested.

- MCP: `https://targetmcp.adobe.io/mcp`
- [官方文档 / Provider documentation](https://experienceleague.adobe.com/en/docs/target/using/integrate/mcp/target-mcp-get-started)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/36018178?v=4
