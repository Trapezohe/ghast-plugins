#!/usr/bin/env python3
"""Verify Boltz's official plugin release, local tests, CLI, and Ghast hardening."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import types
import urllib.request
import zipfile
from pathlib import Path
from types import ModuleType


EXPECTED_REVISION = "70e480ebb14baecfc4456b49eb8b724611470b7c"
RELEASE_VERSION = "0.1.1"
RELEASE_SOURCE_REVISION = "59c4c2868b8ebbd1eca1f4b94bb99bf96220d15e"
RELEASE_API = (
    "https://api.github.com/repos/boltz-bio/boltz-api-skills/releases/tags/"
    "codex-plugin%2Fv0.1.1"
)
RELEASE_ARCHIVE_SHA256 = "7ec459d0737f399ba1b2c8f6d966abe1060b80834f8c7c22ce959a0780f850c3"
RELEASE_CHECKSUM_SHA256 = "1049bff5ab40fbbe51dcbc4523a7ff37d0d7885571f04d56fe58afc702f9305a"
CLI_VERSION = "0.41.0"
CLI_RELEASE_METADATA = (
    f"https://install.boltz.bio/boltz-api/releases/v{CLI_VERSION}/release.json"
)
CLI_ARCHIVE_NAME = f"boltz-api_{CLI_VERSION}_macos_arm64.zip"
CLI_ARCHIVE_SHA256 = "2d640f6ec055108494e6d4c9c6e93819043c2d0043ba92ea16c10c89ea0eac81"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/boltz-api-cli"
    )
    parser.add_argument("--python", default=sys.executable)
    return parser.parse_args()


def fetch(url: str, *, github: bool = False) -> bytes:
    headers = {"User-Agent": "ghast-audit/1.0"}
    if github:
        headers["Accept"] = "application/vnd.github+json"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def run(arguments: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(arguments, check=True, text=True, **kwargs)


def load_importer() -> ModuleType:
    spec = importlib.util.spec_from_file_location("ghast_official_importer", IMPORTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {IMPORTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def zip_files(archive: bytes, prefix: str) -> dict[str, bytes]:
    with tempfile.SpooledTemporaryFile() as stream:
        stream.write(archive)
        stream.seek(0)
        with zipfile.ZipFile(stream) as package:
            result = {}
            for item in package.infolist():
                if item.is_dir() or not item.filename.startswith(prefix):
                    continue
                relative = item.filename.removeprefix(prefix)
                if relative.endswith("/agents/openai.yaml"):
                    continue
                result[relative] = package.read(item)
            return result


def directory_files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    }


def verify_release(source: Path, plugin: Path) -> None:
    release = json.loads(fetch(RELEASE_API, github=True))
    if release.get("tag_name") != f"codex-plugin/v{RELEASE_VERSION}":
        raise ValueError("unexpected Boltz plugin release tag")
    if release.get("target_commitish") != RELEASE_SOURCE_REVISION:
        raise ValueError("Boltz release source revision changed")
    assets = {asset["name"]: asset for asset in release.get("assets", [])}
    archive_name = f"boltz-api-cli-{RELEASE_VERSION}.zip"
    checksum_name = f"{archive_name}.sha256"
    archive_asset = assets.get(archive_name)
    checksum_asset = assets.get(checksum_name)
    if archive_asset is None or archive_asset.get("digest") != f"sha256:{RELEASE_ARCHIVE_SHA256}":
        raise ValueError("Boltz release archive digest changed")
    if checksum_asset is None or checksum_asset.get("digest") != f"sha256:{RELEASE_CHECKSUM_SHA256}":
        raise ValueError("Boltz release checksum-file digest changed")
    archive = fetch(archive_asset["browser_download_url"])
    checksum = fetch(checksum_asset["browser_download_url"])
    if hashlib.sha256(archive).hexdigest() != RELEASE_ARCHIVE_SHA256:
        raise ValueError("Boltz plugin archive does not match GitHub's digest")
    if hashlib.sha256(checksum).hexdigest() != RELEASE_CHECKSUM_SHA256:
        raise ValueError("Boltz checksum file does not match GitHub's digest")
    expected_checksum = f"{RELEASE_ARCHIVE_SHA256}  dist/{archive_name}\n".encode()
    if checksum != expected_checksum:
        raise ValueError("Boltz checksum file does not name the release archive")

    official_files = zip_files(archive, "skills/")
    if len(official_files) != 31:
        raise ValueError(f"expected 31 official Boltz skill files, found {len(official_files)}")
    current_official = {
        relative: data
        for relative, data in directory_files(
            source / "plugins/boltz-api-cli/skills"
        ).items()
        if not relative.endswith("/agents/openai.yaml")
    }
    if current_official != official_files:
        raise ValueError("Boltz current official skill tree differs from release 0.1.1")

    with tempfile.TemporaryDirectory(prefix="ghast-boltz-expected-") as temp:
        root = Path(temp)
        skills = root / "skills"
        for relative, data in official_files.items():
            target = skills / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        load_importer().harden_boltz_skills(root)
        if directory_files(skills) != directory_files(plugin / "skills"):
            raise ValueError("Ghast Boltz skills differ from official release plus hardening")


def verify_hardened_scan(plugin: Path) -> None:
    script = plugin / "skills/boltz-protein-design/scripts/scan_sites.py"
    common = types.ModuleType("_common")
    common.atom_coords = None
    common.indexed_residues = None
    dependencies = {
        "_common": common,
        "gemmi": types.ModuleType("gemmi"),
        "numpy": types.ModuleType("numpy"),
    }
    spec = importlib.util.spec_from_file_location("ghast_boltz_scan_sites", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {script}")
    module = importlib.util.module_from_spec(spec)
    original_modules = {name: sys.modules.get(name) for name in dependencies}
    try:
        sys.modules.update(dependencies)
        spec.loader.exec_module(module)
    finally:
        for name, previous in original_modules.items():
            if previous is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = previous

    class Chain:
        def __init__(self, name: str) -> None:
            self.name = name

    if module.cluster_sites([{1, 2}, {3, 4}, {2, 3}], 0.25) != [[0, 1, 2]]:
        raise ValueError("Boltz scan clustering is not transitive")
    if module._binder_chain_names([Chain("A"), Chain("B")], "A") != {"B"}:
        raise ValueError("Boltz scan did not infer one unambiguous binder")
    try:
        module._binder_chain_names([Chain("A"), Chain("B"), Chain("C")], "A")
    except ValueError as error:
        if "ambiguous" not in str(error):
            raise
    else:
        raise ValueError("Boltz scan accepted ambiguous binder chains")
    try:
        module._binder_chain_names([Chain("A"), Chain("B")], "A", ["A"])
    except ValueError:
        pass
    else:
        raise ValueError("Boltz scan accepted the target as a binder")


def verify_official_local_tests(source: Path, python: str) -> None:
    run(["scripts/verify-generated.sh"], cwd=source)
    if run(["git", "status", "--short"], cwd=source, capture_output=True).stdout:
        raise ValueError("Boltz generated-surface verification changed the source checkout")
    with tempfile.TemporaryDirectory(prefix="ghast-boltz-tests-") as temp:
        environment = Path(temp) / "venv"
        run([python, "-m", "venv", str(environment)])
        run(
            [
                str(environment / "bin/python"),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--quiet",
                "-r",
                str(
                    source
                    / "core/skills/cli/boltz-protein-design/scripts/requirements.txt"
                ),
            ]
        )
        result = run(
            [
                str(environment / "bin/python"),
                "-m",
                "unittest",
                "discover",
                "-s",
                str(source / "core/skills/cli/boltz-protein-design/tests"),
                "-v",
            ],
            capture_output=True,
        )
        if "Ran 16 tests" not in result.stderr or not result.stderr.rstrip().endswith("OK"):
            raise ValueError("unexpected Boltz official local test result")


def verify_cli() -> None:
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        raise RuntimeError("the pinned Boltz CLI check requires macOS arm64")
    metadata = json.loads(fetch(CLI_RELEASE_METADATA))
    if metadata.get("tag_name") != f"v{CLI_VERSION}":
        raise ValueError("unexpected Boltz CLI release metadata")
    assets = {asset["name"]: asset for asset in metadata.get("assets", [])}
    asset = assets.get(CLI_ARCHIVE_NAME)
    if asset is None:
        raise ValueError(f"Boltz CLI metadata is missing {CLI_ARCHIVE_NAME}")
    archive = fetch(asset["browser_download_url"])
    if hashlib.sha256(archive).hexdigest() != CLI_ARCHIVE_SHA256:
        raise ValueError("Boltz CLI archive changed from the independently observed hash")

    with tempfile.TemporaryDirectory(prefix="ghast-boltz-cli-") as temp:
        root = Path(temp)
        archive_path = root / CLI_ARCHIVE_NAME
        archive_path.write_bytes(archive)
        with zipfile.ZipFile(archive_path) as package:
            member = next(
                (item for item in package.infolist() if item.filename == "boltz-api"),
                None,
            )
            if member is None:
                raise ValueError("Boltz CLI archive is missing the binary")
            binary = root / "boltz-api"
            binary.write_bytes(package.read(member))
            binary.chmod(0o755)
        environment = os.environ.copy()
        environment.pop("BOLTZ_API_KEY", None)
        environment["HOME"] = str(root / "home")
        Path(environment["HOME"]).mkdir()

        version = run(
            [str(binary), "--version"], capture_output=True, env=environment
        ).stdout.strip()
        if version != f"boltz-api version {CLI_VERSION}":
            raise ValueError(f"Boltz CLI reported {version}")
        root_help = run(
            [str(binary), "--help"], capture_output=True, env=environment
        ).stdout
        resources = {
            "predictions:structure-and-binding": ("estimate-cost", "start", "run"),
            "predictions:adme": ("estimate-cost", "start", "run"),
            "small-molecule:design": ("estimate-cost", "list-results", "start"),
            "small-molecule:library-screen": ("estimate-cost", "list-results", "start"),
            "protein:design": ("estimate-cost", "list-results", "start"),
            "protein:library-screen": ("estimate-cost", "list-results", "start"),
        }
        for resource, markers in resources.items():
            if resource not in root_help:
                raise ValueError(f"Boltz CLI root help is missing {resource}")
            resource_help = run(
                [str(binary), resource, "--help"],
                capture_output=True,
                env=environment,
            ).stdout
            for marker in markers:
                if marker not in resource_help:
                    raise ValueError(f"Boltz {resource} help is missing {marker}")

        auth = subprocess.run(
            [str(binary), "--format", "json", "--format-error", "json", "auth", "status"],
            capture_output=True,
            text=True,
            env=environment,
            timeout=20,
        )
        auth_status = json.loads(auth.stdout)
        if auth.returncode != 1 or auth_status.get("authenticated") is not False:
            raise ValueError(f"unexpected Boltz auth boundary: {auth_status!r}")
        if auth_status.get("effective_mode") != "none" or auth_status.get("api_key_configured") is not False:
            raise ValueError(f"Boltz isolated auth state is not empty: {auth_status!r}")


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    revision = run(
        ["git", "rev-parse", "HEAD"], cwd=source, capture_output=True
    ).stdout.strip()
    if revision != EXPECTED_REVISION:
        raise ValueError(f"expected {EXPECTED_REVISION}, found {revision}")
    manifest = json.loads((plugin / "plugin.json").read_text())
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError("Boltz is not Agent Plugins 1.0")
    if manifest.get("version") != '0.1.1':
        raise ValueError(f"unexpected Ghast Boltz version: {manifest.get('version')}")
    if not (plugin / "assets/icon.png").is_file():
        raise ValueError("Boltz icon is missing")

    verify_release(source, plugin)
    verify_hardened_scan(plugin)
    verify_official_local_tests(source, args.python)
    verify_cli()
    print(
        "verified Boltz official 0.1.1 release digests and 31-file skill tree, "
        "16 local tests, Ghast multi-chain hardening, CLI 0.41.0 workflow "
        "surface and isolated auth boundary, Agent Plugins 1.0 manifest, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
