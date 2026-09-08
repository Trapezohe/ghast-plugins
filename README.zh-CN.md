# Ghast Plugins

为 Ghast 扩展技能、服务连接、命令和生命周期 Hook。

[English](README.md) · **简体中文**

这里维护 Ghast 的公开插件目录、插件源码和可下载安装包。你可以在 Ghast 桌面应用中浏览 500+ 个插件，覆盖开发者工具、数据、效率、沟通、设计、营销运营和金融等场景。

[浏览插件源码](plugins/) · [查看插件目录](plugin-catalog.json) · [上游维护说明](maintenance/README.md)

## 开始使用

1. 在 Ghast 中打开「插件」，进入「浏览」。
2. 搜索插件，打开详情并点击「安装」。
3. 如果插件需要连接外部服务，在「服务连接」中完成配置。不同服务可能需要 OAuth 授权、API Key 或本地运行环境。
4. 在对话中使用插件。具体能力和前置条件见对应插件的 README。

安装插件**不会直接授予账号访问权限**。安装成功、服务授权成功、工具实际调用成功是三个不同的验证环节。你可以在「已安装」中管理插件。

Ghast 默认使用以下插件目录地址：

```text
https://raw.githubusercontent.com/trapezohe/ghast-plugins/main/plugin-catalog.json
```

客户端会在安装前核对下载包的 SHA-256 摘要。这些安装包适配 Ghast，不依赖 Codex 账号、私有连接器后端或已安装插件缓存。

## 插件可以做什么

| 能力 | 用途 | 示例 |
| --- | --- | --- |
| 技能 | 提供特定任务的操作指导与工作流程 | [Binance](plugins/binance/) |
| MCP 连接 | 调用外部服务或本地服务器提供的工具与数据 | [GitHub](plugins/github/)、[Cloudflare](plugins/cloudflare/)、[Supabase](plugins/supabase/) |
| 命令 | 为重复工作提供明确的调用入口 | 见各插件的命令定义 |
| 生命周期 Hook | 在支持的对话事件发生时补充上下文 | [Ponytail](plugins/ponytail/) |

一个插件可以组合多种能力。具体工具、权限和运行条件取决于插件本身及 Ghast 版本。目前 Hook 支持 `SessionStart`、`UserPromptSubmit` 和 `SubagentStart`，不代表兼容其他客户端的全部 Hook 事件。

办公与协作场景可以从 [Google Gmail](plugins/google-gmail/)、[Google Docs](plugins/google-docs/)、[Google Sheets](plugins/google-sheets/)、[Microsoft Work IQ](plugins/microsoft-workiq/)、[Notion](plugins/notion/) 和 [Slack](plugins/slack/) 开始。目录中既有需要账号授权的连接器，也有无需账号即可使用的插件。

## 来源与上架标准

新增服务连接器必须使用服务商发布或维护的实现。出现在某个插件市场中，不足以证明它是官方连接器。社区连接器需要明确的例外授权，并如实标注来源。

Ghast 为官方服务编写的适配包，不等于服务商亲自发布的插件。每个安装包都应说明实际来源、作者、许可证和适配改动。

官方商店中的每个插件必须具备：

- **真实 Logo**：品牌图标随插件存放，并记录来源。
- **中英文介绍**：中文界面显示中文，其他语言显示默认英文，不将两种介绍拼接展示。
- **可核验来源**：提供上游官方文档或仓库依据，为分发的文件保留适用许可证。
- **可用能力**：说明配置要求，不能把其他客户端的私有应用 ID 当作已经可用的连接器。
- **本地安装验证**：发布前检查安装、品牌展示和卸载；账号授权与真实工具调用另行记录结果。

禁止提交 Token、Client Secret 或账号凭据。不要为了增加数量，把同一个连接器拆成重复条目。

## 仓库结构

| 路径 | 内容 |
| --- | --- |
| [`plugins/`](plugins/) | 插件源码与各插件的使用说明 |
| [`packages/`](packages/) | 自动生成、可重复构建的 ZIP 安装包 |
| [`plugin-catalog.json`](plugin-catalog.json) | Ghast 使用的插件元数据、下载地址和 SHA-256 摘要 |
| [`mcp-registry.json`](mcp-registry.json) | 独立 MCP 服务器目录 |
| [`scripts/`](scripts/) | 构建、校验、导入和审计脚本 |
| [`maintenance/`](maintenance/) | 上游清单、更新策略与维护说明 |

## 贡献插件

安装包采用供应商中立的 Agent Plugins 1.0 格式，以根目录的 `plugin.json` 为入口。技能位于 `skills/`，MCP 配置位于 `mcp.json`；Ghast 专用元数据放在 `extensions.ai.trapezohe.ghast` 中。

优先参考能力相近的现有插件：服务连接可以看 [GitHub](plugins/github/)，Hook 插件可以看 [Ponytail](plugins/ponytail/)。只保留实际需要的文件。

```text
plugins/<name>/
├── plugin.json                  # 清单与 Ghast 元数据
├── assets/                      # 品牌 Logo
├── skills/                      # 可选：技能
├── mcp.json                     # 可选：MCP 配置
├── ai.trapezohe.ghast/commands/  # 可选：Ghast 命令
├── hooks/                       # 可选：在 Ghast 扩展中声明的 Hook
├── README.md                    # 配置、能力、来源与限制
└── LICENSE                      # 适用的再分发许可证
```

在 Ghast 扩展中填写 `descriptions.en` 和 `descriptions.zh-CN`，根字段 `description` 与英文介绍保持一致。分类使用 [`scripts/plugin_categories.py`](scripts/plugin_categories.py) 中的规范值。

在仓库根目录准备校验环境并重新构建：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-agent-plugins.txt
python scripts/build-ghast-catalog.py
python scripts/validate-ghast-repository.py
```

CI 使用 Python 3.12 和 Node.js 24。脚本检查还需要本机可用的 Node.js 与 Bash。校验范围包括清单、MCP 配置、技能、图标、脚本语法、包结构、摘要和常见硬编码密钥模式；校验通过不等于真实账号连接已经可用。

在 Ghast 中安装生成的包，检查界面展示和相关运行行为，然后卸载测试安装。通过 PR 一并提交源码、重新生成的安装包和目录文件。保留上游许可证，记录兼容性改动。导入脚本用于经过审核、固定版本的上游源码，不用于整站镜像其他插件市场。

## 版本规则

插件直接使用已核验的上游清单或官方发行版本，不添加 Ghast 后缀。版本来源、对应的打包提交和证据摘要记录在 `maintenance/upstreams.json` 的 `versionSource` 中。没有可核验上游包版本时，清单省略 `version`，不拿 API 协议版本或仓库中无关依赖包的版本代替。

目录构建器会在打包前将这项规则应用到源码清单，包括旧导入脚本生成的内容。更新上游快照时，需要同时更新对应版本证据；版本证据与打包提交不一致会导致校验失败。Ghast 适配、翻译或 Logo 的修改通过 Git 和安装包 SHA-256 追踪；即使上游版本没变，客户端也能识别包内容变化。

## 如何保持更新

维护工作流配置为每日检查上游，将变化集中到一个待审核 PR。**创建 PR 的权限仍待开启**：需要在仓库设置中允许 GitHub Actions 创建 PR。

自动发现更新不等于自动改写全部插件。当前清单支持检查 GitHub 修订、npm/PyPI 发布版本和固定 HTTPS 地址；无法自动识别的来源需要人工处理。目前仅 Ponytail 配置了带文件校验的自动更新映射，其他变化先生成审核信息，不会直接覆盖插件内容。

更新不会自动合并。端点返回结果不能代替完整的 MCP 或账号测试；仓库更新也不代表用户已经安装的插件会自动升级。

调度、权限、校验、失败报告和当前限制详见[维护指南](maintenance/README.md)。

## 许可证

许可证按插件分别定义。再分发前，请查看对应清单、README 和附带的许可证文件。适配包的许可证不涵盖服务商托管服务、商标或用户数据；相关使用仍受服务商条款约束。
