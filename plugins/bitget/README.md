# Bitget for Ghast

## 简介 / Overview

查询加密货币行情，处理 Bitget 账户、订单与持仓工作流。

Explore crypto market data and manage Bitget account, order and position workflows.

## 连接 / Connection

需要 Node.js 22+ 与 npx。在 Ghast 连接设置中填写 Bitget API Key、Secret Key 与 Passphrase。分析任务可使用只读 API 权限；账户操作取决于密钥权限。需要支持 credentialEnv 的 Ghast 版本，受地区与账号限制。

Requires Node.js 22+ and npx. Enter your Bitget API Key, Secret Key and Passphrase in Ghast connection settings. Use read-only API permissions for analysis; account actions depend on permissions granted to the key. Requires a Ghast build with credentialEnv support. Region availability and account restrictions apply.

- MCP: `npx -y @bitget-ai/bitget-agent-mcp@3.3.0`
- [官方文档 / Provider documentation](https://github.com/Bitget-AI/agent-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.bitget.com/baseasset/favicon4.png
