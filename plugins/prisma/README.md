# Prisma Postgres for Ghast

## 简介 / Overview

查看 Prisma Postgres 数据库与表结构、查询数据，并管理获授权的备份流程。

Inspect Prisma Postgres databases and schemas, query data and manage authorized backup workflows.

## 连接 / Connection

在浏览器连接 Prisma Console。托管服务管理 Prisma Postgres，与本地 Prisma CLI 迁移服务不同。

Connect Prisma Console in the browser. The hosted server manages Prisma Postgres; it is separate from the local Prisma CLI migration server.

- MCP endpoint: `https://mcp.prisma.io/mcp`
- [Provider documentation / 官方文档](https://github.com/prisma/mcp)
- 安装后在 Ghast 插件详情连接服务；安装成功不代表账号授权或业务调用成功。
- Install in the Ghast plugin store, then connect in the detail page. Installation does not prove account authorization or task execution.
- 本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 插件、私有连接器 ID 或账号凭据。
- Independently authored for Ghast using the provider's public MCP service. No Codex packages, private connector IDs or credentials are included.
- 如需撤销授权，请同时检查服务商账号的授权设置。To revoke provider access, also review connected applications in your provider account.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Service names and brand assets belong to their respective owners. 品牌标识归相应权利人所有。

Brand logo source: https://cdn.simpleicons.org/prisma/2D3748
