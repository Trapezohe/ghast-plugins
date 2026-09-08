# Duda for Ghast

## 简介 / Overview

连接 Duda 官方 MCP，通过已授权工具管理网站、站点内容和账号业务。

Connect Duda’s official MCP to manage websites, site content and account operations with your authorized tools.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Duda OAuth 授权；受账号权限与服务配额限制。 此测试版连接器采用 Duda 主环境端点。在账号设置中检查 MCP 访问权限和套餐支持。其他 Duda 环境可能使用不同端点，本包未配置这些环境。已验证到服务商 OAuth PKCE 授权跳转，未测试账号同意授权、Token 交换或站点业务操作。

Connect in Ghast and complete Duda OAuth in the provider browser page. Account permissions and service quotas apply. This beta connector uses Duda’s primary environment endpoint. Check Account Settings for MCP access and plan availability. Other Duda environments may require a different endpoint and are not configured in this package. Verification reached the provider OAuth PKCE redirect before consent; account authorization, token exchange and site operations were not tested.

- MCP: `https://mcp.duda.co/mcp`
- [官方文档 / Provider documentation](https://developer.duda.co/docs/duda-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/11398238?v=4
