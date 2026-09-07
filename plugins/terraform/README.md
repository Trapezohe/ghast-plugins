# Terraform for Ghast

## 简介 / Overview

通过 HashiCorp 官方 MCP 查找 Terraform Provider、模块与策略文档。

Find Terraform providers, modules and policy documentation using HashiCorp’s official MCP server.

## 连接 / Connection

连接前请安装 HashiCorp 官方 terraform-mcp-server 可执行文件并加入 PATH。本包已测试 1.3.0，只启用公开 registry 工具集，无需 Token；当前配置不包含私有 HCP Terraform 工作区操作。

Install HashiCorp’s official terraform-mcp-server binary on PATH before connecting. Tested with version 1.3.0. This package enables the public registry toolset only; no token is required. Private HCP Terraform workspaces are outside this package’s configured toolset.

- MCP: `terraform-mcp-server stdio --toolsets=registry`
- [官方文档 / Provider documentation](https://developer.hashicorp.com/terraform/mcp-server/deploy/local)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://developer.hashicorp.com/_next/static/media/svg-sprite.e0bb55ed.svg#flight-terraform-fill-16
