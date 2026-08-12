#!/usr/bin/env python3
"""Build Ghast's downloadable plugin catalog from local plugin sources."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


CATALOG_PATH = Path("plugin-catalog.json")
MARKETPLACE_PATH = Path(".claude-plugin/marketplace.json")
PACKAGE_DIR = Path("packages")


def main() -> int:
    marketplace = json.loads(MARKETPLACE_PATH.read_text())
    PACKAGE_DIR.mkdir(exist_ok=True)

    plugins = []
    for entry in marketplace["plugins"]:
        source = entry.get("source")
        if not isinstance(source, str) or not source.startswith("./plugins/"):
            continue
        plugin_dir = Path(source)
        if not plugin_dir.exists():
            continue

        manifest = json.loads((plugin_dir / ".claude-plugin/plugin.json").read_text())
        manifest_for_catalog = {
            "name": manifest["name"],
            "description": manifest["description"],
            "author": manifest.get("author", entry.get("author", "")),
        }
        if (plugin_dir / "skills").exists():
            manifest_for_catalog["skills"] = "./skills/"
        if (plugin_dir / "commands").exists():
            manifest_for_catalog["commands"] = "./commands/"
        if (plugin_dir / ".mcp.json").exists():
            manifest_for_catalog["mcpServers"] = "./.mcp.json"
        if (plugin_dir / "hooks").exists():
            manifest_for_catalog["hooks"] = "./hooks/"

        zip_path = PACKAGE_DIR / f"{manifest['name']}.zip"
        write_plugin_zip(plugin_dir, zip_path)
        sha256 = hashlib.sha256(zip_path.read_bytes()).hexdigest()

        plugins.append(
            {
                "id": manifest["name"],
                "name": manifest["name"],
                "description": entry.get("description") or manifest["description"],
                "category": entry.get("category"),
                "homepage": entry.get("homepage"),
                "manifest": manifest_for_catalog,
                "package": {
                    "url": f"./packages/{zip_path.name}",
                    "sha256": sha256,
                },
            }
        )

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
