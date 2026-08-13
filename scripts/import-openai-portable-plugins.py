#!/usr/bin/env python3
"""Import the connector-free, redistributable OpenAI marketplace plugins."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


EXPECTED_SOURCE_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
OPENAI_REPOSITORY = "https://github.com/openai/plugins"
PLUGIN_DIR = Path("plugins")
REPORT_PATH = Path("openai-portability.json")

PORTS = {
    "test-android-apps": {
        "category": "development",
        "description": (
            "Test Android apps on a local emulator with reproducible UI "
            "inspection, screenshots, input actions, and log capture."
        ),
        "license": "Apache-2.0",
        "license_files": [
            (
                "plugin",
                "skills/android-emulator-qa/LICENSE.txt",
                "LICENSE",
            )
        ],
        "skills": ["android-emulator-qa"],
        "omitted": [
            {
                "path": "skills/android-performance",
                "reason": "No redistributable license file was present in the source snapshot.",
            }
        ],
    },
}

EXISTING_PORTS = {
    "boltz-api-cli": "Ghast regenerates Boltz directly from the pinned official Boltz repository.",
    "circleci": "Ghast regenerates CircleCI from the MIT-licensed official CLI repository and current CircleCI-operated MCP services.",
    "cloudflare": "Ghast already ships a broader Cloudflare port with public MCP support.",
    "coderabbit": "Ghast regenerates CodeRabbit from its current MIT-licensed official multi-agent skills repository.",
    "expo": "Ghast already ships the portable Expo skills.",
    "hyperframes": "Ghast regenerates HyperFrames directly from the pinned official HeyGen repository.",
    "mixpanel-headless": "Ghast regenerates Mixpanel Headless directly from the pinned official repository.",
    "nvidia": "Ghast regenerates the complete NVIDIA skill catalog directly from the pinned official repository.",
    "remotion": "Ghast already ships a port pinned to the canonical Remotion repository.",
    "render": "Ghast regenerates Render directly from the pinned official Render repository.",
    "sentry": "Ghast already ships the licensed read-only Sentry skill.",
    "superpowers": "Ghast regenerates Superpowers directly from its pinned canonical repository.",
    "temporal": "Ghast already ships a newer canonical Temporal port.",
    "twilio-developer-kit": "Ghast regenerates the Twilio Developer Kit directly from the pinned official Twilio repository.",
}

BLOCKED_PORTS = {
    "build-ios-apps": "The source snapshot declares MIT but contains no license grant for the bundled skills.",
    "build-macos-apps": "The source snapshot declares MIT but contains no license grant for the bundled skills.",
    "build-web-apps": "The source snapshot declares MIT but contains no license grant for the bundled skills.",
    "build-web-data-visualization": "The source snapshot declares MIT but contains no license grant for the bundled skills.",
    "game-studio": "The source snapshot declares MIT but contains no license grant for the bundled skills.",
    "life-science-research": "The marketplace manifest marks this plugin Proprietary.",
    "magicpath": "The marketplace manifest marks this plugin UNLICENSED.",
    "ngs-analysis": "The source snapshot declares MIT but contains no license grant for the bundled skills.",
    "openai-ads-conversions": "The marketplace manifest marks this plugin Proprietary.",
    "plugin-eval": "The source snapshot declares MIT but contains no license grant for the bundled code and skills.",
    "zotero": "The source snapshot declares MIT but contains no license grant for the bundled skill.",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Checkout of github.com/openai/plugins.",
    )
    parser.add_argument(
        "--external-root",
        type=Path,
        help=(
            "Directory containing canonical license checkouts. Defaults to an "
            "'upstreams' directory beside the OpenAI checkout."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    external_root = (
        args.external_root.resolve()
        if args.external_root
        else source.parent / "upstreams"
    )
    source_revision = git_revision(source)
    if source_revision != EXPECTED_SOURCE_REVISION:
        raise ValueError(
            f"{source}: expected revision {EXPECTED_SOURCE_REVISION}, "
            f"found {source_revision}"
        )

    marketplace_path = source / ".agents/plugins/marketplace.json"
    marketplace = json.loads(marketplace_path.read_text())
    entries = {entry["name"]: entry for entry in marketplace["plugins"]}
    connector_free = {
        name
        for name, entry in entries.items()
        if not (source / entry["source"]["path"] / ".app.json").exists()
    }
    classified = set(PORTS) | set(EXISTING_PORTS) | set(BLOCKED_PORTS)
    if connector_free != classified:
        missing = sorted(connector_free - classified)
        stale = sorted(classified - connector_free)
        raise ValueError(
            "Connector-free classification is out of date: "
            f"unclassified={missing}, no-longer-matching={stale}"
        )

    for name, config in PORTS.items():
        import_plugin(
            source=source,
            external_root=external_root,
            entry=entries[name],
            config=config,
            source_revision=source_revision,
        )

    write_report(source_revision)
    print(
        "ported "
        f"{len(PORTS)} plugins, retained {len(EXISTING_PORTS)} existing ports, "
        f"and documented {len(BLOCKED_PORTS)} blocked plugins"
    )
    return 0


def git_revision(repository: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def import_plugin(
    *,
    source: Path,
    external_root: Path,
    entry: dict,
    config: dict,
    source_revision: str,
) -> None:
    name = entry["name"]
    source_dir = source / entry["source"]["path"]
    if (source_dir / ".app.json").exists():
        raise ValueError(f"{source_dir}: connector-backed plugins cannot be imported")

    source_manifest = json.loads(
        (source_dir / ".codex-plugin/plugin.json").read_text()
    )
    external_license = config.get("external_license")
    if external_license:
        external_repository = external_root / external_license["directory"]
        external_revision = git_revision(external_repository)
        if external_revision != external_license["revision"]:
            raise ValueError(
                f"{external_repository}: expected license revision "
                f"{external_license['revision']}, found {external_revision}"
            )
    selected_skills = config.get("skills")
    all_skills = sorted(
        path.name for path in (source_dir / "skills").iterdir() if path.is_dir()
    )
    skills = selected_skills or all_skills
    if not skills:
        raise ValueError(f"{source_dir}: plugin has no skills")

    PLUGIN_DIR.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".{name}-", dir=PLUGIN_DIR) as temp:
        staging_dir = Path(temp)
        skills_dir = staging_dir / "skills"
        skills_dir.mkdir()
        for skill_name in skills:
            source_skill = source_dir / "skills" / skill_name
            if not (source_skill / "SKILL.md").exists():
                raise ValueError(f"{source_skill}: missing SKILL.md")
            shutil.copytree(source_skill, skills_dir / skill_name, copy_function=shutil.copy2)
            remove_codex_agent_metadata(skills_dir / skill_name)

        for source_kind, source_path, target_name in config["license_files"]:
            license_root = source_dir if source_kind == "plugin" else external_root
            license_path = license_root / source_path
            if not license_path.is_file():
                raise ValueError(f"{license_path}: required license file is missing")
            shutil.copy2(license_path, staging_dir / target_name)

        manifest = {
            "name": name,
            "version": f"{source_manifest['version']}-ghast.1",
            "description": config.get(
                "description", source_manifest["description"]
            ),
            "category": config["category"],
            "author": source_manifest.get("author", {"name": "OpenAI"}),
            "homepage": source_manifest.get("homepage", OPENAI_REPOSITORY),
            "repository": OPENAI_REPOSITORY,
            "upstreamRevision": source_revision,
            "upstreamPath": entry["source"]["path"].removeprefix("./"),
            "license": config.get("license", source_manifest["license"]),
            "skills": "./skills/",
        }
        canonical_repository = source_manifest.get("repository")
        if canonical_repository and canonical_repository != OPENAI_REPOSITORY:
            manifest["canonicalRepository"] = canonical_repository
        if external_license:
            manifest["licenseSource"] = {
                "repository": external_license["repository"],
                "revision": external_license["revision"],
            }
        if config.get("omitted"):
            manifest["portStatus"] = "partial"
            manifest["omitted"] = config["omitted"]

        manifest_dir = staging_dir / ".ghast-plugin"
        manifest_dir.mkdir()
        (manifest_dir / "plugin.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        )
        (staging_dir / "README.md").write_text(
            readme_for(name, source_manifest, manifest, config)
        )

        target_dir = PLUGIN_DIR / name
        if target_dir.exists():
            shutil.rmtree(target_dir)
        staging_dir.rename(target_dir)


def remove_codex_agent_metadata(skill_dir: Path) -> None:
    metadata_path = skill_dir / "agents" / "openai.yaml"
    if not metadata_path.exists():
        return
    metadata_path.unlink()
    try:
        metadata_path.parent.rmdir()
    except OSError:
        pass


def readme_for(
    name: str, source_manifest: dict, manifest: dict, config: dict
) -> str:
    display_name = source_manifest.get("interface", {}).get("displayName", name)
    lines = [
        f"# {display_name}",
        "",
        source_manifest["description"],
        "",
        "## Ghast port",
        "",
        (
            "This package contains the connector-free skill payload from "
            f"`{manifest['upstreamPath']}` in `openai/plugins` at "
            f"`{manifest['upstreamRevision']}`."
        ),
        "",
        (
            "The Codex marketplace manifest, screenshots, and OpenAI-specific "
            "agent metadata are not included. A single marketplace icon is "
            "retained by the Ghast icon sync step. The plugin does not contain "
            "an OpenAI `.app.json` connector declaration."
        ),
        "",
    ]
    if manifest.get("canonicalRepository"):
        lines.extend(
            [
                "Canonical project:",
                "",
                f"- {manifest['canonicalRepository']}",
                "",
            ]
        )
    if config.get("omitted"):
        lines.extend(["## Partial port", ""])
        for omitted in config["omitted"]:
            lines.append(f"- `{omitted['path']}`: {omitted['reason']}")
        lines.append("")
    lines.extend(
        [
            "Local CLIs, SDKs, API credentials, or paid services described by "
            "individual skills remain user-managed dependencies.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(source_revision: str) -> None:
    plugins = []
    for name, reason in sorted(EXISTING_PORTS.items()):
        plugins.append({"name": name, "status": "existing", "reason": reason})
    for name, config in sorted(PORTS.items()):
        status = "partial" if config.get("omitted") else "ported"
        reason = (
            "Imported only the explicitly licensed skill subset."
            if status == "partial"
            else "Imported as a connector-free Ghast skill plugin."
        )
        plugins.append({"name": name, "status": status, "reason": reason})
    for name, reason in sorted(BLOCKED_PORTS.items()):
        plugins.append({"name": name, "status": "blocked", "reason": reason})

    counts = Counter(plugin["status"] for plugin in plugins)
    REPORT_PATH.write_text(
        json.dumps(
            {
                "source": OPENAI_REPOSITORY,
                "sourceRevision": source_revision,
                "selectionRule": "Plugin directory does not contain .app.json.",
                "summary": dict(sorted(counts.items())),
                "plugins": sorted(plugins, key=lambda plugin: plugin["name"]),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
