# Sitecore Marketer for Ghast

## 简介 / Overview

连接 Sitecore 官方 Marketer MCP，处理站点、页面、内容、素材、品牌上下文与活动优化。

Connect Sitecore’s official Marketer MCP to work with sites, pages, content, assets, brand context and campaign optimization.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Sitecore Marketer OAuth 授权；受账号权限与服务配额限制。 需要 SitecoreAI Admin 角色，并有权访问目标组织与租户。通过服务商页面授权时选择目标组织和租户。本包采用更新后的 marketer.sitecorecloud.io 端点，不采用已进入弃用流程的 edge-platform 域名。已验证到 PKCE 授权跳转，未测试 Token 交换、账号工具、内容修改或实验。

Connect in Ghast and complete Sitecore Marketer OAuth in the provider browser page. Account permissions and service quotas apply. Requires an Admin role in SitecoreAI and access to the target organization and tenant. Authorize through the provider page and select the intended organization and tenant. This uses the updated marketer.sitecorecloud.io endpoint rather than the deprecated edge-platform hostname. Verification reached a PKCE redirect before consent; token exchange, account tools, content changes and experiments were not tested.

- MCP: `https://marketer.sitecorecloud.io/mcp/marketer-mcp-prod`
- [官方文档 / Provider documentation](https://doc.sitecore.com/sai/en/users/sitecoreai/sitecore-marketer-mcp-server/index.html)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/1051478?v=4
