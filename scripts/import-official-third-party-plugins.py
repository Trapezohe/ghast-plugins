#!/usr/bin/env python3
"""Import audited plugins directly from their developers' repositories."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


PLUGIN_DIR = Path("plugins")
PLUGINS = {
    "boltz-api-cli": {
        "directory": "boltz-api-skills",
        "revision": "70e480ebb14baecfc4456b49eb8b724611470b7c",
        "repository": "https://github.com/boltz-bio/boltz-api-skills",
        "plugin_root": "plugins/boltz-api-cli",
        "manifest": ".codex-plugin/plugin.json",
        "license": "../../LICENSE",
        "icon": "assets/app-icon.png",
        "category": "research",
        "license_name": "MIT",
    },
    "cloudflare": {
        "directory": "cloudflare-skills",
        "revision": "f96bff754e428838818017f75817f0f9428acd48",
        "repository": "https://github.com/cloudflare/skills",
        "plugin_root": ".",
        "manifest": ".claude-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "logo.svg",
        "category": "development",
        "homepage": "https://workers.cloudflare.com",
        "author": {
            "name": "Cloudflare",
            "url": "https://workers.cloudflare.com",
        },
        "description": (
            "Build and operate on Cloudflare with official skills, slash "
            "commands, and five official MCP servers."
        ),
        "commands": "commands",
        "mcp": ".mcp.json",
        "license_name": "Apache-2.0",
    },
    "expo": {
        "directory": "expo-skills",
        "revision": "dcff9e7cd61f79ee821e18b5b215d5585eaac441",
        "repository": "https://github.com/expo/skills",
        "plugin_root": "plugins/expo",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/expo.png",
        "category": "development",
        "mcp": ".mcp.json",
        "license_name": "MIT",
        "compatibility_notes": [
            (
                "The Expo telemetry status command uses Ghast's "
                "host-resolved <SKILL_DIR> placeholder instead of the "
                "Claude-only CLAUDE_PLUGIN_ROOT environment variable."
            ),
            (
                "Claude hooks and Codex-only agent metadata are not included "
                "because Ghast does not execute those client extension points."
            ),
        ],
    },
    "hyperframes": {
        "directory": "hyperframes",
        "revision": "9b0c5e85596efaf93823bf5f19b7f1d1216ca7d5",
        "repository": "https://github.com/heygen-com/hyperframes",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/icon.png",
        "category": "creativity",
        "license_name": "Apache-2.0",
    },
    "mixpanel-headless": {
        "directory": "mixpanel-headless",
        "revision": "6c2c2f975d51628bdbc75802fb879d4f6cb66f69",
        "repository": "https://github.com/mixpanel/mixpanel-headless",
        "plugin_root": "mixpanel-plugin",
        "manifest": ".claude-plugin/plugin.json",
        "license": "../LICENSE",
        "category": "data",
        "license_name": "MIT",
        "commands": "commands",
        "extra_directories": ["docs"],
        "generated_icon": "./assets/icon.png",
        "compatibility_notes": [
            (
                "Skill-local helper paths use Ghast's host-resolved "
                "<SKILL_DIR> placeholder instead of Claude-only variables."
            ),
            (
                "The auth slash command routes through the official mp CLI, "
                "so it remains runnable without a plugin-root environment "
                "variable."
            ),
            (
                "The setup dependency list explicitly includes click>=8.1 "
                "because the pinned official CLI imports click directly but "
                "does not declare it as a direct package dependency."
            ),
        ],
    },
    "nvidia": {
        "directory": "nvidia-skills",
        "revision": "aa116673017bf75f9885edabab34d8ec883c0a3a",
        "repository": "https://github.com/NVIDIA/skills",
        "plugin_root": "plugins/nvidia-skills",
        "manifest": ".codex-plugin/plugin.json",
        "license": "../../LICENSE-APACHE",
        "additional_licenses": [
            ["../../LICENSE-CC-BY-4.0", "LICENSE-CC-BY-4.0"]
        ],
        "icon": "assets/nvidia.png",
        "category": "development",
        "license_name": "Apache-2.0 AND CC-BY-4.0",
        "skills_root": "skills",
        "skills_from_repository_root": True,
        "preserve_agent_metadata": True,
        "compatibility_notes": [
            (
                "NVIDIA's signed skill directories, agent metadata, skill "
                "cards, evaluations, and detached signatures are retained "
                "byte-for-byte so the official trust chain is not broken."
            ),
        ],
        "extra_repository_files": [
            ["nv-agent-root-cert.pem", "nv-agent-root-cert.pem"]
        ],
        "description": (
            "Complete pinned catalog of NVIDIA-verified skills for GPU "
            "acceleration, CUDA, AI, data, training, inference, robotics, "
            "Physical AI, Omniverse, simulation, networking, and more."
        ),
    },
    "remotion": {
        "directory": "remotion",
        "revision": "a23672203e00db3d9ad905b2b2088bdc6aa2f2ac",
        "repository": "https://github.com/remotion-dev/remotion",
        "plugin_root": "packages/codex-plugin",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/icon.png",
        "category": "creativity",
        "remotion_build": True,
        "license_name": "MIT",
        "compatibility_notes": [
            (
                "The official generated skill build is reproduced without "
                "Codex-only agent metadata and with preview guidance adapted "
                "to Ghast's browser."
            ),
        ],
    },
    "render": {
        "directory": "render",
        "revision": "14032768453fd21c57f7e3a9c0e7659a2c7dce9d",
        "repository": "https://github.com/renderinc/render-codex-plugin",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/logo.svg",
        "category": "development",
        "mcp": ".mcp.json",
        "license_name": "MIT",
    },
    "temporal": {
        "directory": "temporal-codex-plugin",
        "revision": "a3fa2bdff73a93e60e1077c08bde2b682cd0f5ae",
        "repository": "https://github.com/temporalio/codex-temporal-plugin",
        "plugin_root": "plugins/temporal",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/temporal-logo.svg",
        "category": "development",
        "license_name": "MIT",
    },
    "superpowers": {
        "directory": "superpowers",
        "revision": "b36e0829c6d0140e93cfef2ca599b1b07d4a7797",
        "repository": "https://github.com/obra/superpowers",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/app-icon.png",
        "category": "development",
        "license_name": "MIT",
    },
    "twilio-developer-kit": {
        "directory": "twilio-ai",
        "revision": "d7b0f231468cd9a6a0bab9ebcde8c1a5c9220bba",
        "repository": "https://github.com/twilio/ai",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "category": "development",
        "license_name": "MIT",
        "recursive_skills": True,
        "generated_icon": "./assets/icon.svg",
        "frontmatter_overrides": {
            "twilio-agent-connect": (
                "Integrate agentic applications with Twilio Agent Connect "
                "across identity, memory, orchestration, Voice, SMS, RCS, "
                "WhatsApp, and Chat."
            )
        },
        "compatibility_notes": [
            (
                "A minimal Ghast-compatible frontmatter block is added to "
                "twilio-agent-connect because that official skill is the "
                "only source skill without one."
            ),
        ],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        required=True,
        help="Directory containing the pinned official repository checkouts.",
    )
    return parser.parse_args()


def main() -> int:
    source_root = parse_args().source_root.resolve()
    for name, config in PLUGINS.items():
        import_plugin(name, config, source_root)
    print(f"imported {len(PLUGINS)} plugins from official developer repositories")
    return 0


def import_plugin(name: str, config: dict, source_root: Path) -> None:
    repository = source_root / config["directory"]
    actual_remote = normalized_git_remote(repository)
    expected_remote = normalized_repository_url(config["repository"])
    if actual_remote != expected_remote:
        raise ValueError(
            f"{repository}: expected origin {config['repository']}, "
            f"found {actual_remote}"
        )
    revision = git_revision(repository)
    if revision != config["revision"]:
        raise ValueError(
            f"{repository}: expected revision {config['revision']}, found {revision}"
        )

    plugin_root = repository / config["plugin_root"]
    source_manifest = json.loads(
        (plugin_root / config["manifest"]).read_text()
    )
    license_path = plugin_root / config["license"]
    if not license_path.is_file():
        raise ValueError(f"{license_path}: license is missing")

    with tempfile.TemporaryDirectory(prefix=f".{name}-", dir=PLUGIN_DIR) as temp:
        staging = Path(temp)
        skills_target = staging / "skills"
        if config.get("remotion_build"):
            build_remotion_skills(repository, skills_target)
        else:
            skills_root = (
                repository / config["skills_root"]
                if config.get("skills_from_repository_root")
                else plugin_root / config.get("skills_root", "skills")
            )
            copy_skill_tree(
                skills_root,
                skills_target,
                recursive=config.get("recursive_skills", False),
                preserve_agent_metadata=config.get(
                    "preserve_agent_metadata", False
                ),
                frontmatter_overrides=config.get(
                    "frontmatter_overrides", {}
                ),
            )

        if config.get("commands"):
            shutil.copytree(
                plugin_root / config["commands"],
                staging / "commands",
                copy_function=shutil.copy2,
            )
        if config.get("mcp"):
            shutil.copy2(plugin_root / config["mcp"], staging / ".mcp.json")
        for directory in config.get("extra_directories", []):
            shutil.copytree(
                plugin_root / directory,
                staging / directory,
                copy_function=shutil.copy2,
            )

        apply_ghast_compatibility(name, staging)

        shutil.copy2(license_path, staging / "LICENSE")
        for source_name, target_name in config.get("additional_licenses", []):
            shutil.copy2(plugin_root / source_name, staging / target_name)
        for source_name, target_name in config.get(
            "extra_repository_files", []
        ):
            shutil.copy2(repository / source_name, staging / target_name)

        if config.get("icon"):
            icon_source = plugin_root / config["icon"]
            icon_target = staging / "assets" / f"icon{icon_source.suffix.lower()}"
            icon_target.parent.mkdir()
            shutil.copy2(icon_source, icon_target)
            icon_manifest_path = f"./{icon_target.relative_to(staging)}"
        else:
            icon_manifest_path = config["generated_icon"]

        manifest = {
            "name": name,
            "version": f"{source_manifest.get('version', '1.0.0')}-ghast.1",
            "description": config.get(
                "description", source_manifest["description"]
            ),
            "category": config["category"],
            "author": config.get("author", source_manifest.get("author")),
            "homepage": config.get(
                "homepage",
                source_manifest.get("homepage", config["repository"]),
            ),
            "repository": config["repository"],
            "upstreamRevision": revision,
            "upstreamPath": config["plugin_root"],
            "license": config["license_name"],
            "icon": icon_manifest_path,
            "skills": "./skills/",
        }
        if config.get("commands"):
            manifest["commands"] = "./commands/"
        if config.get("mcp"):
            manifest["mcpServers"] = "./.mcp.json"

        manifest_dir = staging / ".ghast-plugin"
        manifest_dir.mkdir()
        (manifest_dir / "plugin.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        )
        (staging / "README.md").write_text(
            render_readme(name, source_manifest, manifest, config)
        )

        target = PLUGIN_DIR / name
        if target.exists():
            shutil.rmtree(target)
        staging.rename(target)


def copy_skill_tree(
    source: Path,
    target: Path,
    *,
    recursive: bool,
    preserve_agent_metadata: bool,
    frontmatter_overrides: dict[str, str],
) -> None:
    if not source.is_dir():
        raise ValueError(f"{source}: skills directory is missing")
    target.mkdir()
    copied = 0
    source_skills = (
        sorted(path.parent for path in source.rglob("SKILL.md"))
        if recursive
        else sorted(path for path in source.iterdir() if path.is_dir())
    )
    names = [path.name for path in source_skills if (path / "SKILL.md").is_file()]
    if len(names) != len(set(names)):
        raise ValueError(f"{source}: recursive skill names are not unique")
    for source_skill in source_skills:
        if not (source_skill / "SKILL.md").is_file():
            continue
        target_skill = target / source_skill.name
        shutil.copytree(
            source_skill,
            target_skill,
            copy_function=shutil.copy2,
            ignore=(
                None
                if preserve_agent_metadata
                else shutil.ignore_patterns("openai.yaml")
            ),
        )
        if not preserve_agent_metadata:
            remove_empty_directories(target_skill)
        ensure_skill_frontmatter(
            target_skill / "SKILL.md",
            skill_name=source_skill.name,
            description=frontmatter_overrides.get(source_skill.name),
        )
        copied += 1
    if not copied:
        raise ValueError(f"{source}: no valid skills")


def ensure_skill_frontmatter(
    skill_path: Path, *, skill_name: str, description: str | None
) -> None:
    text = skill_path.read_text()
    if text.startswith("---\n") and text.find("\n---\n", 4) >= 0:
        return
    if not description:
        raise ValueError(
            f"{skill_path}: official skill lacks frontmatter and no "
            "compatibility description is configured"
        )
    frontmatter = (
        "---\n"
        f"name: {skill_name}\n"
        "description: >-\n"
        f"  {description}\n"
        "---\n\n"
    )
    skill_path.write_text(frontmatter + text)


def apply_ghast_compatibility(name: str, staging: Path) -> None:
    if name == "expo":
        rewrite_text(
            staging / "skills/expo-skill-feedback/SKILL.md",
            {
                '"${CLAUDE_PLUGIN_ROOT}/skills/expo-skill-feedback/scripts/telemetry.cjs"': (
                    '"<SKILL_DIR>/scripts/telemetry.cjs"'
                )
            },
        )
    elif name == "mixpanel-headless":
        for markdown in (staging / "skills").rglob("*.md"):
            rewrite_text(
                markdown,
                {"${CLAUDE_SKILL_DIR}": "<SKILL_DIR>"},
                require_all=False,
            )
        rewrite_text(
            staging / "skills/setup/SKILL.md",
            {
                (
                    "python3 <SKILL_DIR>/../mixpanelyst/scripts/"
                    "auth_manager.py session"
                ): "mp session --format json",
                (
                    "python3 <SKILL_DIR>/../mixpanelyst/scripts/"
                    "auth_manager.py account test"
                ): "mp account test",
            },
        )
        rewrite_text(
            staging / "skills/setup/scripts/setup.sh",
            {
                (
                    "DEPS=(pandas numpy matplotlib seaborn 'networkx>=3.0' "
                    "'anytree>=2.8.0' scipy)"
                ): (
                    "DEPS=(pandas numpy matplotlib seaborn 'networkx>=3.0' "
                    "'anytree>=2.8.0' 'click>=8.1' scipy)"
                )
            },
        )
        (staging / "commands/auth.md").write_text(
            render_mixpanel_auth_command()
        )


def rewrite_text(
    path: Path,
    replacements: dict[str, str],
    *,
    require_all: bool = True,
) -> None:
    text = path.read_text()
    for old, new in replacements.items():
        if require_all and old not in text:
            raise ValueError(f"{path}: expected compatibility marker is missing: {old}")
        text = text.replace(old, new)
    path.write_text(text)


def render_mixpanel_auth_command() -> str:
    return """---
name: mixpanel-headless:auth
description: Manage Mixpanel authentication, accounts, projects, workspaces, targets, and bridge status through the official mp CLI.
argument-hint: [session|login|account|project|workspace|target|bridge] [...]
---

# Mixpanel Authentication Management

Use the official `mp` CLI installed by `mixpanel-headless`. Parse
`$ARGUMENTS`, run the matching command below, and present the result
conversationally. Never invent an account, project, workspace, or target ID.

## Security rules

- Never ask for passwords, API secrets, or bearer tokens in conversation.
- Never pass a secret as a CLI argument.
- Prefer `mp login` for interactive OAuth.
- For service accounts, instruct the user to run `mp account add` themselves;
  it prompts with hidden input or accepts `--secret-stdin`.
- Use environment variables for non-interactive credentials.

## Routing

With no arguments or `session`, run:

```bash
mp session --format json
```

For `login`, tell the user the browser flow may open, then run:

```bash
mp login
```

Useful login flags are `--name`, `--region us|eu|in`, `--project`,
`--service-account`, `--token-env`, `--secret-stdin`, and `--no-browser`.

### Accounts

```bash
mp account list --format json
mp account show <NAME>
mp account use <NAME>
mp account test <NAME>
mp account login <NAME>
mp account logout <NAME>
```

For account creation, guide the user to one of these official flows:

```bash
mp login --name <NAME> --region <REGION>
mp account add <NAME> --type service_account --username <USERNAME> --project <PROJECT_ID> --region <REGION>
mp account add <NAME> --type oauth_token --token-env <ENV_VAR> --project <PROJECT_ID> --region <REGION>
```

Do not run `account add` on the user's behalf when it would require handling a
secret. After the user completes it, verify with `mp account test <NAME>`.

### Projects

```bash
mp project list --format json
mp project show
mp project use <PROJECT_ID>
```

If `project use` has no ID, list projects first and ask the user to choose.

### Workspaces

```bash
mp workspace list --format json
mp workspace show
mp workspace use <WORKSPACE_ID>
```

If `workspace use` has no ID, list workspaces first and ask the user to choose.

### Targets

```bash
mp target list --format json
mp target show <NAME> --format json
mp target add <NAME> --account <ACCOUNT> --project <PROJECT_ID> [--workspace <WORKSPACE_ID>]
mp target use <NAME>
```

Before adding a target, collect its name, account, project, and optional
workspace. These are identifiers, not secrets.

### Bridge

For bridge status, run:

```bash
mp session --bridge --format json
```

To create a bridge at an explicit path, guide the user to:

```bash
mp account export-bridge [<ACCOUNT>] --to <PATH> [--project <PROJECT_ID>] [--workspace <WORKSPACE_ID>]
```

## Non-interactive authentication

Supported environment combinations include:

```text
MP_USERNAME + MP_SECRET + MP_PROJECT_ID + MP_REGION
MP_OAUTH_TOKEN + MP_PROJECT_ID + MP_REGION
```

Never print their values. When a command fails, report the CLI's concrete error
and suggest the smallest matching recovery command.
"""


def build_remotion_skills(repository: Path, target: Path) -> None:
    source = repository / "packages/skills/skills"
    target.mkdir()
    for source_skill in sorted(path for path in source.iterdir() if path.is_dir()):
        target_skill = target / source_skill.name
        shutil.copytree(
            source_skill,
            target_skill,
            copy_function=shutil.copy2,
            ignore=ignore_remotion_build_files,
        )
        remove_empty_directories(target_skill)

    prepare_remotion_embedded_skills(target)
    remotion_create = target / "remotion-create/SKILL.md"
    text = remotion_create.read_text()
    preview_phrases = [
        "Instead of rendering the video, consider starting the preview server for faster iteration:",
        "Start the preview server after building the composition:",
    ]
    for phrase in preview_phrases:
        if phrase in text:
            text = text.replace(
                phrase,
                "After creating or updating the video, start the preview server by default:",
            )
            break
    text = text.replace(
        "If an in-harness browser is available, open it there.",
        (
            "Open the exact URL in Ghast's available browser. If no browser "
            "tool is available, keep the preview server running and provide "
            "the URL to the user."
        ),
    )
    remotion_create.write_text(text)


def ignore_remotion_build_files(directory: str, names: list[str]) -> set[str]:
    ignored = {name for name in names if name.endswith(".tsx")}
    if Path(directory).name == "agents":
        ignored.add("openai.yaml")
    return ignored


def prepare_remotion_embedded_skills(skills_root: Path) -> None:
    roots = [
        (
            skills_root / "remotion-best-practices/remotion-markup",
            "REFERENCE.md",
        ),
        (skills_root / "remotion-markup", "SKILL.md"),
        (skills_root / "remotion-best-practices", "SKILL.md"),
    ]
    for embedded_root, parent_entry in roots:
        if not embedded_root.exists():
            continue
        embedded_names = sorted(
            child.name
            for child in embedded_root.iterdir()
            if child.is_dir()
            and child.name != "rules"
            and (child / "SKILL.md").is_file()
        )
        parent_name = embedded_root.name
        for markdown in embedded_root.rglob("*.md"):
            text = markdown.read_text()
            text = text.replace(
                f"../{parent_name}/SKILL.md", f"../{parent_entry}"
            ).replace(f"../{parent_name}/", "../")
            if parent_name == "remotion-markup":
                text = text.replace(
                    "../../../remotion-interactivity/SKILL.md",
                    "../../../../remotion-interactivity/SKILL.md",
                )
            for skill_name in embedded_names:
                text = text.replace(
                    f"{skill_name}/SKILL.md",
                    f"{skill_name}/REFERENCE.md",
                )
            markdown.write_text(text)
        for skill_name in embedded_names:
            (embedded_root / skill_name / "SKILL.md").rename(
                embedded_root / skill_name / "REFERENCE.md"
            )


def remove_empty_directories(root: Path) -> None:
    directories = sorted(
        (path for path in root.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    )
    for directory in directories:
        try:
            directory.rmdir()
        except OSError:
            pass


def render_readme(
    name: str,
    source_manifest: dict,
    manifest: dict,
    config: dict,
) -> str:
    display_name = (source_manifest.get("interface") or {}).get(
        "displayName", name
    )
    lines = [
            f"# {display_name}",
            "",
            manifest["description"],
            "",
            "## Official Ghast port",
            "",
            (
                "This package is generated directly from the developer-owned "
                f"repository `{manifest['repository']}` at "
                f"`{manifest['upstreamRevision']}`."
            ),
            "",
    ]
    if config.get("preserve_agent_metadata"):
        lines.extend(
            [
                (
                    "Ghast replaces only the marketplace manifest. Signed "
                    "skill directories and their developer metadata remain "
                    "byte-for-byte from the pinned official repository."
                ),
                "",
            ]
        )
    else:
        lines.extend(
            [
                (
                    "Skills, references, scripts, commands, and public MCP "
                    "declarations remain sourced from the pinned official "
                    "repository. Unsupported client metadata is omitted."
                ),
                "",
            ]
        )
    compatibility_notes = config.get("compatibility_notes", [])
    if compatibility_notes:
        lines.extend(["## Ghast compatibility", ""])
        lines.extend(f"- {note}" for note in compatibility_notes)
        lines.append("")
    lines.extend(
        [
            (
                "External CLIs, accounts, credentials, paid services, and "
                "platform permissions remain user-managed dependencies."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def git_revision(repository: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def normalized_git_remote(repository: Path) -> str:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return normalized_repository_url(result.stdout.strip())


def normalized_repository_url(url: str) -> str:
    value = url.removesuffix(".git").rstrip("/")
    if value.startswith("git@github.com:"):
        value = f"https://github.com/{value.removeprefix('git@github.com:')}"
    return value


if __name__ == "__main__":
    raise SystemExit(main())
