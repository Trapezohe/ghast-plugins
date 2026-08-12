#!/usr/bin/env python3
"""Import the licensed Binance skills into one Ghast plugin."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


EXPECTED_SOURCE_REVISION = "2863a186d2bbd8987fa4790d7b81a299a58364ce"
BINANCE_REPOSITORY = "https://github.com/binance/binance-skills-hub"
PLUGIN_DIR = Path("plugins")
SELECTED_SKILLS = {
    "binance": "skills/binance/binance",
    "fiat": "skills/binance/fiat",
    "onchain-pay": "skills/binance/onchain-pay",
    "p2p": "skills/binance/p2p",
}

SAFETY_SECTION = """\
## Ghast financial execution policy

These rules override less restrictive confirmation examples elsewhere in this skill:

- Never ask the user to paste API secrets, private keys, seed phrases, or PEM contents into chat.
- Use environment variables or an existing local Binance CLI profile for credentials. Never place a secret directly in a command argument, log, or generated file.
- Public market-data and authenticated read-only requests may run after the user asks for them.
- Before any order, cancellation, transfer, withdrawal, conversion, subscription, redemption, loan, staking action, advertisement change, appeal mutation, payment, pre-order, or other state-changing request, show the exact environment/profile, action, asset, amount, price or slippage, destination, and known irreversible effects.
- Execute a state-changing request only after the user replies with the exact text `CONFIRM BINANCE`. A confirmation authorizes one displayed action and expires immediately after that action.
- Never infer production intent. Use testnet or demo for state-changing examples unless the user explicitly chooses production and then provides the required confirmation.
- Prefer quote, test, preview, or dry-run endpoints when available. After execution, query status and report whether the action is pending, filled, completed, rejected, or failed.

"""

SECURE_ONCHAIN_SCRIPT = """\
#!/usr/bin/env bash
set -euo pipefail

# Binance Onchain-Pay Open API - Sign & Call
# Credentials are read from the environment so they do not appear in process args.
# Usage: sign_and_call.sh <api_path> [json_body]

: "${BINANCE_ONCHAIN_PAY_BASE_URL:?Set BINANCE_ONCHAIN_PAY_BASE_URL}"
: "${BINANCE_ONCHAIN_PAY_CLIENT_ID:?Set BINANCE_ONCHAIN_PAY_CLIENT_ID}"
: "${BINANCE_ONCHAIN_PAY_API_KEY:?Set BINANCE_ONCHAIN_PAY_API_KEY}"
: "${BINANCE_ONCHAIN_PAY_PEM_PATH:?Set BINANCE_ONCHAIN_PAY_PEM_PATH}"

API_PATH="${1:?API path is required}"
JSON_BODY="${2:-}"
timestamp=$(($(date +%s) * 1000))
payload="${JSON_BODY}${timestamp}"

signature=$(printf '%s' "$payload" \\
  | openssl dgst -sha256 -sign "$BINANCE_ONCHAIN_PAY_PEM_PATH" \\
  | openssl enc -base64 -A)

curl_args=(
  --silent
  --show-error
  --fail-with-body
  --location
  --request POST "${BINANCE_ONCHAIN_PAY_BASE_URL%/}/${API_PATH#/}"
  --header "X-Tesla-ClientId: ${BINANCE_ONCHAIN_PAY_CLIENT_ID}"
  --header "X-Tesla-SignAccessToken: ${BINANCE_ONCHAIN_PAY_API_KEY}"
  --header "X-Tesla-Signature: ${signature}"
  --header "X-Tesla-Timestamp: ${timestamp}"
  --header "Content-Type: application/json"
  --header "x-trace-id: ghast_skill_${timestamp}"
  --header "User-Agent: ghast-binance-onchain-pay/0.1.2"
)

if [ -n "$JSON_BODY" ]; then
  curl_args+=(--data-raw "$JSON_BODY")
fi

response=$(curl "${curl_args[@]}")
printf '%s' "$response" | python3 -m json.tool 2>/dev/null || printf '%s\\n' "$response"
"""

CORE_AUTH_REFERENCE = """\
# Binance Authentication

Credentials must be configured outside chat before an authenticated request.

## Environment variables

- `BINANCE_API_KEY`: Binance API key
- `BINANCE_SECRET_KEY`: HMAC secret, private-key path, or private-key content
- `BINANCE_API_ENV`: `prod`, `testnet`, or `demo`

The agent may reference these specific variables inside one command, but must
never print them, dump the environment, or copy them into another file.

## Existing CLI profiles

```bash
binance-cli profile list
binance-cli profile view
binance-cli profile select --name <name>
```

Use `--profile <name>` to override the active profile. Do not create or update
profiles from credentials supplied in chat. Users who need a new profile should
configure it themselves in a trusted terminal with
`binance-cli profile create -i`, then ask the agent to use the profile name.

## Security rules

- Never run `printenv`, `env`, or an unscoped `export`.
- Never read `.env`, `TOOLS.md`, or arbitrary secret files.
- Never echo or log raw credentials or private-key paths.
- Use testnet or demo for state-changing examples unless production is explicit.
- Follow the Ghast financial execution policy before every write operation.
"""

HMAC_AUTH_REFERENCE = """\
# Binance P2P Authentication

Authenticated P2P SAPI requests require HMAC SHA256 credentials already present
in `BINANCE_API_KEY` and `BINANCE_SECRET_KEY`.

## Base URL

`https://api.binance.com`

## SAPI-specific behavior

- Keep parameters in their original insertion order; do not sort them.
- Percent-encode names and values with RFC 3986 before signing.
- Add `timestamp` in Unix milliseconds and optionally `recvWindow`.
- Use the exact encoded query string for both the signature and request.

## Secure example

```bash
: "${BINANCE_API_KEY:?Set BINANCE_API_KEY outside chat}"
: "${BINANCE_SECRET_KEY:?Set BINANCE_SECRET_KEY outside chat}"

BASE_URL="https://api.binance.com"
TIMESTAMP=$(($(date +%s) * 1000))
QUERY="page=1&rows=20&recvWindow=60000&timestamp=${TIMESTAMP}"
SIGNATURE=$(printf '%s' "$QUERY" \\
  | openssl dgst -sha256 -hmac "$BINANCE_SECRET_KEY" \\
  | cut -d' ' -f2)

curl --silent --show-error --fail-with-body \\
  "${BASE_URL}/sapi/v1/c2c/orderMatch/listUserOrderHistory?${QUERY}&signature=${SIGNATURE}" \\
  -H "X-MBX-APIKEY: ${BINANCE_API_KEY}" \\
  -H "User-Agent: ghast-binance-p2p/1.1.0"
```

Never print either variable or store it in a generated file. Use an IP
allowlist and the minimum API permissions required for the requested endpoint.
"""

FIAT_AUTH_REFERENCE = """\
# Binance Fiat Authentication

Authenticated fiat SAPI requests require credentials configured outside chat.
Use `BINANCE_API_KEY` with one supported signing method:

- HMAC: `BINANCE_SECRET_KEY`
- RSA or Ed25519: `BINANCE_PRIVATE_KEY_PATH`

Never print these variables, inspect the full environment, or write them to a
workspace file.

## Signing process

1. Build the request query in its required order with a Unix-millisecond
   `timestamp` and optional `recvWindow`.
2. Percent-encode the exact names and values with RFC 3986.
3. Sign the exact encoded query with HMAC SHA256, RSA, or Ed25519.
4. Append `signature` and send `X-MBX-APIKEY`.

## HMAC example

```bash
: "${BINANCE_API_KEY:?Set BINANCE_API_KEY outside chat}"
: "${BINANCE_SECRET_KEY:?Set BINANCE_SECRET_KEY outside chat}"

BASE_URL="https://api.binance.com"
TIMESTAMP=$(($(date +%s) * 1000))
QUERY="transactionType=0&timestamp=${TIMESTAMP}"
SIGNATURE=$(printf '%s' "$QUERY" \\
  | openssl dgst -sha256 -hmac "$BINANCE_SECRET_KEY" \\
  | cut -d' ' -f2)

curl --silent --show-error --fail-with-body \\
  "${BASE_URL}/sapi/v1/fiat/orders?${QUERY}&signature=${SIGNATURE}" \\
  -H "X-MBX-APIKEY: ${BINANCE_API_KEY}" \\
  -H "User-Agent: ghast-binance-fiat/1.1.0"
```

Use an IP allowlist and minimum permissions. Follow the Ghast financial
execution policy before any state-changing operation.
"""

SECURE_FIAT_CREDENTIALS = """\
## Authentication

Authenticated endpoints use credentials already present in the process
environment:

- `BINANCE_API_KEY`
- `BINANCE_SECRET_KEY` for HMAC, or `BINANCE_PRIVATE_KEY_PATH` for RSA/Ed25519

Do not search for `.env`, `TOOLS.md`, inline credential files, or raw secrets.
Do not ask the user to paste credentials into chat. If the variables are
missing, stop and ask the user to configure them outside the conversation.

## Security

- Never dump the environment or print a credential.
- Never create or update a credential file.
- Send credentials only to the documented Binance API base URL.
- Use IP allowlists and minimum permissions.
- Apply the Ghast financial execution policy before any write operation.

"""

SECURE_ONCHAIN_SECURITY = """\
## Security

- Read credentials only from `BINANCE_ONCHAIN_PAY_BASE_URL`,
  `BINANCE_ONCHAIN_PAY_CLIENT_ID`, `BINANCE_ONCHAIN_PAY_API_KEY`, and
  `BINANCE_ONCHAIN_PAY_PEM_PATH`.
- Never read or create `.local.md`, `.env`, `TOOLS.md`, or another credential
  file.
- Never show the API key, private-key content, or private-key path.
- Never send credentials to a URL other than
  `BINANCE_ONCHAIN_PAY_BASE_URL`.
- Apply the Ghast financial execution policy before `pre-order` or another
  state-changing request.

"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Checkout of github.com/binance/binance-skills-hub.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    revision = git_revision(source)
    if revision != EXPECTED_SOURCE_REVISION:
        raise ValueError(
            f"{source}: expected revision {EXPECTED_SOURCE_REVISION}, found {revision}"
        )

    with tempfile.TemporaryDirectory(prefix=".binance-", dir=PLUGIN_DIR) as temp:
        staging_dir = Path(temp)
        skills_dir = staging_dir / "skills"
        skills_dir.mkdir()

        for name, relative_path in SELECTED_SKILLS.items():
            source_skill = source / relative_path
            license_path = source_skill / "LICENSE.md"
            if not (source_skill / "SKILL.md").is_file():
                raise ValueError(f"{source_skill}: missing SKILL.md")
            if not license_path.is_file() or "MIT License" not in license_path.read_text():
                raise ValueError(f"{source_skill}: missing a verifiable MIT license")
            shutil.copytree(
                source_skill,
                skills_dir / name,
                copy_function=shutil.copy2,
            )
            inject_safety_policy(skills_dir / name / "SKILL.md")

        secure_onchain_pay(skills_dir / "onchain-pay")
        secure_binance_cli(skills_dir / "binance")
        secure_fiat(skills_dir / "fiat")
        secure_p2p(skills_dir / "p2p")
        validate_security(skills_dir)
        shutil.copy2(
            source / SELECTED_SKILLS["binance"] / "LICENSE.md",
            staging_dir / "LICENSE",
        )

        manifest = {
            "name": "binance",
            "version": "2.0.0-ghast.1",
            "description": (
                "Comprehensive Binance workflows for public market data, Spot, "
                "Futures, Options, Convert, Margin, Earn, Loans, Wallet, Fiat, "
                "P2P, and Onchain Pay."
            ),
            "category": "finance",
            "author": {
                "name": "Binance",
                "url": "https://www.binance.com",
            },
            "homepage": BINANCE_REPOSITORY,
            "repository": BINANCE_REPOSITORY,
            "upstreamRevision": revision,
            "license": "MIT",
            "icon": "./assets/icon.svg",
            "skills": "./skills/",
            "includedSkills": sorted(SELECTED_SKILLS),
            "portStatus": "licensed-subset",
        }
        manifest_dir = staging_dir / ".ghast-plugin"
        manifest_dir.mkdir()
        (manifest_dir / "plugin.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        )
        (staging_dir / "README.md").write_text(readme(revision))

        target_dir = PLUGIN_DIR / "binance"
        if target_dir.exists():
            shutil.rmtree(target_dir)
        staging_dir.rename(target_dir)

    print("imported Binance plugin with 4 licensed skills")
    return 0


def git_revision(repository: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def inject_safety_policy(skill_path: Path) -> None:
    content = skill_path.read_text()
    marker = "\n---\n"
    frontmatter_end = content.find(marker, 4)
    if frontmatter_end == -1:
        raise ValueError(f"{skill_path}: missing YAML frontmatter")
    insertion_point = frontmatter_end + len(marker)
    content = (
        content[:insertion_point]
        + "\n"
        + SAFETY_SECTION
        + content[insertion_point:].lstrip("\n")
    )
    skill_path.write_text(content)


def secure_onchain_pay(skill_dir: Path) -> None:
    for path in (skill_dir / ".local.md.example", skill_dir / ".gitignore"):
        if path.exists():
            path.unlink()

    script_path = skill_dir / "scripts/sign_and_call.sh"
    script_path.write_text(SECURE_ONCHAIN_SCRIPT)
    script_path.chmod(0o755)

    skill_path = skill_dir / "SKILL.md"
    content = skill_path.read_text()
    content = content.replace(
        """Use the default account (prod) unless the user specifies otherwise. You need:

- **BASE_URL**: API base URL
- **CLIENT_ID**: Client identifier
- **API_KEY**: The sign access token
- **PEM_PATH**: Absolute path to the RSA private key PEM file

Use the account marked `(default)` in `.local.md`.
""",
        """Credentials must already be configured outside chat:

- `BINANCE_ONCHAIN_PAY_BASE_URL`: API base URL
- `BINANCE_ONCHAIN_PAY_CLIENT_ID`: Client identifier
- `BINANCE_ONCHAIN_PAY_API_KEY`: Sign access token
- `BINANCE_ONCHAIN_PAY_PEM_PATH`: Absolute path to the RSA private key PEM file

Do not create or read `.local.md`, and do not place these values in command arguments.
""",
    )
    content = content.replace(
        """bash <skill_path>/scripts/sign_and_call.sh \\
  "<BASE_URL>" \\
  "<API_PATH>" \\
  "<CLIENT_ID>" \\
  "<API_KEY>" \\
  "<PEM_PATH>" \\
  '<JSON_BODY>'
""",
        """bash <skill_path>/scripts/sign_and_call.sh \\
  "<API_PATH>" \\
  '<JSON_BODY>'
""",
    )
    content = content.replace(
        "- If the user has configured `Default Address` and `Default Network` in `.local.md`, use them automatically\n"
        "- If not configured or not provided by user, ASK the user to provide both values before proceeding",
        "- Require the user to provide `address` and `network` for the displayed operation summary\n"
        "- Never load a default destination from a credential file",
    )
    content = content.replace(
        "| network | string | **Yes*** | Blockchain network (can use default from `.local.md`) |",
        "| network | string | **Yes*** | Blockchain network selected by the user |",
    )
    content = content.replace(
        "\\* Recommended: These parameters should be provided. If not specified by user, check `.local.md` for defaults. If no defaults exist, ask user before proceeding.",
        "\\* Required by Ghast policy: ask the user when either value is missing.",
    )
    content = replace_section(
        content,
        "## Security\n",
        "## User Agent Header\n",
        SECURE_ONCHAIN_SECURITY,
    )
    content = content.replace(
        "3. Use stored credentials if available, otherwise ask the user",
        "3. Verify the required environment variables exist; never ask for their values",
    )
    old_example_start = "### Example Pre-order Request\n"
    if old_example_start in content:
        content = content[: content.index(old_example_start)] + """\
### Example Pre-order Request

After displaying the complete operation summary and receiving the exact reply
`CONFIRM BINANCE`:

```bash
TIMESTAMP=$(($(date +%s) * 1000))
ORDER_ID="order$(date +%s)"

bash /path/to/scripts/sign_and_call.sh \
  "papi/v1/ramp/connect/buy/pre-order" \
  "{\\"externalOrderId\\":\\"$ORDER_ID\\",\\"merchantCode\\":\\"<MERCHANT_CODE>\\",\\"merchantName\\":\\"<MERCHANT_NAME>\\",\\"ts\\":$TIMESTAMP,\\"fiatCurrency\\":\\"USD\\",\\"requestedAmount\\":100,\\"cryptoCurrency\\":\\"BNB\\",\\"amountType\\":1,\\"address\\":\\"0x...\\",\\"network\\":\\"BSC\\",\\"payMethodCode\\":\\"BUY_CARD\\"}"
```
"""
    skill_path.write_text(content)


def secure_binance_cli(skill_dir: Path) -> None:
    (skill_dir / "references/auth.md").write_text(CORE_AUTH_REFERENCE)
    skill_path = skill_dir / "SKILL.md"
    content = skill_path.read_text().replace(
        "- ⚠️ **Prod transactions** — always ask user to type `CONFIRM` before executing.",
        "- **Prod transactions** — follow the Ghast policy and require the exact reply `CONFIRM BINANCE`.",
    )
    skill_path.write_text(content)


def secure_fiat(skill_dir: Path) -> None:
    (skill_dir / "references/authentication.md").write_text(FIAT_AUTH_REFERENCE)
    sapi_path = skill_dir / "references/sapi-endpoints.md"
    content = sapi_path.read_text()
    content = replace_section(
        content,
        "## Authentication\n",
        "## Signing Requests\n",
        SECURE_FIAT_CREDENTIALS,
    )
    sapi_path.write_text(content)


def secure_p2p(skill_dir: Path) -> None:
    (skill_dir / "references/authentication.md").write_text(HMAC_AUTH_REFERENCE)
    skill_path = skill_dir / "SKILL.md"
    content = skill_path.read_text()
    content = content.replace(
        """### Storage guidance
- Prefer environment injection (session/runtime env vars) over writing to disk.
- Only write to `.env` if the user explicitly agrees.
- Ensure `.env` is in `.gitignore` before saving.
""",
        """### Storage guidance
- Credentials must already exist in `BINANCE_API_KEY` and `BINANCE_SECRET_KEY`.
- Never read or create `.env`, `TOOLS.md`, or another credential file.
""",
    )
    content = content.replace(
        "Invalid API key (-2015): prompt to verify `.env` / API Management.",
        "Invalid API key (-2015): prompt to verify the configured environment variables and API permissions.",
    )
    skill_path.write_text(content)


def replace_section(content: str, start: str, end: str, replacement: str) -> str:
    start_index = content.find(start)
    end_index = content.find(end, start_index + len(start))
    if start_index == -1 or end_index == -1:
        raise ValueError(f"cannot replace section {start!r} through {end!r}")
    return content[:start_index] + replacement + content[end_index:]


def validate_security(skills_dir: Path) -> None:
    for skill_path in skills_dir.glob("*/SKILL.md"):
        if "## Ghast financial execution policy" not in skill_path.read_text():
            raise ValueError(f"{skill_path}: missing Ghast execution policy")

    forbidden = (
        "Credentials are stored in a `.local.md`",
        "Read the `.local.md`",
        "Store in `TOOLS.md`",
        "Only write to `.env`",
        "profile create --name",
        'API_KEY="your_api_key"',
        'SECRET_KEY="your_secret_key"',
        "<YOUR_API_KEY>",
    )
    for path in skills_dir.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".sh"}:
            continue
        if path.name in {"CHANGELOG.md", "LICENSE.md"}:
            continue
        content = path.read_text()
        matches = [pattern for pattern in forbidden if pattern in content]
        if matches:
            raise ValueError(f"{path}: forbidden credential patterns {matches}")


def readme(revision: str) -> str:
    return f"""\
# Binance for Ghast

This plugin ports the independently MIT-licensed Binance skills from
`binance/binance-skills-hub` at `{revision}`.

## Included

- `binance`: Binance CLI coverage for public data and authenticated Spot,
  Futures, Options, Convert, Margin, Earn, Loans, Wallet, sub-account, staking,
  mining, gift card, rebate, and related API families.
- `fiat`: public fiat capabilities, quotes, methods, limits, and authenticated
  fiat order history.
- `p2p`: P2P market discovery plus authenticated order, appeal-evidence, and
  advertisement-management workflows.
- `onchain-pay`: signed merchant Onchain Pay discovery, quote, order, and
  pre-order workflows.

The repository's Web3 Agentic Wallet, payment-assistant, Square posting, and
other skills were not copied because this pinned snapshot does not include a
standalone license file for those directories.

## Safety

Read-only requests are available without transaction confirmation. Every
state-changing request requires a fresh operation summary and the exact reply
`CONFIRM BINANCE`; production is never inferred from an existing profile.
Credentials remain in environment variables or local Binance CLI profiles and
must not be pasted into chat.

The plugin provides procedural skills and does not bundle `binance-cli`,
credentials, an exchange account, or merchant permissions.
"""


if __name__ == "__main__":
    raise SystemExit(main())
