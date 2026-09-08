# Redis for Ghast

## 简介 / Overview

通过 Redis 官方 MCP 服务读取和管理键、数据结构及受支持的搜索功能。

Read and manage Redis keys, data structures and supported search features with Redis’s official MCP server.

## 连接 / Connection

需要 uv／uvx、Python 3.12（uv 可安装）和可访问的 Redis 实例。按需在 Ghast 连接凭据中填写 REDIS_HOST、REDIS_PORT、REDIS_USERNAME、REDIS_PWD；REDIS_DB 可选，默认 0。TLS 连接填写 REDIS_SSL=true。未配置主机和端口时默认为 localhost:6379。建议使用专用、最小权限的 Redis ACL 用户；只读任务使用只读 ACL。自定义 TLS 证书路径和集群模式可通过官方包的环境配置设置。JSON、向量与搜索工具需要 Redis 实例支持对应功能。需要支持 stdio credentialEnv 的 Ghast 版本。采用官方模块入口保留环境配置，避免包 CLI 的默认值覆盖主机、端口及 TLS 设置。

Requires uv/uvx and Python 3.12 (uv can provision it), plus an accessible Redis instance. Enter REDIS_HOST, REDIS_PORT, REDIS_USERNAME and REDIS_PWD in Ghast connection credentials as applicable; REDIS_DB is optional (default 0). Set REDIS_SSL to true for TLS. Unspecified host and port default to localhost:6379. Use a dedicated least-privilege Redis ACL user; read-only tasks should use read-only ACL permissions. Custom TLS certificate paths and cluster mode can be set using the official package environment configuration. JSON, vector and search tools require the corresponding server features. Requires Ghast stdio credentialEnv support. The module entrypoint preserves environment settings; the package CLI defaults otherwise override host, port and TLS environment values.

`uvx --python 3.12 --from redis-mcp-server==0.5.1 python -m src.main`

[官方源码 / Official source](https://github.com/redis/mcp-redis)

This is the database connector; Redis Documentation is a separate documentation service. Installation does not prove access to your database. 本插件连接数据库；Redis Documentation 是独立文档服务。安装成功不代表可以访问你的数据库。

Independently authored for Ghast using the official Redis package; no Codex private connectors or credentials. Ghast 独立编写，使用 Redis 官方包，不包含 Codex 私有连接器或凭据。

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their owners. 品牌名称及标识归相应权利人所有。

Brand logo source: https://redis.io/icon.png?icon.3r8p6nysrg-mh.png
