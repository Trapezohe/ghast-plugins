# Firecrawl for Ghast

## 简介 / Overview

使用 Firecrawl 提取结构化网页内容、梳理站点，支持调研、数据采集和 SEO 审核。

Extract structured web content, map websites and support research, data collection and SEO audits with Firecrawl.

## 连接 / Connection

通过浏览器 OAuth 连接 Firecrawl，抓取等操作消耗账号额度并受计划限制。

Connect Firecrawl using browser OAuth. Crawls and other operations consume account credits and are subject to plan limits.

- MCP endpoint: `https://mcp.firecrawl.dev/v2/mcp-oauth`
- [Provider documentation / 官方文档](https://github.com/firecrawl/firecrawl-mcp-server)
- 安装后在 Ghast 插件详情连接服务；安装成功不代表账号授权或业务调用成功。
- Install in the Ghast plugin store, then connect in the detail page. Installation does not prove account authorization or task execution.
- 本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 插件、私有连接器 ID 或账号凭据。
- Independently authored for Ghast using the provider's public MCP service. No Codex packages, private connector IDs or credentials are included.
- 如需撤销授权，请同时检查服务商账号的授权设置。To revoke provider access, also review connected applications in your provider account.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Service names and brand assets belong to their respective owners. 品牌标识归相应权利人所有。

Brand logo source: https://www.firecrawl.dev/favicon.png
