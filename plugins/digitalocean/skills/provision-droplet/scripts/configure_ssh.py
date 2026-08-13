#!/usr/bin/env python3
"""Add or update one marked DigitalOcean host in an OpenSSH config."""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import tempfile
from pathlib import Path


ALIAS_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")
USER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_-]{0,31}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--alias", required=True)
    parser.add_argument("--ip", required=True)
    parser.add_argument("--user", default="root")
    parser.add_argument("--key-path", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path.home() / ".ssh" / "config",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not ALIAS_RE.fullmatch(args.alias):
        raise SystemExit("invalid SSH alias")
    if not USER_RE.fullmatch(args.user):
        raise SystemExit("invalid SSH user")
    try:
        address = ipaddress.ip_address(args.ip)
    except ValueError as exc:
        raise SystemExit("--ip must be a public IPv4 address") from exc
    if address.version != 4 or not address.is_global:
        raise SystemExit("--ip must be a public IPv4 address")

    unresolved_key_path = args.key_path.expanduser()
    if unresolved_key_path.is_symlink():
        raise SystemExit("--key-path must not be a symlink")
    key_path = unresolved_key_path.resolve(strict=True)
    if not key_path.is_file():
        raise SystemExit("--key-path must be a regular, non-symlink file")
    if any(character in str(key_path) for character in ('"', "\r", "\n")):
        raise SystemExit("--key-path contains unsupported characters")
    key_path.chmod(0o600)

    config = args.config.expanduser().resolve()
    config.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    config.parent.chmod(0o700)
    original = config.read_text() if config.exists() else ""

    begin = f"# ghast-digitalocean:{args.alias}:begin"
    end = f"# ghast-digitalocean:{args.alias}:end"
    pattern = re.compile(
        rf"(?ms)^{re.escape(begin)}\n.*?^{re.escape(end)}\n?"
    )
    remaining = pattern.sub("", original)
    host_pattern = re.compile(
        rf"(?im)^\s*Host\s+{re.escape(args.alias)}(?:\s|$)"
    )
    if host_pattern.search(remaining):
        raise SystemExit(
            "SSH alias already exists outside Ghast's managed block"
        )

    block = "\n".join(
        [
            begin,
            f"Host {args.alias}",
            f"  HostName {address}",
            f"  User {args.user}",
            f'  IdentityFile "{key_path}"',
            "  IdentitiesOnly yes",
            "  StrictHostKeyChecking accept-new",
            "  ServerAliveInterval 30",
            end,
            "",
        ]
    )
    updated = remaining.rstrip()
    if updated:
        updated += "\n\n"
    updated += block

    fd, temporary_name = tempfile.mkstemp(
        prefix=".ghast-ssh-config-",
        dir=config.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w") as handle:
            handle.write(updated)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.chmod(0o600)
        os.replace(temporary, config)
        config.chmod(0o600)
    finally:
        temporary.unlink(missing_ok=True)

    print(
        json.dumps(
            {
                "alias": args.alias,
                "config": str(config),
                "host": str(address),
                "identity_file": str(key_path),
                "user": args.user,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
