#!/usr/bin/env python3
"""Verify the official-source Razorpay read-only Ghast adapter."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path


OFFICIAL_REVISION = "7950d51d118ca164c32b7cf0cfaa14f34f24849f"
OFFICIAL_TREE = "feeadae4514cce8fa67651eeae22ba94ffe28dfd"
OFFICIAL_REPOSITORY = "https://github.com/razorpay/razorpay-mcp-server"
OFFICIAL_FILE_COUNT = 94
OFFICIAL_INVENTORY_SHA256 = (
    "6e74ab32e2e2971fe314e3a19be0e03dc3140c7968cc88d4e02c80e1a0117669"
)
OFFICIAL_HASHES = {
    "LICENSE": (
        "2b51ab429d27ce74a8afc18a4b99beb8066b4c7e48e494ece56288ee5b9df140"
    ),
    "README.md": (
        "bc50ceb1174e73105ffdec19c36b8bbf6a349901d9446ff703bc8cfc8cdd1968"
    ),
    "go.mod": (
        "fcfff81f6bb216f0191f5925aa0802f23985741051c6f9934deb3e4f4033cf7d"
    ),
    "go.sum": (
        "e53ccd749964dada4192a2c4d4039d97bb27acc5967da7e30ca8f92d155ac94b"
    ),
    "pkg/razorpay/tokens.go": (
        "48b314c65f602c588ab1c1ed9fd5ed247ae5e50ce9996c42ec4d241f0600d5ce"
    ),
    "pkg/razorpay/tools.go": (
        "e6ba1fde19ab1b09a3101329f269c620d8d9f8ab6d1afac1b0f78bc7bf298065"
    ),
}

OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
OPENAI_FILE_COUNT = 3
OPENAI_INVENTORY_SHA256 = (
    "cf338a15f01f2aefed5d5cecaad0478e893239431fb688108288ebf1479520ff"
)
OPENAI_HASHES = {
    ".app.json": (
        "ab455c309a771e3c6196a0d5b66d78ab26960fa679b2f411d8ab9918fcb9560c"
    ),
    ".codex-plugin/plugin.json": (
        "797c936ece70d148a42fffc17db59b090fa6d9eab666abc3bb07f247c7630a76"
    ),
    "assets/logo.png": (
        "2998fc8eefca5b8f516ff1b50598a566193fd19e512eab46e36c9ae28786c98b"
    ),
}

PLUGIN_HASHES = {
    "go.mod": (
        "f9bd7e4e71c698035dff2e8083bc87589b04b311368d8b419f2e76719c949b87"
    ),
    "go.sum": (
        "9963007111c3f94736197b97d172d66ae2e53cb2bdf166c740a6944ceb42d97d"
    ),
    "cmd/razorpay-readonly/main.go": (
        "d1d67f17cf3b81946967c80c3563db9369c16c63bc3978be73dcddb8e0d59c12"
    ),
    "cmd/razorpay-readonly/main_test.go": (
        "abdd8b3c56081b724b12fdeb5c4a83d1b2565562fa0dfc6b4093ab5bcb0e56ee"
    ),
    "mcp/start.mjs": (
        "9e5b980272d746fe7b5938b4f4f212d5b0b6517ea9513e55218ce7f694e6e4af"
    ),
}

EXPECTED_TOOLS = (
    "fetch_all_instant_settlements",
    "fetch_all_orders",
    "fetch_all_payment_links",
    "fetch_all_payments",
    "fetch_all_payouts",
    "fetch_all_qr_codes",
    "fetch_all_refunds",
    "fetch_all_settlements",
    "fetch_instant_settlement_with_id",
    "fetch_multiple_refunds_for_payment",
    "fetch_order",
    "fetch_order_payments",
    "fetch_payment",
    "fetch_payment_card_details",
    "fetch_payment_link",
    "fetch_payments_for_qr_code",
    "fetch_payout_with_id",
    "fetch_qr_code",
    "fetch_qr_codes_by_customer_id",
    "fetch_qr_codes_by_payment_id",
    "fetch_refund",
    "fetch_settlement_recon_details",
    "fetch_settlement_with_id",
    "fetch_specific_refund_for_payment",
    "fetch_tokens",
)
TOOL_NAMES_SHA256 = (
    "5b2ed7545b884fee2e6437ef46edb5c7eafeb61025537645ce9c29f6632bf88e"
)
TOOL_SCHEMA_SHA256 = (
    "0ff285ace0b554bbea32a7cd781b591b4fdf955e2169126590838083776d5cd1"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        required=True,
        help="Pinned checkout of razorpay/razorpay-mcp-server.",
    )
    parser.add_argument(
        "--openai-source",
        type=Path,
        required=True,
        help="Pinned checkout of github.com/openai/plugins.",
    )
    parser.add_argument(
        "--go",
        type=Path,
        required=True,
        help="Verified Go 1.24.2 executable.",
    )
    return parser.parse_args()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: object) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()
    )


def git_value(source: Path, expression: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", expression],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def inventory(source: Path) -> tuple[list[str], str]:
    paths = sorted(
        path.relative_to(source).as_posix()
        for path in source.rglob("*")
        if path.is_file() and ".git" not in path.parts
    )
    body = "".join(
        f"{sha256((source / relative).read_bytes())}  {relative}\n"
        for relative in paths
    )
    return paths, sha256(body.encode())


def verify_official_source(source: Path) -> None:
    if git_value(source, "HEAD") != OFFICIAL_REVISION:
        raise ValueError("Razorpay official source revision changed")
    if git_value(source, "HEAD^{tree}") != OFFICIAL_TREE:
        raise ValueError("Razorpay official source tree changed")
    if subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout:
        raise ValueError("Razorpay official source checkout is dirty")

    remotes = subprocess.run(
        ["git", "remote", "-v"],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    if "github.com/razorpay/razorpay-mcp-server" not in remotes:
        raise ValueError("Razorpay official source remote changed")

    paths, digest = inventory(source)
    if len(paths) != OFFICIAL_FILE_COUNT or digest != OFFICIAL_INVENTORY_SHA256:
        raise ValueError("Razorpay official source inventory changed")
    for relative, expected in OFFICIAL_HASHES.items():
        if sha256((source / relative).read_bytes()) != expected:
            raise ValueError(f"Razorpay official source changed at {relative}")

    license_text = (source / "LICENSE").read_text()
    if (
        "MIT License" not in license_text
        or "Copyright (c) 2025 Razorpay" not in license_text
    ):
        raise ValueError("Razorpay official license changed")

    tools = (source / "pkg/razorpay/tools.go").read_text()
    tokens = (source / "pkg/razorpay/tokens.go").read_text()
    for marker in (
        "payments.AddWriteTools(FetchSavedPaymentMethods(obs, client))",
        'toolsets.NewToolsetGroup(readOnly)',
        'toolsets.NewToolset("payments"',
        'toolsets.NewToolset("settlements"',
    ):
        if marker not in tools:
            raise ValueError(f"Razorpay tool classification lacks {marker!r}")
    for marker in (
        '"contact"',
        "client.Customer.Create(customerData, nil)",
        "client.Request.Get(url, nil, nil)",
        '"fetch_tokens"',
    ):
        if marker not in tokens:
            raise ValueError(f"Razorpay token behavior lacks {marker!r}")


def verify_openai_source(source: Path) -> None:
    if git_value(source, "HEAD") != OPENAI_REVISION:
        raise ValueError("OpenAI plugin snapshot revision changed")
    plugin = source / "plugins/razorpay"
    paths, digest = inventory(plugin)
    if len(paths) != OPENAI_FILE_COUNT or digest != OPENAI_INVENTORY_SHA256:
        raise ValueError("Razorpay Codex snapshot inventory changed")
    for relative, expected in OPENAI_HASHES.items():
        if sha256((plugin / relative).read_bytes()) != expected:
            raise ValueError(f"Razorpay Codex snapshot changed at {relative}")

    manifest = json.loads(
        (plugin / ".codex-plugin/plugin.json").read_text()
    )
    app = json.loads((plugin / ".app.json").read_text())
    interface = manifest.get("interface", {})
    if (
        manifest.get("name") != "razorpay"
        or manifest.get("version") != "1.0.3"
        or interface.get("developerName")
        != "Razorpay Software Private Limited"
        or app.get("apps", {}).get("razorpay", {}).get("id")
        != "asdk_app_69529eb504788191a8800810327e0b2c"
    ):
        raise ValueError("Razorpay Codex developer evidence changed")
    for marker in (
        "Track payouts and reconciliation data",
        "Access saved customer payment methods",
        "Read-only access",
        "no transactions are executed",
    ):
        if marker not in interface.get("longDescription", ""):
            raise ValueError(f"Razorpay Codex capability lacks {marker!r}")


def verify_plugin(plugin: Path, go: Path) -> None:
    for relative, expected in PLUGIN_HASHES.items():
        if sha256((plugin / relative).read_bytes()) != expected:
            raise ValueError(f"Razorpay Ghast adapter changed at {relative}")

    manifest = json.loads(
        (plugin / ".ghast-plugin/plugin.json").read_text()
    )
    if (
        manifest.get("name") != "razorpay"
        or manifest.get("repository") != OFFICIAL_REPOSITORY
        or manifest.get("upstreamRevision") != OFFICIAL_REVISION
        or manifest.get("license") != "MIT"
        or manifest.get("portStatus")
        != "official-source-readonly-adapter"
    ):
        raise ValueError("Razorpay Ghast manifest changed")

    version = subprocess.run(
        [str(go), "version"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    if "go version go1.24.2 " not in version:
        raise ValueError(f"expected Go 1.24.2, found {version.strip()}")

    subprocess.run([str(go), "mod", "verify"], cwd=plugin, check=True)
    subprocess.run([str(go), "vet", "./..."], cwd=plugin, check=True)
    subprocess.run([str(go), "test", "-race", "./..."], cwd=plugin, check=True)
    formatted = subprocess.run(
        [str(go.parent / "gofmt"), "-l", "."],
        cwd=plugin,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    if formatted:
        raise ValueError(f"Razorpay Go files need formatting:\n{formatted}")

    with tempfile.TemporaryDirectory(prefix="ghast-razorpay-audit-") as temp:
        binary = Path(temp) / "razorpay-readonly"
        subprocess.run(
            [
                str(go),
                "build",
                "-mod=readonly",
                "-trimpath",
                "-o",
                str(binary),
                "./cmd/razorpay-readonly",
            ],
            cwd=plugin,
            check=True,
        )
        messages = (
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "ghast-razorpay-audit",
                        "version": "1.0",
                    },
                },
            },
            {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {},
            },
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {},
            },
        )
        payload = "".join(
            json.dumps(message, separators=(",", ":")) + "\n"
            for message in messages
        )
        env = {
            **os.environ,
            "RAZORPAY_KEY_ID": "rzp_test_ghast_audit",
            "RAZORPAY_KEY_SECRET": "ghast_audit_secret",
        }
        result = subprocess.run(
            [str(binary)],
            cwd=plugin,
            env=env,
            input=payload,
            capture_output=True,
            text=True,
            check=True,
        )

    responses = [
        json.loads(line)
        for line in result.stdout.splitlines()
        if line.strip()
    ]
    tool_response = next(
        response for response in responses if response.get("id") == 2
    )
    tools = tool_response["result"]["tools"]
    tools = sorted(tools, key=lambda tool: tool["name"])
    names = tuple(tool["name"] for tool in tools)
    if names != EXPECTED_TOOLS:
        raise ValueError("Razorpay adapter tool inventory changed")
    if canonical_sha256(list(names)) != TOOL_NAMES_SHA256:
        raise ValueError("Razorpay adapter tool-name digest changed")
    if canonical_sha256(tools) != TOOL_SCHEMA_SHA256:
        raise ValueError("Razorpay adapter tool-schema digest changed")
    for tool in tools:
        annotations = tool.get("annotations", {})
        if (
            annotations.get("readOnlyHint") is not True
            or annotations.get("destructiveHint") is not False
        ):
            raise ValueError(f"{tool['name']}: unsafe tool annotations")

    fetch_tokens = next(
        tool for tool in tools if tool["name"] == "fetch_tokens"
    )
    schema = fetch_tokens["inputSchema"]
    if (
        schema.get("required") != ["customer_id"]
        or set(schema.get("properties", {})) != {"customer_id"}
        or "contact" in json.dumps(fetch_tokens)
    ):
        raise ValueError("Razorpay fetch_tokens mutation path reappeared")


def main() -> int:
    args = parse_args()
    source = args.source_root.resolve()
    openai_source = args.openai_source.resolve()
    go = args.go.resolve()
    plugin = Path("plugins/razorpay").resolve()
    verify_official_source(source)
    verify_openai_source(openai_source)
    verify_plugin(plugin, go)
    print(
        "verified Razorpay official-source read-only adapter "
        f"{OFFICIAL_REVISION[:12]} with 25 tools"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
