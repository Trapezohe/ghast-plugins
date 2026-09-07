# draw.io for Ghast

## 简介 / Overview

通过 draw.io 官方 MCP 工具将 XML、Mermaid 或 CSV 转成可编辑图表。

Create editable diagrams from draw.io XML, Mermaid or CSV using the official MCP tool server.

## 连接 / Connection

需要 Node.js 18 或更高版本及 npx。Ghast 启动官方 @drawio/mcp@1.5.0 工具服务，无需账号或 Token。图表在浏览器编辑器中打开；不包含独立的 MCP Apps 内嵌界面。

Requires Node.js 18 or later and npx. Ghast launches the official @drawio/mcp@1.5.0 tool server. No account or token is required. Diagrams open in the browser editor; the separate MCP Apps inline interface is not included.

- MCP: `npx -y @drawio/mcp@1.5.0`
- [官方文档 / Provider documentation](https://www.drawio.com/docs/manual/generate/drawio-mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp/images/drawlogo-color.svg
