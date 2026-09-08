#!/usr/bin/env python3
"""Verify NVIDIA's official catalog, signatures, and packaged source fidelity."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
from pathlib import Path

import official_plugin_verification as verify

REVISION = "7149a886d50da8db72cdc1f20ff01cefeadfe6a9"
REPOSITORY = "https://github.com/NVIDIA/skills"
SHELL_EXCEPTION = (
    "vss-deploy-detection-tracking-2d/scripts/write_deployment_log.sh",
    "c62d8335d30708e7a6d5f23b8bc66f8e693bb1d71bb16ba2fa6239b92f87e765",
)
CONTENT_MISMATCHES = {
    "amc-run-sample-calibration/SKILL.md",
    "amc-run-video-calibration/SKILL.md",
    "amc-setup-calibration-stack/SKILL.md",
    "deepstream-dev/references/kafka_messaging.md",
    "deepstream-dev/references/nvinfer_config.md",
    "deepstream-dev/references/service_maker_api.md",
    "earth2studio-create-datasource/SKILL.md",
    "earth2studio-create-datasource/references/testing-guide.py",
    "earth2studio-create-datasource/references/validation-guide.md",
    "earth2studio-create-diagnostic/SKILL.md",
    "earth2studio-create-prognostic/SKILL.md",
    "earth2studio-create-prognostic/references/method-templates.py",
    "earth2studio-create-prognostic/references/skeleton-template.py",
    "earth2studio-create-prognostic/references/testing-guide.py",
    "earth2studio-create-prognostic/references/validation-guide.md",
}
OMS_FAILURES = {
    "amc-run-rtsp-calibration", "amc-run-sample-calibration",
    "amc-run-video-calibration", "amc-setup-calibration-stack",
    "deepstream-dev", "deepstream-run-mv3dt", "deepstream-sop",
    "earth2studio-create-datasource", "earth2studio-create-diagnostic",
    "earth2studio-create-prognostic",
}


def signed_resources(signature: Path) -> list[dict]:
    bundle = json.loads(signature.read_text())
    payload = base64.b64decode(bundle["dsseEnvelope"]["payload"])
    return json.loads(payload)["predicate"]["resources"]


def content_mismatches(skills: Path) -> set[str]:
    mismatches: set[str] = set()
    for skill in sorted(d for d in skills.iterdir() if (d / "SKILL.md").is_file()):
        for resource in signed_resources(skill / "skill.oms.sig"):
            target = skill / resource["name"]
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != resource["digest"]:
                mismatches.add(f"{skill.name}/{resource['name']}")
    return mismatches


def verify_oms(model_signing: Path, skills: Path, certificate: Path) -> tuple[int, set[str]]:
    passed, failed = 0, set()
    for skill in sorted(d for d in skills.iterdir() if (d / "SKILL.md").is_file()):
        result = subprocess.run([
            str(model_signing), "verify", "certificate", str(skill),
            "--signature", str(skill / "skill.oms.sig"),
            "--certificate_chain", str(certificate), "--ignore_unsigned_files",
        ], text=True, capture_output=True)
        if result.returncode == 0 and "Verification succeeded" in result.stdout:
            passed += 1
        else:
            failed.add(skill.name)
    return passed, failed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--model-signing", type=Path, required=True)
    parser.add_argument(
        "--plugin", type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/nvidia",
    )
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(
        source
    ) != imp.normalized_repository_url(REPOSITORY):
        raise ValueError("NVIDIA official source identity changed")
    verify.manifest(
        plugin, name="nvidia", version='1.4.0', revision=REVISION
    )
    source_skills = source / "skills"
    packaged_skills = plugin / "skills"
    signed_skills = plugin / "upstream-signed/skills"
    source_dirs = sorted(d for d in source_skills.iterdir() if (d / "SKILL.md").is_file())
    packaged_dirs = sorted(d for d in packaged_skills.iterdir() if (d / "SKILL.md").is_file())
    if [d.name for d in source_dirs] != [d.name for d in packaged_dirs] or len(source_dirs) != 343:
        raise ValueError("NVIDIA skill inventory changed")
    signed_files = verify.compare_trees(
        source_skills, signed_skills, ignore_skill_frontmatter=False
    )
    if signed_files != 4406:
        raise ValueError(f"NVIDIA signed-source archive changed: {signed_files}")
    files = 0
    for source_skill, packaged_skill in zip(source_dirs, packaged_dirs, strict=True):
        expected = {
            name: path for name, path in verify.file_map(source_skill).items()
            if name != "skill.oms.sig" and not name.endswith("/openai.yaml")
        }
        actual = verify.file_map(packaged_skill)
        if expected.keys() != actual.keys():
            raise ValueError(f"{packaged_skill}: normalized file inventory differs")
        for name, source_path in expected.items():
            source_data, packaged_data = source_path.read_bytes(), actual[name].read_bytes()
            if name == "SKILL.md":
                source_data = verify.skill_body(source_data)
                packaged_data = verify.skill_body(packaged_data)
            if source_data != packaged_data:
                raise ValueError(f"{packaged_skill}: official content differs at {name}")
        files += len(actual)
    if files != 4054:
        raise ValueError(f"NVIDIA runnable file count changed: {files}")
    if list(packaged_skills.rglob("skill.oms.sig")):
        raise ValueError("NVIDIA normalized runnable tree must not claim signed identity")
    for name in ("skill.oms.sig", "skill-card.md", "BENCHMARK.md"):
        if len(list(signed_skills.glob(f"*/{name}"))) != 343:
            raise ValueError(f"NVIDIA {name} inventory changed")
    eval_count = sum(
        bool(list(skill.glob("evals/*.json")) or list(skill.glob("eval/*.json"))
             or list(skill.glob("benchmark/evals.json")))
        for skill in sorted(d for d in signed_skills.iterdir() if (d / "SKILL.md").is_file())
    )
    if eval_count != 343:
        raise ValueError(f"NVIDIA evaluation inventory changed: {eval_count}")
    for source_name, packaged_name in (
        ("LICENSE-APACHE", "LICENSE"),
        ("LICENSE-CC-BY-4.0", "LICENSE-CC-BY-4.0"),
        ("nv-agent-root-cert.pem", "nv-agent-root-cert.pem"),
    ):
        if (source / source_name).read_bytes() != (plugin / packaged_name).read_bytes():
            raise ValueError(f"NVIDIA packaged {packaged_name} changed")

    if content_mismatches(signed_skills) != CONTENT_MISMATCHES:
        raise ValueError("NVIDIA signed-content drift set changed; re-audit required")
    passed, failed = verify_oms(
        args.model_signing.resolve(), signed_skills,
        plugin / "nv-agent-root-cert.pem",
    )
    if passed != 333 or failed != OMS_FAILURES:
        raise ValueError(
            f"NVIDIA OMS verification changed: passed={passed}, failed={sorted(failed)}"
        )
    shells = sorted(packaged_skills.rglob("*.sh"))
    shell_failures = []
    for shell in shells:
        result = subprocess.run(["bash", "-n", str(shell)], capture_output=True)
        if result.returncode:
            shell_failures.append(shell)
    exception_path = packaged_skills / SHELL_EXCEPTION[0]
    if shells.__len__() != 123 or shell_failures != [exception_path]:
        raise ValueError("NVIDIA shell syntax inventory changed")
    if hashlib.sha256(exception_path.read_bytes()).hexdigest() != SHELL_EXCEPTION[1]:
        raise ValueError("NVIDIA documented signed shell exception changed")
    print(
        "verified NVIDIA 1.4.0 official 343-skill/4406-file signed-source "
        "archive, 343 portable runnable skills across 4054 files, 343 cards, "
        "signatures, benchmarks and eval sets, 333 successful OMS certificate "
        "verifications, exact 10-skill/15-file upstream signature-drift set, "
        "123 shell scripts with one pinned Bash 3.2 exception, Agent Plugins "
        "1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
