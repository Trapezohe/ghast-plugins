# Descript for Ghast

## 简介 / Overview

通过 Descript 官方 MCP 处理已连接 Drive 中的媒体项目、Underlord 编辑、转录与发布。

Use Descript’s official MCP to work with media projects, Underlord edits, transcripts and publishing in your connected Drive.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Descript OAuth 授权；受账号权限与服务配额限制。 OAuth 连接单个 Descript Drive，无需 API Token。请在服务商流程中选择目标 Drive。导入消耗媒体分钟数，Underlord 编辑可能消耗 AI 积分。当前下载渲染媒体需要先发布，转录格式与 REST API 不完全相同。已验证到服务商 PKCE 授权跳转，未上传、编辑或发布媒体。

Connect in Ghast and complete Descript OAuth in the provider browser page. Account permissions and service quotas apply. OAuth connects one Descript Drive; no API token is needed. Select the intended Drive in the provider flow. Imports consume media minutes and Underlord edits may consume AI credits. Rendered media download currently requires publishing; transcript formats differ from the REST API. Verification reached the provider PKCE redirect before consent; no media was uploaded, edited or published.

- MCP: `https://api.descript.com/v2/mcp`
- [官方文档 / Provider documentation](https://help.descript.com/api-and-mcp/mcp-custom)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/31518792?v=4
