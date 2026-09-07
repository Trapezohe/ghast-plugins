# Chainstack for Ghast

## 简介 / Overview

查询区块链基础设施与文档，管理 Chainstack 节点。

Inspect blockchain infrastructure, search documentation and manage Chainstack nodes.

## 连接 / Connection

在 Chainstack 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 公开文档与平台状态工具无需 Token。

Create a Chainstack API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. Public documentation and platform-status tools also work without a token.

- MCP: `https://mcp.chainstack.com/mcp`
- [官方文档 / Provider documentation](https://docs.chainstack.com/docs/chainstack-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://docs.chainstack.com/mintlify-assets/_mintlify/favicons/chainstack/jo9dYY4MCWk3fHQO/_generated/favicon/android-chrome-192x192.png
