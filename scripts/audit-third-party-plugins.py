#!/usr/bin/env python3
"""Build the auditable inventory for third-party Codex plugins."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path


EXPECTED_OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
OPENAI_REPOSITORY = "https://github.com/openai/plugins"
REVIEWS_PATH = Path("third-party-plugin-reviews.json")
JSON_REPORT_PATH = Path("third-party-plugin-audit.json")
MARKDOWN_REPORT_PATH = Path("THIRD_PARTY_PLUGIN_AUDIT.md")
GHAST_PLUGIN_DIR = Path("plugins")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Checkout of github.com/openai/plugins.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    source_revision = git_revision(source)
    if source_revision != EXPECTED_OPENAI_REVISION:
        raise ValueError(
            f"{source}: expected revision {EXPECTED_OPENAI_REVISION}, "
            f"found {source_revision}"
        )

    marketplace = json.loads(
        (source / ".agents/plugins/marketplace.json").read_text()
    )
    reviews = load_reviews()
    ghast_plugins = load_ghast_plugins()

    third_party = []
    excluded_openai = []
    for entry in marketplace["plugins"]:
        plugin_dir = source / entry["source"]["path"]
        manifest = json.loads(
            (plugin_dir / ".codex-plugin/plugin.json").read_text()
        )
        name = manifest["name"]
        if name != entry["name"]:
            raise ValueError(f"{plugin_dir}: marketplace and manifest names differ")

        if is_openai_authored(manifest):
            excluded_openai.append(name)
            continue

        review = reviews.get(name)
        record = build_record(
            name=name,
            plugin_dir=plugin_dir,
            manifest=manifest,
            ghast_manifest=ghast_plugins.get(name),
            review=review,
        )
        third_party.append(record)

    unknown_reviews = sorted(set(reviews) - {item["id"] for item in third_party})
    if unknown_reviews:
        raise ValueError(f"Reviews reference unknown third-party plugins: {unknown_reviews}")

    status_counts = Counter(item["auditStatus"] for item in third_party)
    implementation_counts = Counter(
        item["ghast"]["implementationStatus"] for item in third_party
    )
    report = {
        "schemaVersion": 1,
        "source": OPENAI_REPOSITORY,
        "sourceRevision": source_revision,
        "selectionRule": (
            "Include plugins whose Codex manifest author and interface developer "
            "are not OpenAI. Official origin, license, and capability equivalence "
            "must be independently verified before a port is marked complete."
        ),
        "acceptanceCriteria": [
            "The source is controlled by the named plugin developer or is linked from its official documentation.",
            "Redistribution and modification are allowed by an identified license.",
            "The Ghast plugin uses an official API, MCP server, CLI, SDK, or developer-maintained skill source.",
            "Codex capabilities and Ghast capabilities are compared explicitly.",
            "Authentication, write actions, and high-risk operations have enforceable safety rules.",
            "The packaged plugin installs and its supported core workflows pass recorded verification.",
        ],
        "summary": {
            "codexPlugins": len(marketplace["plugins"]),
            "excludedOpenAIAuthored": len(excluded_openai),
            "thirdPartyPlugins": len(third_party),
            "auditStatus": dict(sorted(status_counts.items())),
            "ghastImplementationStatus": dict(sorted(implementation_counts.items())),
        },
        "excludedOpenAIPlugins": sorted(excluded_openai),
        "plugins": sorted(third_party, key=lambda item: item["id"]),
    }
    JSON_REPORT_PATH.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    )
    MARKDOWN_REPORT_PATH.write_text(render_markdown(report))
    print(
        f"wrote {JSON_REPORT_PATH} and {MARKDOWN_REPORT_PATH} for "
        f"{len(third_party)} third-party plugins"
    )
    return 0


def build_record(
    *,
    name: str,
    plugin_dir: Path,
    manifest: dict,
    ghast_manifest: dict | None,
    review: dict | None,
) -> dict:
    interface = manifest.get("interface") or {}
    declared_repository = manifest.get("repository")
    external_repository = (
        declared_repository
        if declared_repository and not is_openai_repository(declared_repository)
        else None
    )
    license_name = manifest.get("license")
    blocked_license = license_name in {None, "UNLICENSED", "Proprietary"}

    if review:
        validate_review(name, review)
        audit_status = review["verificationStatus"]
    elif blocked_license:
        audit_status = "blocked-license"
    elif external_repository:
        audit_status = "declared-upstream-needs-verification"
    else:
        audit_status = "official-source-research-required"

    review_matches_ghast = (
        review
        and ghast_manifest
        and review["officialRepository"] == ghast_manifest.get("repository")
        and review["officialRevision"] == ghast_manifest.get("upstreamRevision")
        and review["license"] == ghast_manifest.get("license")
    )
    if review and ghast_manifest and not review_matches_ghast:
        raise ValueError(
            f"{name}: review source, revision, or license does not match "
            "the Ghast manifest"
        )

    if ghast_manifest:
        implementation_status = (
            "implemented-verified"
            if review_matches_ghast
            and review["verificationStatus"] == "official-source-verified"
            else "implemented-needs-revalidation"
        )
        ghast = {
            "implementationStatus": implementation_status,
            "version": ghast_manifest.get("version"),
            "repository": ghast_manifest.get("repository"),
            "upstreamRevision": ghast_manifest.get("upstreamRevision"),
            "portStatus": ghast_manifest.get("portStatus", "full"),
        }
    else:
        ghast = {"implementationStatus": "not-implemented"}

    source = {
        "status": (
            "reviewed"
            if review
            else "manifest-declared-candidate"
            if external_repository
            else "unknown"
        ),
        "codexRepository": declared_repository,
        "candidateOfficialRepository": external_repository,
        "homepage": manifest.get("homepage") or interface.get("websiteURL"),
    }
    if review:
        source["review"] = review

    return {
        "id": name,
        "auditStatus": audit_status,
        "developer": {
            "manifestAuthor": manifest.get("author"),
            "interfaceDeveloper": interface.get("developerName"),
        },
        "codex": {
            "version": manifest.get("version"),
            "description": manifest.get("description"),
            "capabilities": interface.get("capabilities", []),
            "longDescription": interface.get("longDescription"),
            "defaultPrompts": normalize_prompts(interface.get("defaultPrompt")),
            "transport": {
                "appConnector": (plugin_dir / ".app.json").exists(),
                "mcpServers": (plugin_dir / ".mcp.json").exists(),
                "skills": (plugin_dir / "skills").exists(),
                "commands": (plugin_dir / "commands").exists(),
            },
        },
        "declaredLicense": license_name,
        "officialSource": source,
        "ghast": ghast,
    }


def normalize_prompts(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def validate_review(name: str, review: dict) -> None:
    required = {
        "verificationStatus",
        "officialDeveloper",
        "officialRepository",
        "officialRevision",
        "license",
        "licenseEvidence",
        "officialityEvidence",
        "codexCapabilities",
        "ghastCapabilities",
        "capabilityRelationship",
        "limitations",
        "verification",
    }
    missing = sorted(required - set(review))
    if missing:
        raise ValueError(f"{name}: review is missing fields {missing}")
    supported_statuses = {
        "blocked-license",
        "official-source-research-required",
        "official-source-verified",
    }
    if review["verificationStatus"] not in supported_statuses:
        raise ValueError(
            f"{name}: unsupported verification status "
            f"{review['verificationStatus']!r}"
        )
    for field in (
        "licenseEvidence",
        "officialityEvidence",
        "codexCapabilities",
        "ghastCapabilities",
        "limitations",
        "verification",
    ):
        value = review[field]
        if not isinstance(value, list) or not value:
            raise ValueError(f"{name}: review field {field!r} must be non-empty")


def is_openai_authored(manifest: dict) -> bool:
    author = manifest.get("author") or {}
    author_name = author.get("name", "") if isinstance(author, dict) else str(author)
    developer_name = (manifest.get("interface") or {}).get("developerName", "")
    return "openai" in author_name.lower() or "openai" in developer_name.lower()


def is_openai_repository(repository: str) -> bool:
    normalized = repository.rstrip("/")
    return normalized == OPENAI_REPOSITORY or normalized.startswith(
        f"{OPENAI_REPOSITORY}/tree/"
    )


def load_reviews() -> dict[str, dict]:
    if not REVIEWS_PATH.exists():
        return {}
    data = json.loads(REVIEWS_PATH.read_text())
    return data["plugins"]


def load_ghast_plugins() -> dict[str, dict]:
    result = {}
    for plugin_dir in sorted(GHAST_PLUGIN_DIR.iterdir()):
        manifest_path = plugin_dir / ".ghast-plugin/plugin.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text())
            result[manifest["name"]] = manifest
    return result


def git_revision(repository: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    lines = [
        "# Third-party Codex plugin audit",
        "",
        f"Source: `{report['source']}` at `{report['sourceRevision']}`.",
        "",
        "## Scope",
        "",
        f"- Codex marketplace plugins: {summary['codexPlugins']}",
        f"- OpenAI-authored plugins excluded: {summary['excludedOpenAIAuthored']}",
        f"- Third-party developer plugins in scope: {summary['thirdPartyPlugins']}",
        "",
        "A plugin is not considered complete merely because its Codex manifest is",
        "present or says MIT. Completion requires an independently verified official",
        "source, usable license, explicit capability comparison, and runnable Ghast",
        "verification.",
        "",
        "## Acceptance criteria",
        "",
    ]
    lines.extend(f"- {criterion}" for criterion in report["acceptanceCriteria"])
    lines.extend(
        [
            "",
            "## Inventory",
            "",
            "| Plugin | Developer | Codex transport | Declared license | Audit | Ghast |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for plugin in report["plugins"]:
        developer = (
            plugin["developer"].get("interfaceDeveloper")
            or (plugin["developer"].get("manifestAuthor") or {}).get("name")
            or "Unknown"
        )
        enabled_transports = [
            name
            for name, enabled in plugin["codex"]["transport"].items()
            if enabled
        ]
        lines.append(
            "| {id} | {developer} | {transport} | {license} | {audit} | {ghast} |".format(
                id=plugin["id"],
                developer=str(developer).replace("|", "\\|"),
                transport=", ".join(enabled_transports) or "metadata-only",
                license=plugin["declaredLicense"] or "none",
                audit=plugin["auditStatus"],
                ghast=plugin["ghast"]["implementationStatus"],
            )
        )
    lines.extend(
        [
            "",
            "The JSON report is the machine-readable source of truth. Human review",
            "evidence lives in `third-party-plugin-reviews.json` and must be updated",
            "before changing an item to `official-source-verified`.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
