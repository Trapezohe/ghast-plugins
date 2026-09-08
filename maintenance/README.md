# Official upstream maintenance / 官方来源维护

The workflow `Maintain official upstreams` runs daily at 20:23 UTC (04:23 Asia/Singapore).
It also supports manual dispatch with an optional plugin ID. A single-plugin dispatch
is read-only and does not replace the full pending maintenance PR. It needs no user account
credentials for connectors. It checks only the official sources already recorded in
the reviewed plugin metadata; a source record does not replace ownership verification.

## What is automated

- `upstreams.json` inventories every plugin, official provenance, GitHub revisions,
  npm/PyPI releases and literal hosted MCP endpoints. `--inventory` refreshes it after
  adding plugins; CI rejects a stale inventory. Parameterized URLs, custom binaries
  and unclear sources remain explicitly `manual-source-review`.
- Each source is checked once per run even when shared by multiple plugins.
- GitHub checks follow HEAD to detect changes; a discovered commit is not automatically
  trusted or installed. `packagedRevision` is kept separate from `observed.json`.
- `observed.json` records successful observations only. A first baseline means
  "first observed", not "installed version is current". npm `latest`/unpinned launch
  commands remain runtime-floating; observing a release does not pin them.
- HTTP 400/401/403/405/406 means authentication/protocol requirements or access denial,
  not verified health. GET probes do not enumerate tools or invoke account actions.
- Mapped files are downloaded at an immutable commit. Existing file hashes must match
  the reviewed baseline. Ghast manifests, MCP/auth configuration and extension code
  cannot be copied over by a mapping. Package versions and SHA-256 catalog hashes are
  rebuilt after mapped changes. The current executable mapping is **Ponytail only**;
  other changes are automatically reported for adapter review, not silently overwritten.
- One generated branch/PR (`codex/official-upstream-maintenance`) is refreshed, with
  unchanged pending content left alone. Do not edit this branch manually: change the
  mappings/importers on main. No automatic merge is enabled for this initial rollout.
- Changed scripts, rules, licenses and minimum runtime requirements require review.
  Accepted PRs publish to the existing catalog on main. This is the weekly review/release
  queue; it does not force a release on a day when checks fail or review is incomplete.
- Errors produce one updating GitHub Issue, closed on a later successful full run.
  Every run retains its JSON report as an Actions artifact. Watch the repository's
  Actions/Issues notifications to receive failure and review notifications.

## Validation and execution boundaries

Collection runs trusted maintenance scripts and syntax/metadata checks; it never runs
upstream plugin code. PR CI runs Ponytail hooks in a separate ephemeral hosted runner,
with read-only repository access and no connector account secrets. This smoke test is
not Electron installation, OAuth authorization, or production account functionality.
Those checks remain separate release evidence. Other plugin types currently receive
repository/package contract checks, not a blanket claim of live runtime verification.

All actions are pinned to resolved official commit SHAs. `GITHUB_TOKEN` is sufficient
for collection and writing the maintenance branch/PR when the repository permits Actions
to create PRs. Do not add a personal account Token for connectors to this workflow.
A bot-created PR may require workflow approval under GitHub's rules; the preparation job
already runs repository validation, but executable smoke checks must be confirmed before
merge. This workflow does not grant itself approval or bypass branch protection.

## Local commands

```sh
python scripts/maintain-upstreams.py --inventory
python scripts/maintain-upstreams.py --validate
python scripts/test-maintain-upstreams.py
python scripts/maintain-upstreams.py --plugin ponytail --output /tmp/upstreams.json
# In an isolated checkout; prepares files, never pushes:
python scripts/maintain-upstreams.py --apply --output /tmp/upstreams.json
```

Use `GH_TOKEN` in CI. Locally, `GHAST_GH_API=1` uses the already authenticated `gh api`
for GitHub requests without exporting a token. Some macOS Python installations need
`SSL_CERT_FILE=/etc/ssl/cert.pem`; TLS verification must remain enabled.

## Limits that must remain visible

This does not implement client-side plugin auto-upgrade, rollback, or minimum-client
version enforcement. It does not automatically translate newly added upstream features.
GitHub scheduled runs may be delayed; public repositories inactive for 60 days can have
schedules disabled. The latest successful Actions run is the source of freshness evidence.
An independent scheduler/watchdog is still needed if a hard execution SLA is required;
this repository must not claim that a disabled GitHub schedule can monitor itself.

中文：每天自动查源、集中生成一个更新 PR；脚本/规则与兼容性变化需要审查。
Ponytail 已配置可执行同步映射，其余插件的新版自动进入报告，未完成映射的插件
不会伪装成已自动升级。连接器认证、客户端真实安装和商店发布是不同验收阶段。
