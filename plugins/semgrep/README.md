# Semgrep for Ghast

## 简介 / Overview

通过 Semgrep 官方 CLI 内置 MCP 分析代码并排查安全发现。

Analyze code and investigate security findings with the MCP server built into the official Semgrep CLI.

## 连接 / Connection

需要 uv/uvx 与 Python 3.12。在 Ghast 连接凭据填写 Semgrep Application Token。本包使用官方 Semgrep CLI 内置 MCP 命令，不使用已迁移的独立 semgrep-mcp 包。MCP 扫描需要在同一 CLI 环境中通过官方 semgrep login 与 semgrep install-semgrep-pro 流程安装 Pro Engine，并具备相应账号权限。没有 Pro Engine 时工具目录仍可能加载，这不代表扫描可用。 需要支持 stdio credentialEnv 的 Ghast 版本。服务商可能读取本地 .env 文件，请避免冲突配置。

Requires uv/uvx and Python 3.12. Enter your Semgrep application token in Ghast connection credentials. Uses the MCP command integrated in the official Semgrep CLI, not the retired standalone semgrep-mcp package. MCP scanning requires the Semgrep Pro Engine installed in the same CLI environment (official semgrep login and semgrep install-semgrep-pro flow) and appropriate account access. Tool discovery can succeed without the Pro Engine; it does not prove scans work. Requires a Ghast build with stdio credentialEnv support. The provider may load a local .env file; avoid conflicting configuration.

- MCP: `uvx --python 3.12 semgrep==1.176.1 mcp`
- [官方文档 / Provider documentation](https://github.com/semgrep/semgrep/tree/develop/cli/src/semgrep/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://semgrep.dev/build/assets/favicon-CIx-xpG_.svg
