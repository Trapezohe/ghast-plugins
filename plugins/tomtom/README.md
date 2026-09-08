# TomTom for Ghast

## 简介 / Overview

通过 TomTom 地图查找地点、解析地址、比较路线和查看交通，辅助出行与物流规划。

Find places, geocode addresses, compare routes and inspect traffic with TomTom Maps.

## 连接 / Connection

在 Ghast 连接设置填写 TomTom API Key，启用 MCP Server 和任务需要的地图、搜索、路线或交通 API。服务处于公开预览，按 TomTom 用量计费。

Enter a TomTom API key in Ghast connection settings. Enable MCP Server and only the Maps, Search, Routing or Traffic APIs needed for your tasks. Public preview; usage is billed by TomTom.

- MCP endpoint: `https://mcp.tomtom.com/maps`
- [Provider documentation / 官方文档](https://docs.tomtom.com/tomtom-maps-mcp/documentation/quick-setup)
- 安装后在 Ghast 插件详情连接服务；安装成功不代表账号授权或业务调用成功。
- Install in the Ghast plugin store, then connect in the detail page. Installation does not prove account authorization or task execution.
- 本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 插件、私有连接器 ID 或账号凭据。
- Independently authored for Ghast using the provider's public MCP service. No Codex packages, private connector IDs or credentials are included.
- 如需撤销授权，请同时检查服务商账号的授权设置。To revoke provider access, also review connected applications in your provider account.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Service names and brand assets belong to their respective owners. 品牌标识归相应权利人所有。

Brand logo source: https://cdn.simpleicons.org/tomtom/DF1B12


## Browser authorization / 浏览器授权

`tomtom` publishes OAuth authorization metadata. Ghast prefers browser authorization; an existing API key or token remains an optional advanced alternative. The service advertises dynamic registration or client metadata documents. Discovery was checked without signing in; account authorization and tool execution were not tested.

Ghast 优先使用浏览器授权；已有 API Key 或 Token 保留为高级备选项。服务公开提供动态注册或客户端元数据文档支持。本次只验证了公开授权元数据，没有登录账户或执行工具。

Official discovery: [tomtom resource metadata](https://mcp.tomtom.com/.well-known/oauth-protected-resource/maps) · [authorization metadata](https://oauth.my.tomtom.com/.well-known/oauth-authorization-server)
