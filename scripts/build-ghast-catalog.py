#!/usr/bin/env python3
"""Build Ghast's downloadable plugin catalog from native plugin sources."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


CATALOG_PATH = Path("plugin-catalog.json")
PACKAGE_DIR = Path("packages")
PLUGIN_DIR = Path("plugins")


def main() -> int:
    PACKAGE_DIR.mkdir(exist_ok=True)

    plugins = []
    package_names = set()
    for plugin_dir in sorted(PLUGIN_DIR.iterdir()):
        manifest_path = plugin_dir / ".ghast-plugin/plugin.json"
        if not plugin_dir.is_dir() or not manifest_path.exists():
            continue

        manifest = json.loads(manifest_path.read_text())
        if manifest["name"] != plugin_dir.name:
            raise ValueError(f"{manifest_path}: name must match directory")
        if (plugin_dir / ".app.json").exists():
            raise ValueError(
                f"{plugin_dir}: OpenAI connector declarations are not portable"
            )
        icon_path = validate_icon(plugin_dir, manifest)
        if manifest.get("repository") and not (plugin_dir / "LICENSE").exists():
            raise ValueError(f"{plugin_dir}: third-party plugins require LICENSE")
        validate_declared_path(plugin_dir, manifest, "skills", "skills")
        validate_declared_path(plugin_dir, manifest, "commands", "commands")
        validate_declared_path(plugin_dir, manifest, "mcpServers", ".mcp.json")
        if (plugin_dir / "skills").exists():
            validate_skills(plugin_dir / "skills")
        if (plugin_dir / ".mcp.json").exists():
            json.loads((plugin_dir / ".mcp.json").read_text())
        manifest_for_catalog = {
            "name": manifest["name"],
            "description": manifest["description"],
            "author": manifest.get("author", ""),
            "icon": manifest["icon"],
        }
        for field in ("version", "homepage", "repository", "upstreamRevision", "license"):
            if field in manifest:
                manifest_for_catalog[field] = manifest[field]
        if (plugin_dir / "skills").exists():
            manifest_for_catalog["skills"] = "./skills/"
        if (plugin_dir / "commands").exists():
            manifest_for_catalog["commands"] = "./commands/"
        if (plugin_dir / ".mcp.json").exists():
            manifest_for_catalog["mcpServers"] = "./.mcp.json"
        zip_path = PACKAGE_DIR / f"{manifest['name']}.zip"
        write_plugin_zip(plugin_dir, zip_path)
        package_names.add(zip_path.name)
        sha256 = hashlib.sha256(zip_path.read_bytes()).hexdigest()

        catalog_entry = {
            "id": manifest["name"],
            "name": manifest["name"],
            "description": manifest["description"],
            "manifest": manifest_for_catalog,
            "package": {
                "url": f"./packages/{zip_path.name}",
                "sha256": sha256,
            },
            "icon": f"./plugins/{manifest['name']}/{icon_path.relative_to(plugin_dir)}",
        }
        for field in ("category", "homepage", "repository", "license"):
            if field in manifest:
                catalog_entry[field] = manifest[field]
        plugins.append(catalog_entry)

    for package_path in PACKAGE_DIR.glob("*.zip"):
        if package_path.name not in package_names:
            package_path.unlink()

    CATALOG_PATH.write_text(
        json.dumps(
            {
                "name": "ghast-plugins",
                "description": "Downloadable Ghast-compatible plugin packages.",
                "plugins": plugins,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )
    print(f"wrote {CATALOG_PATH} with {len(plugins)} plugins")
    return 0


def validate_declared_path(
    plugin_dir: Path, manifest: dict, field: str, relative_path: str
) -> None:
    exists = (plugin_dir / relative_path).exists()
    declared = field in manifest
    if declared and not exists:
        raise ValueError(
            f"{plugin_dir}: manifest field {field!r} points to missing {relative_path}"
        )


def validate_icon(plugin_dir: Path, manifest: dict) -> Path:
    icon = manifest.get("icon")
    if not isinstance(icon, str) or not icon.startswith("./assets/"):
        raise ValueError(
            f"{plugin_dir}: icon must be a relative path under ./assets/"
        )
    icon_path = plugin_dir / icon.removeprefix("./")
    if not icon_path.is_file():
        raise ValueError(f"{plugin_dir}: icon points to missing {icon}")
    if icon_path.suffix.lower() not in {".png", ".svg", ".jpg", ".jpeg", ".webp"}:
        raise ValueError(f"{plugin_dir}: unsupported icon type {icon_path.suffix}")
    return icon_path


def validate_skills(skills_dir: Path) -> None:
    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    if not skill_dirs:
        raise ValueError(f"{skills_dir}: skills directory is empty")
    for skill_dir in skill_dirs:
        if not (skill_dir / "SKILL.md").exists():
            raise ValueError(f"{skill_dir}: missing SKILL.md")


def write_plugin_zip(plugin_dir: Path, zip_path: Path) -> None:
    root_name = plugin_dir.name
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(path for path in plugin_dir.rglob("*") if path.is_file()):
            info = zipfile.ZipInfo(f"{root_name}/{file_path.relative_to(plugin_dir)}")
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.external_attr = ((file_path.stat().st_mode & 0o777) or 0o644) << 16
            archive.writestr(info, file_path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)


if __name__ == "__main__":
    raise SystemExit(main())
