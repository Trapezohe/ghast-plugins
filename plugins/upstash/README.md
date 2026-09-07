# Upstash Redis for Ghast

## 简介 / Overview

查询与管理 Upstash Redis 数据、执行 Redis 命令并搜索官方文档。

Query and manage Upstash Redis data, run Redis commands and search official documentation.

## 连接 / Connection

需要 Node.js 22+ 与 npx。将 Upstash 控制台提供的 Redis REST URL 与 REST Token 分别填入 Ghast 的两个连接字段。只读任务可使用只读 Token。需要支持 credentialEnv 的 Ghast 版本；旧版本无法配置此连接。受账号权限与用量限制。

Requires Node.js 22+ and npx. Copy your Upstash Redis REST URL and REST Token from the provider console into the two Ghast connection fields. Use a read-only token for read-only tasks. Requires a Ghast build with credentialEnv support; older builds cannot configure this connection. Account permissions and usage limits apply.

- MCP: `npx -y @upstash/redis-mcp@0.1.1`
- [官方文档 / Provider documentation](https://github.com/upstash/redis-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://upstash.com/icons/apple-touch-icon.png
