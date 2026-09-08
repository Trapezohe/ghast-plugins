# Fullstory for Ghast

## 简介 / Overview

通过 Fullstory 官方 MCP 测试版分析用户行为指标、分群与会话回放，支持全局及欧洲区连接。

Analyze behavioral metrics, segments and session replay through Fullstory’s official MCP beta, with global and EU connections.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Fullstory OAuth 授权；受账号权限与服务配额限制。 MCP 处于测试版，需组织管理员在账号管理设置中同时启用 MCP 与 StoryAI。关闭 StoryAI 可能导致连接成功但没有工具。fullstory 使用官方全局端点，欧洲区组织使用 fullstory-eu，只连接适用区域。两个已发布端点均通过 Ghast OAuth 发现并生成 PKCE 授权跳转。na1 域名当前声明全局资源标识，未通过严格匹配，因此未采用。未验证账号工具、会话访问或 Token 交换。

Connect in Ghast and complete Fullstory OAuth in the provider browser page. Account permissions and service quotas apply. MCP is in beta and must be enabled by an org admin together with StoryAI under Account Management settings. Disabled StoryAI can result in a connection with zero tools. Use fullstory for the official global endpoint, or fullstory-eu for EU-hosted organizations; connect the appropriate region only. Both published endpoints passed Ghast OAuth discovery and generated PKCE redirects. The na1 hostname currently advertises the global resource identifier and failed strict matching, so it is not used. Account tools, session access and token exchange were not tested.

- MCP: `https://api.fullstory.com/mcp/fullstory`
- MCP: `https://api.eu1.fullstory.com/mcp/fullstory`
- [官方文档 / Provider documentation](https://developer.fullstory.com/mcp/introduction/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/33756472?v=4
