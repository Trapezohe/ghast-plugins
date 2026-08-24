#!/usr/bin/env python3
"""Verify Binance CLI discovery and one official public Spot data workflow."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess


PUBLIC_TICKER_URL = (
    "https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cli",
        default=shutil.which("binance-cli") or os.path.expanduser("~/.cargo/bin/binance-cli"),
        help="Path to the official binance-cli binary.",
    )
    return parser.parse_args()


def run(*args: str) -> str:
    return subprocess.run(
        args,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> int:
    args = parse_args()
    version = run(args.cli, "--version")
    match = re.fullmatch(r"binance-cli (\d+)\.(\d+)\.(\d+)", version)
    if match is None or int(match.group(1)) < 2:
        raise ValueError(f"unsupported Binance CLI version: {version!r}")

    help_text = run(args.cli, "--help")
    required_commands = ("spot", "futures-usds", "convert", "request", "profile")
    missing = [command for command in required_commands if command not in help_text]
    if missing:
        raise ValueError(f"Binance CLI is missing commands: {missing}")

    response = run(
        "curl",
        "--proto",
        "=https",
        "--tlsv1.2",
        "--fail-with-body",
        "--silent",
        "--show-error",
        PUBLIC_TICKER_URL,
    )
    ticker = json.loads(response)
    if ticker.get("symbol") != "BTCUSDT":
        raise ValueError(f"unexpected ticker symbol: {ticker!r}")
    try:
        if float(ticker["price"]) <= 0:
            raise ValueError(f"non-positive ticker price: {ticker!r}")
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"invalid ticker response: {ticker!r}") from exc

    print(f"verified {version}; official public ticker returned BTCUSDT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
