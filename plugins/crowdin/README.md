# Crowdin for Ghast

## 简介 / Overview

在 Crowdin 中管理翻译项目、源文件、任务、术语表与翻译记忆库。

Manage translation projects, source files, tasks, glossaries and translation memory in Crowdin.

## 连接 / Connection

在 Crowdin 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a Crowdin API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://mcp.crowdin.com/mcp/`
- [官方文档 / Provider documentation](https://store.crowdin.com/crowdin-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://crowdin.com/astro-website/favicon.svg

默认端点面向 Crowdin.com；Enterprise 需要组织专用端点。

The default endpoint targets Crowdin.com; Enterprise requires its organization-specific endpoint.

验证包括公开端点响应、认证发现和本地安装/卸载；未验证真实账号的业务读写。

Validation covers public endpoint responses, auth discovery and local install/removal. Business reads and writes using a real account have not been tested.
