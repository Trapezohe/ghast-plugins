# Directus for Ghast

## 简介 / Overview

通过 Directus 官方 Content MCP 服务查询和管理内容、素材及受支持的自动化流程。

Query and manage Directus content, assets and supported automation workflows using the official Content MCP server.

## 连接 / Connection

需要 Node.js、npx 和可访问的 Directus 项目。在 Ghast 连接凭据中，将实例地址填入 DIRECTUS_URL，将用户资料中已保存的静态 Token 填入 DIRECTUS_TOKEN。用户角色需要允许启动时读取字段和关联结构，以及目标内容操作。启用官方 Content MCP 包的默认工具，默认禁用条目删除。需要支持 stdio credentialEnv 的 Ghast 版本。

Requires Node.js, npx and an accessible Directus project. Enter your instance URL in DIRECTUS_URL and a saved user static token in DIRECTUS_TOKEN in Ghast connection credentials. The user role must permit reading fields and relations at startup and the requested content operations. The official Content MCP package exposes its default tools and disables item deletion by default. Requires Ghast stdio credentialEnv support.

- MCP: `npx -y @directus/content-mcp@0.1.0`
- [官方文档 / Provider documentation](https://github.com/directus/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://framerusercontent.com/images/eQgF4MEhqF4BocT3nAECHqGhk.png
