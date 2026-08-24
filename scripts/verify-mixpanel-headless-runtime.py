#!/usr/bin/env python3
"""Run the pinned Mixpanel Headless non-live test suite in a locked environment."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


EXPECTED_REVISION = "6c2c2f975d51628bdbc75802fb879d4f6cb66f69"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--python", default=sys.executable)
    return parser.parse_args()


def run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, **kwargs)


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if revision != EXPECTED_REVISION:
        raise ValueError(f"expected {EXPECTED_REVISION}, found {revision}")

    with tempfile.TemporaryDirectory(prefix="ghast-mixpanel-runtime-") as temp:
        root = Path(temp)
        bootstrap = root / "bootstrap"
        environment = root / "environment"
        run([args.python, "-m", "venv", str(bootstrap)])
        run(
            [
                str(bootstrap / "bin/python"),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--quiet",
                "uv",
            ]
        )
        sync_environment = os.environ.copy()
        sync_environment["UV_PROJECT_ENVIRONMENT"] = str(environment)
        run(
            [
                str(bootstrap / "bin/uv"),
                "sync",
                "--frozen",
                "--extra",
                "dev",
                "--python",
                args.python,
            ],
            cwd=source,
            env=sync_environment,
        )

        test_environment = os.environ.copy()
        test_environment["PATH"] = os.pathsep.join(
            [str(bootstrap / "bin"), str(environment / "bin"), test_environment["PATH"]]
        )
        test_environment["NO_PROXY"] = "localhost,127.0.0.1,::1"
        test_environment["no_proxy"] = test_environment["NO_PROXY"]

        session = subprocess.run(
            [str(environment / "bin/mp"), "session", "--format", "json"],
            check=True,
            capture_output=True,
            text=True,
            env=test_environment,
        )
        session_data = json.loads(session.stdout)
        if set(session_data) != {
            "account",
            "project",
            "workspace",
            "user",
            "me_cached",
        }:
            raise ValueError(f"unexpected mp session output: {session_data!r}")

        run(
            [
                str(environment / "bin/pytest"),
                "-q",
                "-o",
                "addopts=",
                "-m",
                "not live",
            ],
            cwd=source,
            env=test_environment,
        )

    print("verified Mixpanel Headless locked non-live suite and mp session")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
