# Wrike for Ghast

## 简介 / Overview

使用 Wrike 搜索项目与任务、查看工作进展，整理团队协作和后续待办。

Search projects and tasks, review workload and organize team work and follow-ups with Wrike.

## 连接 / Connection

在 Ghast 连接设置填写 Wrike Permanent Access Token。官方 v2 文档建议依赖 OAuth 动态注册的客户端使用此方式。

Enter a Wrike Permanent Access Token in Ghast connection settings. The official v2 guide recommends tokens for clients that rely on dynamic OAuth client registration.

- MCP endpoint: `https://mcp.wrike.com/v2`
- [Provider documentation / 官方文档](https://developers.wrike.com/docs/setup-other-mcp-clients-with-wrike-mcp)
- 安装后在 Ghast 插件详情连接服务；安装成功不代表账号授权或业务调用成功。
- Install in the Ghast plugin store, then connect in the detail page. Installation does not prove account authorization or task execution.
- 本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 插件、私有连接器 ID 或账号凭据。
- Independently authored for Ghast using the provider's public MCP service. No Codex packages, private connector IDs or credentials are included.
- 如需撤销授权，请同时检查服务商账号的授权设置。To revoke provider access, also review connected applications in your provider account.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Service names and brand assets belong to their respective owners. 品牌标识归相应权利人所有。

Brand logo source: https://www.wrike.com/tp/storage/uploads/ea10c069-f31a-4c6f-ad2e-8e5998be5a95/wrike-website-logo-light.svg

The square icon uses the unchanged brand mark extracted from the official wordmark SVG. 方形图标提取自官方 SVG 中的品牌图形，未改动图形路径。
