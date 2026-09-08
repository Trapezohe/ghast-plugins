# Next.js DevTools for Ghast

## 简介 / Overview

通过 Vercel 官方 DevTools MCP 连接器检查运行中的 Next.js 应用，查询运行时错误、路由和日志。

Inspect running Next.js applications through Vercel’s official DevTools MCP connector for runtime errors, routes and logs.

## 连接 / Connection

需要 npx 和 Node.js >=20.19（建议受支持的 LTS 版本），无需账号或 Token。运行时检查需要正在运行的 Next.js 16+ 开发服务器；访问前确认目标端口。0.4 版的文档与浏览器工具返回本地文档或 CLI 使用指引，不会自行抓取文档或控制浏览器。本插件配置关闭使用统计。

Requires npx and Node.js >=20.19 (use a supported LTS release). No account or token is required. Runtime inspection needs a running Next.js 16+ development server; confirm the intended port before access. Version 0.4 documentation and browser tools return local documentation or CLI instructions, rather than fetching documents or controlling a browser themselves. Plugin telemetry is disabled.

- MCP: `npx -y next-devtools-mcp@0.4.0`
- [官方文档 / Provider documentation](https://github.com/vercel/next-devtools-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://assets.vercel.com/image/upload/v1662130559/nextjs/Icon_dark_background.png
