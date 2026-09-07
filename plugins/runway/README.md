# Runway for Ghast

## 简介 / Overview

通过 Runway 官方 MCP 服务生成创意图片与视频。

Generate creative images and videos with Runway’s official MCP service.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Runway OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Runway OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.runwayml.com/mcp`
- [官方文档 / Provider documentation](https://help.runwayml.com/hc/en-us/articles/51931843164691-Connecting-to-Runway-MCP)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://runwayml.com/icon.png?icon.35ps9bmugbe1e.png

验证范围为官方端点及认证元数据、Ghast 本地安装与卸载；未登录真实账号验证生成任务或账号写入。

Validation covers the official endpoint and auth metadata, plus Ghast local installation and removal. Real account generation and account writes have not been tested.

生成消耗 Runway 积分，MCP 不支持 Explore Mode。

Generation consumes Runway credits. MCP does not support Explore Mode.
