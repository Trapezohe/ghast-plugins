# LangSmith for Ghast

## 简介 / Overview

通过 LangSmith 官方远程 MCP 查看调用追踪、对话历史、提示词、数据集和实验。

Explore LangSmith traces, conversation history, prompts, datasets and experiments through the official remote MCP server.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 LangSmith OAuth 授权；受账号权限与服务配额限制。 默认连接 LangSmith Cloud 美国 GCP 区域。欧洲或美国 AWS 工作区需在本地 MCP 配置中使用对应区域的 /mcp 地址。OAuth 使用 PKCE 和资源绑定。自托管 LangSmith 需要单独配置官方 Python 服务，不包含社区 TypeScript 移植版。

Connect in Ghast and complete LangSmith OAuth in the provider browser page. Account permissions and service quotas apply. Targets LangSmith Cloud US GCP. EU or US AWS workspaces require the matching regional /mcp URL in local MCP configuration. OAuth uses PKCE and resource binding. Self-hosted LangSmith requires the separate official Python server; the community TypeScript port is not included.

- MCP: `https://api.smith.langchain.com/mcp`
- [官方文档 / Provider documentation](https://docs.langchain.com/langsmith/langsmith-remote-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/69a17e4f0c916c644f4de1cd_webclip%20lg.png
