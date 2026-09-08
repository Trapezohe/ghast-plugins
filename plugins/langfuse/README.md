# Langfuse for Ghast

## 简介 / Overview

通过 Langfuse 官方项目 MCP 查询观测记录和指标，管理提示词、数据集及评测。

Query Langfuse observations and metrics and manage prompts, datasets and evaluations through the official project MCP server.

## 连接 / Connection

在 Langfuse 项目中创建 API 密钥，在本地将 public-key:secret-key 整体进行 Base64 编码，再将包含 Basic 前缀的完整 Basic <编码值> 填入 Ghast 的 Authorization 连接凭据字段。不要在聊天中发送密钥或编码值。本配置使用欧洲云区域；其他区域及自托管实例须在本地 MCP 配置中使用对应的 /api/public/mcp 地址。受项目权限和配额限制。

Create project API keys in Langfuse. Base64-encode the exact public-key:secret-key pair locally, then enter the complete value Basic <base64-value> in the Ghast Authorization credential field, including the Basic prefix. Do not send either key or the encoded value in chat. This configuration uses Cloud EU; other regions or self-hosted instances require the matching /api/public/mcp URL in local MCP configuration. Project permissions and quotas apply.

- MCP: `https://cloud.langfuse.com/api/public/mcp`
- [官方文档 / Provider documentation](https://langfuse.com/docs/api-and-data-platform/features/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://langfuse.com/apple-touch-icon.png
