# Ponytail

## 中文

通过 Ghast 生命周期 Hook 注入 Ponytail 极简编码规则，支持会话独立模式与子代理继承。

需要包含插件生命周期 Hook 支持的 Ghast 客户端，以及 PATH 中的 Node.js。安装启用后，新会话默认 full；每次用户提交时注入当前规则，子代理启动时继承父会话模式。`/ponytail lite|full|ultra|off` 切换模式，`stop ponytail` 或 `normal mode` 关闭。状态仅保存到 Ghast 为该插件和会话分配的数据目录，不读取或修改 Codex、Claude 或全局 Ponytail 配置。禁用/卸载后不再注入；已发送给模型的历史内容无法撤回。

此版本只提供核心规则与三类 Hook，不提供上游的状态栏、全局默认值设置、审计和收益报告命令。规则作为 Hook 资源保存，避免 Skills 自动选择在 off 后重新注入规则。客户端尚未发布 Hook 支持时请勿安装；旧客户端会报告没有可运行贡献。

## English

Apply Ponytail’s minimal-code rules through Ghast lifecycle hooks, with per-conversation modes and subagent inheritance.

Requires a Ghast build with plugin lifecycle hooks and Node.js on PATH. New conversations default to full. Rules are supplied on each user submission; subagents inherit the parent conversation mode. Use `/ponytail lite|full|ultra|off`, `stop ponytail`, or `normal mode`. State is confined to Ghast-provided plugin/session storage. No Codex, Claude, or global Ponytail settings are read or changed. Disabling/uninstalling stops future injection; previously sent conversation content cannot be retracted.

This adapter provides the core rules and SessionStart, UserPromptSubmit, SubagentStart only. Upstream statusline, global default settings, audit and gain commands are not included. Rules are hook resources rather than auto-selected skills so off remains effective. Older Ghast builds without hooks reject this hook-only plugin as having no runnable contribution.

## Provenance

Author repository: https://github.com/DietrichGebert/ponytail
Pinned revision: `356918eba965ee1eac64bd3a7f0dd02108350de5`.
`rules/ponytail.md`, `upstream/hooks/ponytail-instructions.js`, and `upstream/hooks/ponytail-config.js` retain the author's bytes under MIT. `hooks/ghast.cjs` is the Ghast-maintained host adapter, also MIT. No Codex plugin implementation or account integration is reused.

Brand logo source: https://github.com/DietrichGebert/ponytail/blob/356918eba965ee1eac64bd3a7f0dd02108350de5/assets/logo.png
The brand remains its owner's property.
