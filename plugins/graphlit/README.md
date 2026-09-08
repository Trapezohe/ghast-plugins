# Graphlit for Ghast

## 简介 / Overview

通过 Graphlit 官方 MCP 检索项目知识、搜索内容、整理集合并构建内容工作流。

Use Graphlit’s official MCP to retrieve project knowledge, search content, organize collections and build content workflows.

## 连接 / Connection

需要 Node.js 18 或更新版本以及 npx。在 Ghast 凭据输入框填写 Graphlit 项目 API 面板中的组织 ID、环境 ID 和 JWT 签名密钥。官方包固定为 1.0.20260112001。本包连接 Graphlit 本身，未配置其他服务的可选凭据。处理、导入和模型调用可能产生 Graphlit 费用。启动和 71 个工具发现成功，测试凭据查询项目用量返回 401。未测试真实项目数据、内容导入或付费处理。

Requires Node.js 18 or later and npx. Enter the organization ID, environment ID and JWT signing secret from your Graphlit project API dashboard in Ghast’s credential fields. The official package is pinned to 1.0.20260112001. This connects to Graphlit itself; other services’ optional credentials are not configured by this package. Processing, ingestion and model calls may incur Graphlit charges. Startup and discovery of 71 tools succeeded; fixture credentials querying project usage returned 401. No real project data, ingestion or paid processing was tested.

- MCP: `npx -y graphlit-mcp-server@1.0.20260112001`
- [官方文档 / Provider documentation](https://github.com/graphlit/graphlit-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/130105661?v=4
