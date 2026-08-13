#!/usr/bin/env python3
"""Generate a unique local Ed25519 key for a DigitalOcean workspace."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import secrets
import shutil
import subprocess
from pathlib import Path


NAME_RE = re.compile(r"[a-z][a-z0-9-]{1,31}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", default="ghast-do")
    parser.add_argument(
        "--directory",
        type=Path,
        default=Path.home() / ".ssh",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not NAME_RE.fullmatch(args.prefix):
        raise SystemExit(
            "--prefix must be 2-32 lowercase letters, digits, or hyphens"
        )
    ssh_keygen = shutil.which("ssh-keygen")
    if not ssh_keygen:
        raise SystemExit("ssh-keygen is required")

    directory = args.directory.expanduser().resolve()
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    directory.chmod(0o700)

    token = secrets.token_hex(3)
    name = f"{args.prefix}-{token}"
    key_name = f"{name}-key"
    private_key = directory / name
    public_key = private_key.with_suffix(".pub")
    if private_key.exists() or public_key.exists():
        raise SystemExit("generated key path already exists; run again")

    try:
        subprocess.run(
            [
                ssh_keygen,
                "-q",
                "-t",
                "ed25519",
                "-N",
                "",
                "-C",
                key_name,
                "-f",
                str(private_key),
            ],
            check=True,
        )
        private_key.chmod(0o600)
        public_key.chmod(0o644)
        public_text = public_key.read_text().strip()
        public_blob = base64.b64decode(
            public_text.split()[1],
            validate=True,
        )
        fingerprint = hashlib.sha256(public_blob).hexdigest()
        md5_hex = hashlib.md5(
            public_blob,
            usedforsecurity=False,
        ).hexdigest()
        digitalocean_fingerprint = ":".join(
            md5_hex[index : index + 2]
            for index in range(0, len(md5_hex), 2)
        )
    except Exception:
        private_key.unlink(missing_ok=True)
        public_key.unlink(missing_ok=True)
        raise

    print(
        json.dumps(
            {
                "name": name,
                "key_name": key_name,
                "key_path": str(private_key),
                "public_key": public_text,
                "public_key_sha256": fingerprint,
                "digitalocean_fingerprint": digitalocean_fingerprint,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
