# Allium for Ghast

## 简介 / Overview

通过 Allium 官方 MCP 查询区块链数据、探索钱包数据并管理已保存分析。

Query blockchain datasets, explore wallet data and manage saved analytics with Allium’s official MCP.

## 连接 / Connection

在 Allium 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 X-API-KEY 请求头。不要在聊天中发送凭据，使用受服务配额限制。 在 app.allium.so/settings/api-keys 创建 Allium API Key。Explorer 与实时数据权限、计算限制和计费取决于账号。工具发现本身不能验证 API Key 是否有效。

Create a Allium API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the X-API-KEY header; do not paste credentials into chat. Service quotas apply. Create an Allium API key in app.allium.so/settings/api-keys. Explorer and realtime data permissions, compute limits and billing depend on your account. Tool discovery alone does not verify API-key validity.

- MCP: `https://mcp.allium.so`
- [官方文档 / Provider documentation](https://docs.allium.so/ai/mcp/overview)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/6a1967263e86bd5aff36e280/6a28a7aa166a9dcfbc69121d_694394e6b362de82eb5247d2_allium.png
