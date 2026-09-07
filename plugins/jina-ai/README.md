# Jina AI for Ghast

## 简介 / Overview

读取网页、检索研究资料并按相关性整理信息。

Read web pages, search research and rerank relevant information.

## 连接 / Connection

在 Jina AI 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 API Key 用于计量搜索等受保护工具；部分公开读取工具也支持匿名访问。

Create a Jina AI API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. An API key enables metered search and other protected tools; some public reader tools also work anonymously.

- MCP: `https://mcp.jina.ai/v1`
- [官方文档 / Provider documentation](https://github.com/jina-ai/MCP)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://jina.ai/icons/favicon-128x128.png
