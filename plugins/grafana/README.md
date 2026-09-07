# Grafana for Ghast

## 简介 / Overview

通过 Grafana 官方 MCP 探索仪表盘、指标、日志、告警与事件。

Explore dashboards, metrics, logs, alerts and incidents using Grafana’s official MCP server.

## 连接 / Connection

需要 uv/uvx 与 Python 3.12。在 Ghast 连接凭据中填写 Grafana 实例地址及按需授权的 Service Account Token。完整功能需要 Grafana 9.0+；部分工具还需要相应 Grafana 产品、权限或显式启用工具组。 需要支持 stdio credentialEnv 的 Ghast 版本。

Requires uv/uvx and Python 3.12. Enter your Grafana instance URL and a scoped service account token in Ghast connection credentials. Grafana 9.0+ is required for full functionality. Some tools require additional Grafana products, permissions or explicit tool-group enablement. Requires a Ghast build with stdio credentialEnv support.

- MCP: `uvx --python 3.12 mcp-grafana==1.3.0`
- [官方文档 / Provider documentation](https://grafana.com/docs/grafana/latest/developer-resources/mcp/set-up/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/7195757?v=4
