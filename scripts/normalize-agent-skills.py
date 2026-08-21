#!/usr/bin/env python3
"""Normalize plugin skills to the Agent Skills frontmatter specification."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - dependency guidance for operators
    raise SystemExit(
        "PyYAML is required: python3 -m pip install 'PyYAML>=6,<7'"
    ) from exc

try:
    from skills_ref import validate as validate_agent_skill
except ImportError as exc:  # pragma: no cover - dependency guidance for operators
    raise SystemExit(
        "skills-ref is required: python3 -m pip install -r requirements-agent-plugins.txt"
    ) from exc


ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugins", type=Path, default=Path("plugins"))
    args = parser.parse_args()

    normalized = 0
    renamed = 0
    for skill_path in sorted(args.plugins.glob("*/skills/*/SKILL.md")):
        changed, directory_renamed = normalize_skill(skill_path)
        normalized += changed
        renamed += directory_renamed

    print(f"normalized {normalized} Agent Skills ({renamed} directories renamed)")
    return 0


def normalize_skill(skill_path: Path) -> tuple[bool, bool]:
    if not validate_agent_skill(skill_path.parent):
        return False, False

    text = skill_path.read_text()
    frontmatter, body = split_frontmatter(skill_path, text)
    metadata = load_frontmatter(skill_path, frontmatter)
    if not isinstance(metadata, dict):
        raise ValueError(f"{skill_path}: frontmatter must be a mapping")

    skill_dir = skill_path.parent
    target_name = normalize_name(skill_dir.name)
    renamed = False
    if target_name != skill_dir.name:
        target_dir = skill_dir.with_name(target_name)
        if target_dir.exists():
            raise ValueError(f"{target_dir}: normalized skill directory already exists")
        skill_dir.rename(target_dir)
        skill_dir = target_dir
        skill_path = skill_dir / "SKILL.md"
        renamed = True

    normalized = normalize_metadata(skill_path, metadata, target_name)
    if (
        not renamed
        and normalized == metadata
        and frontmatter_is_block_style(frontmatter)
        and has_canonical_delimiters(text)
    ):
        return False, False

    rendered = yaml.safe_dump(
        normalized,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=1000,
    ).rstrip()
    candidate = f"---\n{rendered}\n---\n{body.lstrip(chr(10) + chr(13))}"
    if not renamed and candidate == text:
        return False, False
    skill_path.write_text(candidate)
    return True, renamed


def normalize_metadata(path: Path, source: dict, target_name: str) -> dict:
    description = source.get("description")
    if description is None:
        raise ValueError(f"{path}: missing description")
    description = str(description).strip()
    if not description:
        raise ValueError(f"{path}: description must not be empty")

    result = {
        "name": target_name,
        "description": truncate(description, 1024),
    }
    for field in ("license", "compatibility"):
        if field in source and source[field] is not None:
            limit = 500 if field == "compatibility" else None
            value = str(source[field])
            result[field] = truncate(value, limit) if limit else value

    legacy = {}
    existing_metadata = source.get("metadata")
    if existing_metadata is not None:
        if not isinstance(existing_metadata, dict):
            legacy["metadata"] = stringify(existing_metadata)
        else:
            legacy.update({str(key): stringify(value) for key, value in existing_metadata.items()})

    for key, value in source.items():
        if key not in ALLOWED_FIELDS:
            metadata_key = str(key)
            if metadata_key in legacy:
                metadata_key = f"legacy-{metadata_key}"
            legacy[metadata_key] = stringify(value)
    if legacy:
        result["metadata"] = legacy

    allowed_tools = source.get("allowed-tools")
    if allowed_tools is not None:
        if isinstance(allowed_tools, list):
            allowed_tools = " ".join(str(value) for value in allowed_tools)
        else:
            allowed_tools = str(allowed_tools)
        if allowed_tools.strip():
            result["allowed-tools"] = allowed_tools.strip()
    return result


def split_frontmatter(path: Path, text: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: missing opening frontmatter delimiter")
    for index, line in enumerate(lines[1:], start=1):
        if line.startswith("---"):
            inline_body = line[3:]
            return "".join(lines[1:index]), inline_body + "".join(lines[index + 1 :])
    raise ValueError(f"{path}: missing closing frontmatter delimiter")


def load_frontmatter(path: Path, frontmatter: str) -> object:
    try:
        return yaml.safe_load(frontmatter)
    except yaml.YAMLError as original_error:
        # A few imported skills have an unquoted, single-line description with
        # a colon. Quote only that scalar and let the parser validate the rest.
        lines = frontmatter.splitlines(keepends=True)
        repaired = False
        for index, line in enumerate(lines):
            match = re.match(r"^(description:\s*)(.*?)(\r?\n)?$", line)
            if match and match.group(2) and not match.group(2).startswith(("'", '"', "|", ">")):
                newline = match.group(3) or ""
                lines[index] = f"{match.group(1)}{json.dumps(match.group(2), ensure_ascii=False)}{newline}"
                repaired = True
                break
        if repaired:
            try:
                return yaml.safe_load("".join(lines))
            except yaml.YAMLError:
                pass
        raise ValueError(f"{path}: invalid YAML frontmatter: {original_error}") from original_error


def has_canonical_delimiters(text: str) -> bool:
    lines = text.splitlines(keepends=True)
    return len(lines) >= 2 and any(line.strip() == "---" for line in lines[1:])


def normalize_name(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    normalized = re.sub(r"-+", "-", normalized)[:64].rstrip("-")
    if not NAME_PATTERN.fullmatch(normalized):
        raise ValueError(f"cannot normalize skill directory name {value!r}")
    return normalized


def truncate(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def stringify(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(
        value,
        default=str,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def frontmatter_is_block_style(frontmatter: str) -> bool:
    """Return false for flow collections rejected by the reference parser."""
    return not any(re.match(r"^\s*[^#\n]+:\s*[\[{]", line) for line in frontmatter.splitlines())


if __name__ == "__main__":
    raise SystemExit(main())
