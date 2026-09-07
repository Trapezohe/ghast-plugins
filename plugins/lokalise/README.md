# Lokalise for Ghast

## 简介 / Overview

在 Lokalise 中管理本地化项目、翻译键、任务、术语表与截图。

Manage localization projects, translation keys, tasks, glossaries and screenshots in Lokalise.

## 连接 / Connection

在 Lokalise 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 apikey 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a Lokalise API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the apikey header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://mcp.lokalise.com/mcp/project-management`
- [官方文档 / Provider documentation](https://docs.lokalise.com/en/articles/13547066-setting-up-and-using-the-lokalise-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://intercom.help/lokalise-help/assets/favicon

- MCP: `https://mcp.lokalise.com/mcp/software-development`

本服务为 Lokalise Expert 的 Beta 功能，需要包含 API 访问的套餐；不适用于 Lokalise Vantage。

This beta service requires Lokalise Expert with API access; it is unavailable in Lokalise Vantage.

验证包括公开端点响应、认证发现和本地安装/卸载；未验证真实账号的业务读写。

Validation covers public endpoint responses, auth discovery and local install/removal. Business reads and writes using a real account have not been tested.
