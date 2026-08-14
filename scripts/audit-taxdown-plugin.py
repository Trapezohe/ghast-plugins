#!/usr/bin/env python3
"""Verify TaxDown's official MCP and enforce its client-auth blocker."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


sys.dont_write_bytecode = True

PLUGIN_ID = "taxdown"
REVIEWS_PATH = Path("third-party-plugin-reviews.json")
EXPECTED_OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
OPENAI_HASHES = {
    ".app.json": "3dac2ec0cb836b11be146030ba1902193f86cfe76b7de3a76ea3a677c4a1f0a0",
    ".codex-plugin/plugin.json": (
        "f2cb7c22306173bcf0447b176a27d03864a8f6ca03c16aaa0d381a29830beea8"
    ),
    "assets/logo.png": (
        "2f08cd2f465877fd048b0cb6de74cc39c797f0e267ba62a4786e8db9d7352d53"
    ),
}
OPENAI_INVENTORY_SHA256 = (
    "59177fde896373afe8082670626e41083847e0b763d3fa96ff2bdc0e569449d1"
)

AI_URL = "https://taxdown.es/asesor-ia"
TERMS_URL = "https://taxdown.es/terminos-condiciones"
LEGAL_URL = "https://taxdown.es/aviso-legal"
SECURITY_URL = "https://taxdown.es/seguridad"
AI_CORE_SHA256 = (
    "a0e5964a0f9763985544e2327f74923fd032b9aed41cc4a95ec719d61211769f"
)
TERMS_CORE_SHA256 = (
    "40e88ffabcb2c4fc761bcb5f990e84d006e58f7972c8e24ea8fc91bf92e3d51e"
)
LEGAL_CORE_SHA256 = (
    "75b1eca7e62b09c0097ff8a72dd3024e6b4f431ac549df2f18ba42911d266a7e"
)
SECURITY_CORE_SHA256 = (
    "b6799f80b96e9e56bfd6928c5c0f748ba10321e211b662f2a5d79bb70758ea1d"
)

MCP_URL = "https://mcp.taxdown.es/mcp"
HEALTH_URL = "https://mcp.taxdown.es/health"
PROTECTED_RESOURCE_URL = (
    "https://mcp.taxdown.es/.well-known/oauth-protected-resource"
)
AUTHORIZATION_SERVER_URL = (
    "https://mcp.taxdown.es/.well-known/oauth-authorization-server"
)
REGISTRATION_URL = "https://mcp.taxdown.es/register"
PROTECTED_RESOURCE_SHA256 = (
    "452319f67349a529f6a8592ceaf3ac56a7b7b9236519ccea1c643750e1a7eb08"
)
AUTHORIZATION_SERVER_SHA256 = (
    "1ac920a76fceb876b8f8b847c95678afdd2d971bc3c93d677ccf1b6579f699d5"
)
UNAUTHORIZED_CANONICAL_SHA256 = (
    "da7512f66622c27c985f2324a7041dabe34fe3ff552d378c570be9a32e05e102"
)
LOCALHOST_REJECTION_SHA256 = (
    "03efda369924d0c3b04ec07ec503ede501e728303f903fadfebb7e78c193e093"
)
LOOPBACK_REJECTION_SHA256 = (
    "d67bf7d9b70569f18ea370b3c4e0b4b924973e8337af2612d59a1545b9b7f1de"
)
UPSTREAM_REVISION = (
    "taxdown-luz-a0e5964a0f97"
    "+terms-40e88ffabcb2"
    "+legal-75b1eca7e62b"
    "+security-b6799f80b96e"
    "+resource-452319f67349"
    "+oauth-1ac920a76fce"
    "+boundary-da7512f66622"
    "+redirect-03efda369924"
    "+openai-59177fde8963"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--openai-source",
        type=Path,
        required=True,
        help="Pinned checkout of github.com/openai/plugins.",
    )
    return parser.parse_args()


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_sha256(value: object) -> str:
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
    )


def fetch(
    url: str,
    *,
    data: bytes | None = None,
    method: str | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[int, dict[str, str], bytes]:
    request_headers = {
        "Accept": "application/json",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "User-Agent": "ghast-taxdown-audit/1.0",
    }
    request_headers.update(headers or {})
    request = urllib.request.Request(
        url, data=data, method=method, headers=request_headers
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return (
                response.status,
                {key.lower(): value for key, value in response.headers.items()},
                response.read(),
            )
    except urllib.error.HTTPError as error:
        return (
            error.code,
            {key.lower(): value for key, value in error.headers.items()},
            error.read(),
        )


def normalize_html(value: bytes) -> str:
    text = value.decode("utf-8", "replace")
    text = re.sub(
        r"<script[^>]*>.*?</script>",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(
        r"<style[^>]*>.*?</style>",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def section(value: str, start_marker: str, end_marker: str) -> str:
    start = value.find(start_marker)
    if start < 0:
        raise ValueError(f"TaxDown evidence is missing {start_marker!r}")
    end = value.find(end_marker, start + len(start_marker))
    if end < 0:
        raise ValueError(f"TaxDown evidence is missing {end_marker!r}")
    return value[start:end].strip()


def verify_official_pages() -> None:
    documents = (
        (
            AI_URL,
            "Luz · La IA fiscal de TaxDown",
            "Resuelve tu próxima duda fiscal con Luz",
            AI_CORE_SHA256,
            (
                "primer chat experto fiscal de España",
                "Resuelve tus dudas al instante",
                "tus impuestos",
                "respuesta a tu medida",
                "normativa que te aplica",
                "deducir siendo autónomo",
                "vendido acciones",
                "deducciones hay en mi comunidad",
            ),
        ),
        (
            TERMS_URL,
            "Última actualización: 10 de Febrero de 2026.",
            "Términos y Condiciones específicos para autónomos",
            TERMS_CORE_SHA256,
            (
                "Taxdown, S.L.",
                "preparación de la declaración de la renta",
                "servicios de asesoramiento fiscal",
                "CONFIRMAR PRESENTACIÓN",
                "información facilitada por el Usuario",
                "PROPIEDAD INTELECTUAL E INDUSTRIAL",
                "No se entiende cedido",
                "API (interfaz de programación de aplicaciones)",
            ),
        ),
        (
            LEGAL_URL,
            "Última actualización: 23/05/2025",
            (
                "comprometiéndonos a buscar en todo momento una solución "
                "amistosa del conflicto."
            ),
            LEGAL_CORE_SHA256,
            (
                "Tax Down S.L.",
                "B-88287164",
                "propia plataforma, software",
                "ámbito estrictamente doméstico",
                "prohibido modificar, copiar, reproducir",
                "Acceder sin autorización",
                "Quebrantar, o intentar quebrantar, las medidas de seguridad",
            ),
        ),
        (
            SECURITY_URL,
            "Tu seguridad es nuestra prioridad",
            "Descarga ya nuestra app",
            SECURITY_CORE_SHA256,
            (
                "Encriptación de datos",
                "Firewalls de seguridad",
                "Amazon Web Service Security",
                "Integración con la Agencia Tributaria",
                "NO vendemos",
                "NO compartimos",
                "Historial de inicio de sesión y dispositivo",
            ),
        ),
    )
    for url, start, end, expected_hash, markers in documents:
        status, _, body = fetch(
            url, headers={"Accept": "text/html,application/xhtml+xml"}
        )
        if status != 200:
            raise ValueError(f"TaxDown official page returned {status}: {url}")
        core = section(normalize_html(body), start, end)
        if sha256(core.encode()) != expected_hash:
            raise ValueError(f"TaxDown official page changed: {url}")
        for marker in markers:
            if marker not in core:
                raise ValueError(f"{url} lost required marker {marker!r}")


def verify_remote() -> None:
    status, _, body = fetch(HEALTH_URL)
    if status != 200 or json.loads(body) != {"status": "ok"}:
        raise ValueError("TaxDown MCP health boundary changed")

    status, _, body = fetch(PROTECTED_RESOURCE_URL)
    protected = json.loads(body)
    if (
        status != 200
        or canonical_sha256(protected) != PROTECTED_RESOURCE_SHA256
    ):
        raise ValueError("TaxDown protected-resource metadata changed")
    if (
        protected.get("resource") != "https://mcp.taxdown.es"
        or protected.get("authorization_servers")
        != ["https://mcp.taxdown.es"]
        or protected.get("bearer_methods_supported") != ["header"]
        or protected.get("scopes_supported")
        != ["openid", "email", "profile"]
    ):
        raise ValueError("TaxDown protected-resource contract changed")

    status, _, body = fetch(AUTHORIZATION_SERVER_URL)
    authorization = json.loads(body)
    if (
        status != 200
        or canonical_sha256(authorization) != AUTHORIZATION_SERVER_SHA256
    ):
        raise ValueError("TaxDown authorization metadata changed")
    if (
        authorization.get("issuer")
        != (
            "https://cognito-idp.eu-west-1.amazonaws.com/"
            "eu-west-1_E2odVzNqe"
        )
        or authorization.get("authorization_endpoint")
        != "https://mcp.taxdown.es/oauth/authorize"
        or authorization.get("token_endpoint")
        != "https://mcp.taxdown.es/oauth2/token"
        or authorization.get("revocation_endpoint")
        != "https://auth.app.taxdown.es/oauth2/revoke"
        or authorization.get("registration_endpoint") != REGISTRATION_URL
        or authorization.get("code_challenge_methods_supported") != ["S256"]
        or authorization.get("token_endpoint_auth_methods_supported")
        != ["client_secret_basic", "client_secret_post"]
    ):
        raise ValueError("TaxDown authorization contract changed")

    initialize = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {
                "name": "ghast-taxdown-audit",
                "version": "1.0",
            },
        },
    }
    status, headers, body = fetch(
        MCP_URL,
        data=json.dumps(initialize).encode(),
        method="POST",
        headers={
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "MCP-Protocol-Version": "2025-06-18",
        },
    )
    challenge = headers.get("www-authenticate", "")
    boundary = json.loads(body)
    if (
        status != 401
        or PROTECTED_RESOURCE_URL not in challenge
        or canonical_sha256(boundary) != UNAUTHORIZED_CANONICAL_SHA256
    ):
        raise ValueError("TaxDown MCP anonymous boundary changed")


def registration_payload(redirect_uri: str) -> dict:
    return {
        "client_name": "Ghast TaxDown portability audit",
        "redirect_uris": [redirect_uri],
        "grant_types": ["authorization_code"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "client_secret_basic",
        "scope": "openid email profile",
    }


def verify_portability_blocker() -> None:
    cases = (
        (
            "http://localhost:3000/callback",
            LOCALHOST_REJECTION_SHA256,
        ),
        (
            "http://127.0.0.1:3000/callback",
            LOOPBACK_REJECTION_SHA256,
        ),
    )
    for redirect_uri, expected_hash in cases:
        status, _, body = fetch(
            REGISTRATION_URL,
            data=json.dumps(registration_payload(redirect_uri)).encode(),
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        response = json.loads(body)
        if (
            status != 400
            or canonical_sha256(response) != expected_hash
            or response.get("error") != "invalid_redirect_uri"
            or "https://claude.ai/api/mcp/auth_callback"
            not in response.get("error_description", "")
            or "https://claude.com/api/mcp/auth_callback"
            not in response.get("error_description", "")
            or "https://mcp.taxdown.es/oauth/callback"
            not in response.get("error_description", "")
        ):
            raise ValueError(
                "TaxDown independent-client registration behavior changed; "
                "re-audit portability"
            )


def inventory_hash(plugin: Path) -> str:
    entries = []
    for path in sorted(item for item in plugin.rglob("*") if item.is_file()):
        value = path.read_bytes()
        entries.append(
            f"{path.relative_to(plugin).as_posix()}\0{sha256(value)}\0{len(value)}"
        )
    return sha256("\n".join(entries).encode())


def verify_openai_snapshot(source: Path) -> None:
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if revision != EXPECTED_OPENAI_REVISION:
        raise ValueError(
            f"{source}: expected {EXPECTED_OPENAI_REVISION}, found {revision}"
        )

    plugin = source / "plugins/taxdown"
    actual_files = {
        path.relative_to(plugin).as_posix()
        for path in plugin.rglob("*")
        if path.is_file()
    }
    if actual_files != set(OPENAI_HASHES):
        raise ValueError("TaxDown Codex file inventory changed")
    for relative_path, expected_hash in OPENAI_HASHES.items():
        if sha256((plugin / relative_path).read_bytes()) != expected_hash:
            raise ValueError(f"TaxDown Codex evidence changed: {relative_path}")
    if inventory_hash(plugin) != OPENAI_INVENTORY_SHA256:
        raise ValueError("TaxDown Codex inventory hash changed")

    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    app = json.loads((plugin / ".app.json").read_text())
    interface = manifest.get("interface", {})
    if (
        manifest.get("name") != PLUGIN_ID
        or manifest.get("version") != "1.0.3"
        or manifest.get("author", {}).get("name") != "TAXDOWN S.L."
        or interface.get("developerName") != "TAXDOWN S.L."
        or interface.get("defaultPrompt")
        != ["Summarize the relevant Taxdown status or guidance"]
        or app.get("apps", {}).get(PLUGIN_ID, {}).get("id")
        != "asdk_app_6985e420a0c08191b0d2ef99895d2b53"
    ):
        raise ValueError("TaxDown Codex identity changed")
    description = re.sub(r"\s+", " ", interface.get("longDescription", "")).strip()
    for marker in (
        "dudas fiscales en España",
        "particulares como autónomos",
        "deducciones",
        "IRPF",
        "renta",
        "obligaciones fiscales",
        "respuestas claras y orientadas a tu caso",
    ):
        if marker not in description:
            raise ValueError(
                f"TaxDown Codex capability evidence is missing {marker!r}"
            )


def review() -> dict:
    return {
        "verificationStatus": "official-source-research-required",
        "officialDeveloper": "Tax Down S.L.",
        "officialRepository": None,
        "officialRevision": UPSTREAM_REVISION,
        "license": "UNVERIFIED",
        "licenseEvidence": [
            "TaxDown publishes an official hosted MCP but does not publish its "
            "server implementation, tax knowledge system, tool schemas, "
            "official client source, or an open-source license for those "
            "materials.",
            "TaxDown's current terms and legal notice reserve the platform, "
            "software, services, content, interfaces, marks, and related "
            "intellectual property; public or commercial copying, "
            "reproduction, transformation, or distribution requires prior "
            "written authorization.",
            "The MIT declaration in OpenAI's three-file marketplace snapshot "
            "does not license TaxDown's hosted MCP, Luz tax assistant, "
            "customer tax data, private app connector, service content, "
            "trademarks, logo, or marketplace artwork.",
            "No TaxDown code, tax corpus, schema, private credential, response, "
            "logo, icon, or service content is redistributed because no "
            "independently usable capability-equivalent Ghast plugin is "
            "published.",
        ],
        "officialityEvidence": [
            "TaxDown's official Luz page describes Spain's first free expert "
            "tax chat, instant answers, plain-language explanations, "
            "case-specific regulatory analysis, step-by-step guidance, and "
            "questions for individuals, investors, regional deductions, and "
            "self-employed users. Its pinned semantic core SHA-256 is "
            "a0e5964a0f9763985544e2327f74923fd032b9aed41cc4a95ec719d61211769f.",
            "The official MCP is reachable at "
            "https://mcp.taxdown.es/mcp and its health endpoint returned "
            "HTTP 200. Anonymous initialization returns the standard protected "
            "resource challenge and canonical HTTP 401 response SHA-256 "
            "da7512f66622c27c985f2324a7041dabe34fe3ff552d378c570be9a32e05e102.",
            "The official protected-resource metadata identifies "
            "https://mcp.taxdown.es, header bearer authentication, and "
            "openid, email, and profile scopes. Its canonical SHA-256 is "
            "452319f67349a529f6a8592ceaf3ac56a7b7b9236519ccea1c643750e1a7eb08.",
            "The authorization metadata publishes TaxDown authorization, "
            "token, revocation, userinfo, JWKS, and dynamic-registration "
            "endpoints, Cognito issuer, confidential client authentication, "
            "and PKCE S256. Its canonical SHA-256 is "
            "1ac920a76fceb876b8f8b847c95678afdd2d971bc3c93d677ccf1b6579f699d5.",
            "On August 14, 2026, disposable confidential registrations using "
            "TaxDown's own HTTPS callback and Claude's exact HTTPS callback "
            "returned HTTP 201. No returned client ID, secret, authorization "
            "code, token, login, or account data was retained.",
            "The registration service's error text claims any "
            "http://localhost:*/callback or /oauth/callback is allowed, but "
            "actual localhost and 127.0.0.1 registrations return "
            "invalid_redirect_uri. Their canonical response SHA-256 values "
            "are 03efda369924d0c3b04ec07ec503ede501e728303f903fadfebb7e78c193e093 "
            "and d67bf7d9b70569f18ea370b3c4e0b4b924973e8337af2612d59a1545b9b7f1de.",
            "TaxDown's general terms, updated February 10, 2026, describe tax "
            "return preparation, advisory services, explicit confirmation "
            "before filing, user-supplied information, API-assisted data "
            "access, and reserved platform rights. Their pinned core SHA-256 "
            "is 40e88ffabcb2c4fc761bcb5f990e84d006e58f7972c8e24ea8fc91bf92e3d51e.",
            "TaxDown's legal notice identifies Tax Down S.L., NIF B-88287164, "
            "reserves platform and software rights, limits ordinary content "
            "use to a domestic scope, and prohibits unauthorized access, "
            "security bypass, copying, reproduction, transformation, and "
            "distribution. Its pinned core SHA-256 is "
            "75b1eca7e62b09c0097ff8a72dd3024e6b4f431ac549df2f18ba42911d266a7e.",
            "TaxDown's security page documents encryption, firewalls, AWS, "
            "Agencia Tributaria integration, account-session history, login "
            "notifications, and restrictions on selling, sharing, or using "
            "data outside tax-return purposes. Its pinned core SHA-256 is "
            "b6799f80b96e9e56bfd6928c5c0f748ba10321e211b662f2a5d79bb70758ea1d.",
            "OpenAI's pinned snapshot identifies TAXDOWN S.L. as developer, "
            "maps private app ID "
            "asdk_app_6985e420a0c08191b0d2ef99895d2b53, and promises Spanish "
            "tax guidance for individuals and self-employed users covering "
            "deductions, IRPF, income tax, and obligations. Its complete "
            "inventory SHA-256 is "
            "59177fde896373afe8082670626e41083847e0b763d3fa96ff2bdc0e569449d1.",
        ],
        "codexCapabilities": [
            "Answer Spanish tax questions for individuals and self-employed "
            "users",
            "Explain deductions, IRPF, annual income tax, and tax obligations "
            "in clear language",
            "Orient guidance to the user's facts and summarize relevant "
            "TaxDown status or guidance through OpenAI's private app mapping",
        ],
        "ghastCapabilities": [
            "TaxDown's official hosted MCP and Luz product establish a "
            "developer-operated capability corresponding to the Codex app.",
            "The official MCP publishes standard resource and authorization "
            "metadata, but its current dynamic-registration policy does not "
            "provide a working callback for an independent Ghast client.",
            "No Ghast plugin is published until TaxDown accepts an independent "
            "client callback or supplies a supported registered client and "
            "documented onboarding path.",
        ],
        "capabilityRelationship": (
            "official-hosted-mcp-found-independent-client-oauth-callback-blocked"
        ),
        "limitations": [
            "The OpenAI app ID is a private marketplace mapping, not an MCP "
            "URL, OAuth client, client secret, access token, tool schema, or "
            "reusable Ghast authorization.",
            "The MCP registration endpoint accepts only a narrow set of exact "
            "HTTPS callbacks observed during the audit. Localhost and "
            "127.0.0.1 callbacks used by independent desktop or CLI clients "
            "are rejected despite the endpoint's contrary error text.",
            "TaxDown's OAuth server requires confidential-client "
            "authentication. Ghast must not reuse Claude, OpenAI, TaxDown, or "
            "another client's callback, client ID, or client secret.",
            "Authenticated tools/list and tax guidance were not exercised "
            "because no portable client registration and no user TaxDown "
            "account were supplied. Exact tool names, schemas, sources, "
            "personalization fields, entitlements, and limits remain "
            "server-controlled.",
            "No public TaxDown MCP source repository, SDK, OpenAPI contract, "
            "generic API key flow, or independent-client setup guide was "
            "located. The public app and marketing site are not substitute "
            "automation interfaces.",
            "Do not scrape, reverse engineer, replay, or wrap TaxDown's web "
            "application, account traffic, tax forms, internal APIs, or "
            "private marketplace integration to work around OAuth.",
            "Tax records can contain DNI/NIF, income, investments, bank data, "
            "family details, addresses, properties, employment, benefits, "
            "filing history, and Agencia Tributaria access data. Any future "
            "connector requires strict authorization, minimization, "
            "confidentiality, retention, and audit controls.",
            "Spanish tax law changes over time and depends on tax year, "
            "autonomous community, residence, facts, deadlines, and official "
            "interpretation. Generated guidance must be dated, sourced, "
            "verified, and reviewed by a qualified professional before filing "
            "or acting.",
            "No icon or package is generated while authentication remains "
            "blocked. TaxDown and OpenAI marketplace artwork is not "
            "redistributed.",
            "Do not create plugins/taxdown until TaxDown supplies a working "
            "independent callback or registered-client path, authenticated "
            "schemas establish capability coverage, and adapter and artwork "
            "rights are sufficient.",
        ],
        "verification": [
            "python3 scripts/audit-taxdown-plugin.py --openai-source "
            "../openai-plugins",
            "Verify the official Luz, terms, legal-notice, and security page "
            "cores with SHA-256 "
            "a0e5964a0f9763985544e2327f74923fd032b9aed41cc4a95ec719d61211769f, "
            "40e88ffabcb2c4fc761bcb5f990e84d006e58f7972c8e24ea8fc91bf92e3d51e, "
            "75b1eca7e62b09c0097ff8a72dd3024e6b4f431ac549df2f18ba42911d266a7e, "
            "and b6799f80b96e9e56bfd6928c5c0f748ba10321e211b662f2a5d79bb70758ea1d",
            "Verify the MCP health route, protected-resource and authorization "
            "metadata hashes, Cognito issuer, endpoints, scopes, confidential "
            "clients, and PKCE S256",
            "Probe anonymous MCP initialization and require HTTP 401, the "
            "official protected-resource challenge, and canonical body hash "
            "da7512f66622c27c985f2324a7041dabe34fe3ff552d378c570be9a32e05e102",
            "Submit only non-creating localhost and 127.0.0.1 registration "
            "probes and require the pinned invalid_redirect_uri responses; "
            "do not repeatedly create supported client registrations",
            "Treat the August 14, 2026 exact-HTTPS registration checks as "
            "manual evidence only; no returned client value was retained",
            "Verify OpenAI snapshot "
            "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9, all three file hashes, "
            "complete inventory hash, developer identity, private app ID, "
            "prompt, and Spanish tax-guidance markers",
            "Confirm plugins/taxdown and packages/taxdown.zip remain absent "
            "while independent client authentication, schema, license, and "
            "artwork blockers remain",
            "python3 scripts/audit-third-party-plugins.py --source "
            "../openai-plugins",
            "python3 scripts/validate-ghast-repository.py",
        ],
    }


def update_reviews() -> None:
    data = json.loads(REVIEWS_PATH.read_text())
    data.setdefault("plugins", {})[PLUGIN_ID] = review()
    REVIEWS_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    )


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main() -> int:
    args = parse_args()
    source = args.openai_source.resolve()
    verify_official_pages()
    verify_remote()
    verify_portability_blocker()
    verify_openai_snapshot(source)
    if Path("plugins/taxdown").exists() or Path("packages/taxdown.zip").exists():
        raise ValueError(
            "TaxDown must remain unpublished until it supplies a working "
            "independent OAuth callback or registered client, authenticated "
            "tool schemas, and sufficient adapter and artwork rights"
        )
    update_reviews()
    run(
        [
            "python3",
            "scripts/audit-third-party-plugins.py",
            "--source",
            str(source),
        ]
    )
    run(["python3", "scripts/validate-ghast-repository.py"])
    print("verified TaxDown official MCP and independent-client OAuth blocker")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
