#!/usr/bin/env python3
"""Build the Ghast Convex adapter from licensed official distributions."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import select
import shutil
import subprocess
import tarfile
import tempfile
import time
import urllib.request
from pathlib import Path


PLUGIN_DIR = Path("plugins")
CONVEX_VERSION = "1.44.0"
CONVEX_TARBALL_URL = (
    "https://registry.npmjs.org/convex/-/convex-1.44.0.tgz"
)
CONVEX_TARBALL_SHA256 = (
    "8bdb320a17ed370b9635611b4c8b951a6913c9a830e470a28934ffe0a5735493"
)
CONVEX_PACKAGE_HASHES = {
    "package/LICENSE": (
        "79aaec53ef1333544088fe80ecb8ec70f2b84f60c0c4157240df0911cf9696c7"
    ),
    "package/package.json": (
        "6c8e6d9324f93c8cdf63df6a03784cf335eaf0bd108a8ae37a1546208cc52fbf"
    ),
    "package/src/cli/mcp.ts": (
        "faef99a281fa0d23faf7a1927cb41b9078cbb566bc1a589dddc8e78e9f620746"
    ),
    "package/src/cli/lib/mcp/tools/index.ts": (
        "0a2f17e111e29986e7e071b8d4167caf16cbffd72addf30c25124057910d38b1"
    ),
    "package/src/cli/lib/aiFiles/skills.ts": (
        "c76cd1b0fb9366d66e6fb19ab41bfe145178d9a151fc324ebd1aab4ad92a5bf5"
    ),
}
ICON_REVISION = "7023eb599ffe326d3f451cdc27a2d88b70b7bb4d"
ICON_TREE = "297523ec4cb6ebcc6253c1e2fe747b96a8840f57"
ICON_LICENSE_SHA256 = (
    "bf17953d82deeee01c06b020e8ee03b27743ef3985e8eb8d674aa35c27eff4f3"
)
ICON_SHA256 = (
    "cd6eaca42d7c12f8be21f07905dc7d042eef9b8342c61f8e0afd8db8f77ca261"
)
MCP_INITIALIZE_SHA256 = (
    "e1637c4cf48c8431e4131bcbc86cdb9dd6edc4155308411804b46f0b1361b1e1"
)
MCP_TOOLS_SHA256 = (
    "5d3be1fb3d20a781021c53b808de2c5286f0dce8b478f77c45e0d2c75c82567d"
)
MCP_TOOL_NAMES = (
    "status",
    "data",
    "tables",
    "functionSpec",
    "run",
    "envList",
    "envGet",
    "envSet",
    "envRemove",
    "runOneoffQuery",
    "logs",
    "insights",
)
MCP_NAMES_SHA256 = (
    "e437e0d8a904de88ddb5062291905f88db94545d726438a39982709ee4f66aff"
)
UPSTREAM_REVISION = (
    "convex-npm-1.44.0-8bdb320a17ed"
    "+icon-7023eb599ffe+tools-5d3be1fb3d20"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--icon-source",
        type=Path,
        required=True,
        help="Pinned checkout of get-convex/convex-agent-plugins.",
    )
    return parser.parse_args()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: object) -> str:
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
    )


def git_value(source: Path, expression: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", expression],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def verify_official_sources(icon_source: Path) -> tuple[bytes, bytes]:
    if git_value(icon_source, "HEAD") != ICON_REVISION:
        raise ValueError("Convex icon source revision changed")
    if git_value(icon_source, "HEAD^{tree}") != ICON_TREE:
        raise ValueError("Convex icon source tree changed")
    icon_license = (icon_source / "LICENSE").read_bytes()
    icon = (icon_source / "assets/logo.png").read_bytes()
    if sha256(icon_license) != ICON_LICENSE_SHA256:
        raise ValueError("Convex MIT license changed")
    if sha256(icon) != ICON_SHA256:
        raise ValueError("Convex official icon changed")

    request = urllib.request.Request(
        CONVEX_TARBALL_URL,
        headers={"User-Agent": "ghast-convex-import/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        tarball = response.read()
    if sha256(tarball) != CONVEX_TARBALL_SHA256:
        raise ValueError("Convex npm tarball changed")
    with tarfile.open(fileobj=io.BytesIO(tarball), mode="r:gz") as archive:
        files = {}
        for name, expected_hash in CONVEX_PACKAGE_HASHES.items():
            member = archive.extractfile(name)
            if member is None:
                raise ValueError(f"Convex npm package is missing {name}")
            content = member.read()
            if sha256(content) != expected_hash:
                raise ValueError(f"Convex npm evidence changed: {name}")
            files[name] = content
    package = json.loads(files["package/package.json"])
    if (
        package.get("name") != "convex"
        or package.get("version") != CONVEX_VERSION
        or package.get("license") != "Apache-2.0"
        or package.get("engines", {}).get("node") != ">=18.0.0"
        or package.get("bin", {}).get("convex") != "bin/main.js"
    ):
        raise ValueError("Convex npm package identity changed")
    return files["package/LICENSE"], icon


def verify_mcp() -> None:
    process = subprocess.Popen(
        ["npx", "--yes", f"convex@{CONVEX_VERSION}", "mcp", "start"],
        cwd="/tmp",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    assert process.stdin is not None
    assert process.stdout is not None
    assert process.stderr is not None

    def send(payload: dict) -> None:
        process.stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
        process.stdin.flush()

    def receive(expected_id: int, timeout: float = 60) -> dict:
        deadline = time.time() + timeout
        while time.time() < deadline:
            readable, _, _ = select.select(
                [process.stdout, process.stderr],
                [],
                [],
                min(1, deadline - time.time()),
            )
            for stream in readable:
                line = stream.readline()
                if stream is process.stdout and line:
                    message = json.loads(line)
                    if message.get("id") == expected_id:
                        return message
            if process.poll() is not None:
                raise ValueError("Convex MCP exited before responding")
        raise TimeoutError("Convex MCP did not respond")

    try:
        send(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "ghast-convex-audit",
                        "version": "1.0.0",
                    },
                },
            }
        )
        initialize = receive(1)["result"]
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        send(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {},
            }
        )
        tools = receive(2)["result"]["tools"]
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

    names = [tool["name"] for tool in tools]
    if canonical_sha256(initialize) != MCP_INITIALIZE_SHA256:
        raise ValueError("Convex MCP initialize result changed")
    if (
        names != list(MCP_TOOL_NAMES)
        or sha256("\0".join(names).encode()) != MCP_NAMES_SHA256
        or canonical_sha256(tools) != MCP_TOOLS_SHA256
    ):
        raise ValueError("Convex MCP tool catalog changed")


def render_skill() -> str:
    return """---
name: convex
description: >-
  Build and inspect Convex backends with the official Convex CLI, project-level
  Agent Skills, and the official 12-tool Convex MCP server.
---

# Convex

Use the official pinned Convex CLI MCP declared by this plugin.

## Project setup

- Work from the intended JavaScript or TypeScript project root.
- For a new project, follow Convex's current scaffold flow. For an existing
  Convex project, inspect `package.json`, `convex/`, schema, generated API, and
  deployment configuration before changing code.
- Run `npx --yes convex@1.44.0 ai-files install` only when the user asks to add
  or refresh Convex project guidance. It writes a managed `AGENTS.md` section
  and installs Convex's current official Agent Skills into `.agents/skills/`.
  Review the resulting diff; do not overwrite unrelated project instructions.
- Use generated types and Convex primitives for schema, queries, mutations,
  actions, auth-aware access, realtime subscriptions, scheduled jobs, file
  storage, components, and web or mobile clients. Validate with the project's
  own typecheck and tests.

## MCP workflow

- Start with `status` and use its exact deployment selector. Default to a local
  or personal development deployment.
- Use `tables`, `functionSpec`, and `insights` for low-risk structure and
  health inspection. Bound `data` and `logs` requests and avoid unrelated PII.
- `runOneoffQuery` is sandboxed and read-only, but its output can contain
  sensitive records. Keep queries narrow and disclose the deployment.
- Before `run`, inspect `functionSpec`. Queries may be read-only, while
  mutations and actions can change data or call external services. Show the
  exact deployment, function, arguments, and effects and obtain explicit
  confirmation for any mutation, action, unknown function, or external call.
- `envGet` and `envList` can expose secrets. Use only when strictly necessary,
  never print secret values, and do not copy them into chat or files.
- `envSet` and `envRemove` are state-changing. Show the deployment and variable
  name, redact the value, explain restart or outage impact, and obtain explicit
  confirmation immediately before the call.

## Production safety

- This plugin intentionally omits `--prod`,
  `--cautiously-allow-production-pii`, and
  `--dangerously-enable-production-deployments`.
- Do not restart the server with any production-enabling flag unless the user
  explicitly requests production access after reviewing the exact data and
  write risks. Prefer a scoped deploy key or isolated development deployment.
- Never infer production intent from a project name, environment file, or
  deployment selector. Treat deploy keys, admin keys, environment values,
  user records, logs, and function arguments as sensitive.
- After an ambiguous write or function error, inspect current state before
  retrying to avoid duplicate mutations, actions, schedules, or external calls.

## License boundary

- The runtime MCP and `ai-files` commands come from the Apache-2.0
  `convex@1.44.0` package.
- Convex's current full Codex marketplace repository and separate Agent Skills
  repository do not publish a license. Their files are not bundled here.
- The included icon comes from Convex's MIT-licensed official agent-plugin
  repository. Do not copy branding or unlicensed plugin files beyond this
  audited asset.
"""


def render_readme() -> str:
    return f"""# convex

Build and inspect Convex backends with Convex's official CLI, project-level
Agent Skills, and the official 12-tool Convex MCP server.

## Official runtime adapter

Ghast runs `npx --yes convex@{CONVEX_VERSION} mcp start`. The npm tarball is
fixed at SHA-256 `{CONVEX_TARBALL_SHA256}` and includes the Apache-2.0 license.
Protocol initialization and the complete ordered tool schema are pinned at
SHA-256 `{MCP_INITIALIZE_SHA256}` and `{MCP_TOOLS_SHA256}`.

The tools are `status`, `data`, `tables`, `functionSpec`, `run`, `envList`,
`envGet`, `envSet`, `envRemove`, `runOneoffQuery`, `logs`, and `insights`.
The default launcher does not enable production deployments, production PII,
or production writes.

Convex's official Codex guide says the OpenAI directory entry is the lighter
ChatGPT-app connector. It recommends the full marketplace build for skills,
subagents, and an error watcher, but that public repository has no license.
Ghast therefore does not redistribute those files. Instead, the included
workflow uses the licensed CLI's `ai-files install` command to install and
refresh current Convex-authored project guidance at runtime.

The catalog icon is copied from Convex's MIT-licensed
`get-convex/convex-agent-plugins` revision `{ICON_REVISION}` and has SHA-256
`{ICON_SHA256}`.

Node.js 18 or newer, npm 7 or newer, network access, a Convex project, and the
appropriate login or scoped deploy key remain user-managed. Deployment data,
logs, environment variables, mutations, actions, schedules, and external
effects remain subject to Convex permissions and explicit confirmation.
"""


def main() -> int:
    args = parse_args()
    icon_source = args.icon_source.resolve()
    apache_license, icon = verify_official_sources(icon_source)
    verify_mcp()

    with tempfile.TemporaryDirectory(prefix=".convex-", dir=PLUGIN_DIR) as temp:
        staging = Path(temp)
        (staging / ".ghast-plugin").mkdir()
        (staging / "skills/convex").mkdir(parents=True)
        (staging / "assets").mkdir()
        manifest = {
            "name": "convex",
            "version": "1.44.0-ghast.1",
            "description": (
                "Build and inspect Convex backends with the official Convex "
                "CLI, project Agent Skills, and 12-tool MCP server."
            ),
            "category": "development",
            "author": {
                "name": "Convex, Inc.",
                "url": "https://www.convex.dev",
            },
            "homepage": "https://docs.convex.dev/ai/using-codex",
            "repository": "https://github.com/get-convex/convex-backend",
            "upstreamRevision": UPSTREAM_REVISION,
            "license": "Apache-2.0 AND MIT",
            "icon": "./assets/icon.png",
            "skills": "./skills/",
            "mcpServers": "./.mcp.json",
        }
        (staging / ".ghast-plugin/plugin.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        )
        (staging / ".mcp.json").write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "convex": {
                            "command": "npx",
                            "args": [
                                "--yes",
                                f"convex@{CONVEX_VERSION}",
                                "mcp",
                                "start",
                            ],
                        }
                    }
                },
                indent=2,
            )
            + "\n"
        )
        (staging / "skills/convex/SKILL.md").write_text(render_skill())
        mit_license = (icon_source / "LICENSE").read_bytes()
        (staging / "LICENSE").write_bytes(
            b"Convex CLI runtime - Apache-2.0\n\n"
            + apache_license
            + b"\n\nConvex catalog icon - MIT\n\n"
            + mit_license
        )
        (staging / "README.md").write_text(render_readme())
        (staging / "assets/icon.png").write_bytes(icon)
        target = PLUGIN_DIR / "convex"
        if target.exists():
            shutil.rmtree(target)
        staging.rename(target)
    print("imported verified Convex official runtime adapter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
