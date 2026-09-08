# QuestDB for Ghast

## 简介 / Overview

通过 QuestDB 官方 MCP 连接 Web Console，进行 SQL 查询、结构探索、笔记本编辑、图表和实时仪表盘制作。

Connect QuestDB’s official MCP to your Web Console for SQL, schema exploration, notebooks, charts and live dashboards.

## 连接 / Connection

需要 Node.js 22 或更新版本以及 npx。在 Ghast 连接输入框填写正在运行的 QuestDB Web Console 的源地址，例如本地实例的 http://127.0.0.1:9000。此项为 URL 设置，不是 API 密钥。官方桥接程序在用户同意配对后使用浏览器已登录会话，不接收数据库凭据。本包固定为 0.4.0；控制台底部 MCP 状态入口显示所需版本，双方必须兼容。已验证启动和 35 个工具发现，未配对的文档请求被拒绝。未测试已登录控制台配对或数据库业务操作。

Requires Node.js 22 or later and npx. Enter the origin of your running QuestDB Web Console in Ghast’s connection field, for example http://127.0.0.1:9000 for a local instance. This is a URL setting, not an API secret. The official bridge uses the browser’s authenticated session after user-approved pairing and does not accept database credentials. Version 0.4.0 is pinned; the Web Console MCP status pill shows the expected version, which must be compatible. Startup and discovery of 35 tools were verified; an unpaired documentation request was rejected. No authenticated console pairing or database operation was tested.

- MCP: `npx -y @questdb/mcp-server-questdb@0.4.0`
- [官方文档 / Provider documentation](https://questdb.com/docs/getting-started/web-console/mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/52297642?v=4
