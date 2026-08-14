#!/usr/bin/env python3
"""Read Zoho CRM organization and user data through Zoho's official v8 SDK."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path


WHEELS = {
    "certifi-2025.8.3-py3-none-any.whl": "f6c12493cfb1b06ba2ff328595af9350c65d6644968e5d3a2ffd78699af217a5",
    "charset_normalizer-3.4.3-py3-none-any.whl": "ce571ab16d890d23b5c278547ba694193a45011ff86a9162a71307ed9f86759a",
    "idna-3.10-py3-none-any.whl": "946d195a0d259cbba61165e88e65941f16e9b36ea6ddb97f00452bae8b1287d3",
    "python_dateutil-2.8.2-py2.py3-none-any.whl": "961d03dc3453ebbc59dbdea9e4e11c5651520a876d0f4db161e8674aae935da9",
    "requests-2.32.5-py3-none-any.whl": "2462f94637a34fd532264295e186976db0f5d453d1cdd31473c85a6a161affb6",
    "six-1.17.0-py2.py3-none-any.whl": "4721f391ed90541fddacab5acf947aa0d3dc7d27b2e1e8eda2be8970586c3274",
    "urllib3-2.6.0-py3-none-any.whl": "c90f7a39f716c572c4e3e58509581ebd83f9b59cced005b7db7ad2d22b0db99f",
    "zohocrmsdk8_0-7.0.0-py2.py3-none-any.whl": "0a12dc153a7ac063fafed2834dc91e93d151bd0c58fc5f8003ebcad772b915a1"
}
USER_TYPES = (
    "AllUsers",
    "ActiveUsers",
    "DeactiveUsers",
    "ConfirmedUsers",
    "NotConfirmedUsers",
    "DeletedUsers",
    "ActiveConfirmedUsers",
    "AdminUsers",
    "ActiveConfirmedAdmins",
    "CurrentUser",
)


def fail(message: str) -> None:
    print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_extract(archive: zipfile.ZipFile, target: Path) -> None:
    root = target.resolve()
    for member in archive.infolist():
        destination = (target / member.filename).resolve()
        if root not in destination.parents and destination != root:
            fail(f"Unsafe wheel member: {member.filename}")
    archive.extractall(target)


def load_official_sdk() -> tempfile.TemporaryDirectory:
    plugin_root = Path(__file__).resolve().parents[3]
    vendor = plugin_root / "vendor"
    missing = [name for name in WHEELS if not (vendor / name).is_file()]
    if missing:
        fail("Missing bundled official wheel(s): " + ", ".join(missing))
    temporary = tempfile.TemporaryDirectory(prefix="ghast-zoho-sdk-")
    target = Path(temporary.name)
    for name, expected in WHEELS.items():
        wheel = vendor / name
        if sha256(wheel) != expected:
            temporary.cleanup()
            fail(f"Bundled wheel hash mismatch: {name}")
        with zipfile.ZipFile(wheel) as archive:
            safe_extract(archive, target)
    sys.path.insert(0, str(target))
    return temporary


def clean_secret(name: str) -> str | None:
    value = os.environ.get(name)
    if value is None:
        return None
    if not value or any(char in value for char in "\x00\r\n"):
        fail(f"{name} is empty or contains forbidden control characters")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--data-center",
        choices=("us", "eu", "in", "au", "jp", "ca", "cn", "sa"),
        default=os.environ.get("ZOHO_CRM_DATA_CENTER", "us").lower(),
    )
    parser.add_argument(
        "--environment",
        choices=("production", "sandbox", "developer"),
        default=os.environ.get("ZOHO_CRM_ENVIRONMENT", "production").lower(),
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("org")
    users = subparsers.add_parser("users")
    users.add_argument("--type", choices=USER_TYPES, default="ActiveUsers")
    users.add_argument("--page", type=int, default=1)
    users.add_argument("--per-page", type=int, default=200)
    users.add_argument("--ids")
    user = subparsers.add_parser("user")
    user.add_argument("--id", required=True)
    args = parser.parse_args()
    if not args.self_test and not args.command:
        parser.error("a command is required")
    if args.command == "users":
        if args.page < 1:
            parser.error("--page must be at least 1")
        if not 1 <= args.per_page <= 200:
            parser.error("--per-page must be between 1 and 200")
        if args.ids:
            values = args.ids.split(",")
            if len(values) > 100 or any(not value.isdigit() for value in values):
                parser.error("--ids accepts up to 100 comma-separated numeric IDs")
    if args.command == "user" and not args.id.isdigit():
        parser.error("--id must be numeric")
    return args


def simple(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): simple(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [simple(item) for item in value]
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    getter = getattr(value, "get_value", None)
    if callable(getter):
        return simple(getter())
    return str(value)


def read(obj, method: str):
    getter = getattr(obj, method, None)
    return simple(getter()) if callable(getter) else None


def named_ref(obj):
    if obj is None:
        return None
    return {
        "id": read(obj, "get_id"),
        "name": read(obj, "get_name") or read(obj, "get_full_name"),
    }


def initialize(args):
    from zohocrmsdk.src.com.zoho.api.authenticator import OAuthToken
    from zohocrmsdk.src.com.zoho.api.authenticator.store.token_store import (
        TokenStore,
    )
    from zohocrmsdk.src.com.zoho.crm.api import Initializer
    from zohocrmsdk.src.com.zoho.crm.api.dc import (
        AUDataCenter,
        CADataCenter,
        CNDataCenter,
        EUDataCenter,
        INDataCenter,
        JPDataCenter,
        SADataCenter,
        USDataCenter,
    )

    class MemoryStore(TokenStore):
        def __init__(self):
            self.token = None

        def find_token(self, token):
            return self.token

        def save_token(self, token):
            self.token = token

        def delete_token(self, token_id):
            self.token = None

        def get_tokens(self):
            return [self.token] if self.token is not None else []

        def delete_tokens(self):
            self.token = None

        def find_token_by_id(self, token_id):
            return self.token

    centers = {
        "us": USDataCenter,
        "eu": EUDataCenter,
        "in": INDataCenter,
        "au": AUDataCenter,
        "jp": JPDataCenter,
        "ca": CADataCenter,
        "cn": CNDataCenter,
        "sa": SADataCenter,
    }
    environment = getattr(centers[args.data_center], args.environment.upper())()
    access_token = clean_secret("ZOHO_CRM_ACCESS_TOKEN")
    if access_token:
        token = OAuthToken(access_token=access_token, find_user=False)
    else:
        client_id = clean_secret("ZOHO_CRM_CLIENT_ID")
        client_secret = clean_secret("ZOHO_CRM_CLIENT_SECRET")
        refresh_token = clean_secret("ZOHO_CRM_REFRESH_TOKEN")
        missing = [
            name
            for name, value in (
                ("ZOHO_CRM_CLIENT_ID", client_id),
                ("ZOHO_CRM_CLIENT_SECRET", client_secret),
                ("ZOHO_CRM_REFRESH_TOKEN", refresh_token),
            )
            if value is None
        ]
        if missing:
            fail(
                "Set ZOHO_CRM_ACCESS_TOKEN, or set all of "
                "ZOHO_CRM_CLIENT_ID, ZOHO_CRM_CLIENT_SECRET, and "
                "ZOHO_CRM_REFRESH_TOKEN. Missing: " + ", ".join(missing)
            )
        token = OAuthToken(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            find_user=False,
        )
    resource = tempfile.TemporaryDirectory(prefix="ghast-zoho-resource-")
    Initializer.initialize(
        environment,
        token,
        store=MemoryStore(),
        resource_path=resource.name,
    )
    return resource


def api_error(response_object) -> dict:
    details = read(response_object, "get_details")
    if not isinstance(details, dict):
        details = {"value": details} if details is not None else {}
    return {
        "status": read(response_object, "get_status"),
        "code": read(response_object, "get_code"),
        "message": read(response_object, "get_message"),
        "details": details,
    }


def user_row(user) -> dict:
    return {
        "id": read(user, "get_id"),
        "full_name": read(user, "get_full_name") or read(user, "get_name"),
        "first_name": read(user, "get_first_name"),
        "last_name": read(user, "get_last_name"),
        "email": read(user, "get_email"),
        "status": read(user, "get_status"),
        "confirm": read(user, "get_confirm"),
        "role": named_ref(getattr(user, "get_role")()),
        "profile": named_ref(getattr(user, "get_profile")()),
        "reporting_to": named_ref(getattr(user, "get_reporting_to")()),
        "time_zone": read(user, "get_time_zone"),
        "locale": read(user, "get_locale"),
        "language": read(user, "get_language"),
        "created_time": read(user, "get_created_time"),
        "modified_time": read(user, "get_modified_time"),
    }


def list_users(args) -> dict:
    from zohocrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
    from zohocrmsdk.src.com.zoho.crm.api.users import (
        APIException,
        GetUsersParam,
        ResponseWrapper,
        UsersOperations,
    )
    from zohocrmsdk.src.com.zoho.crm.api.util import Choice

    params = ParameterMap()
    params.add(GetUsersParam.type, Choice(args.type))
    params.add(GetUsersParam.page, args.page)
    params.add(GetUsersParam.per_page, args.per_page)
    if args.ids:
        params.add(GetUsersParam.ids, args.ids)
    response = UsersOperations().get_users(params, HeaderMap())
    if response is None:
        fail("Zoho SDK returned no response")
    status = response.get_status_code()
    obj = response.get_object()
    if isinstance(obj, APIException):
        return {"status_code": status, "error": api_error(obj)}
    if not isinstance(obj, ResponseWrapper):
        return {"status_code": status, "users": []}
    info = obj.get_info()
    return {
        "status_code": status,
        "users": [user_row(user) for user in (obj.get_users() or [])],
        "page": {
            "page": read(info, "get_page"),
            "per_page": read(info, "get_per_page"),
            "count": read(info, "get_count"),
            "more_records": read(info, "get_more_records"),
        } if info is not None else None,
    }


def get_user(args) -> dict:
    from zohocrmsdk.src.com.zoho.crm.api import HeaderMap
    from zohocrmsdk.src.com.zoho.crm.api.users import (
        APIException,
        ResponseWrapper,
        UsersOperations,
    )

    response = UsersOperations().get_user(int(args.id), HeaderMap())
    if response is None:
        fail("Zoho SDK returned no response")
    status = response.get_status_code()
    obj = response.get_object()
    if isinstance(obj, APIException):
        return {"status_code": status, "error": api_error(obj)}
    users = obj.get_users() if isinstance(obj, ResponseWrapper) else []
    return {
        "status_code": status,
        "user": user_row(users[0]) if users else None,
    }


def org_row(org) -> dict:
    license_details = getattr(org, "get_license_details")()
    return {
        "id": read(org, "get_id"),
        "company_name": read(org, "get_company_name"),
        "alias": read(org, "get_alias"),
        "type": read(org, "get_type"),
        "domain_name": read(org, "get_domain_name"),
        "country": read(org, "get_country"),
        "country_code": read(org, "get_country_code"),
        "time_zone": read(org, "get_time_zone"),
        "currency": read(org, "get_currency"),
        "currency_symbol": read(org, "get_currency_symbol"),
        "iso_code": read(org, "get_iso_code"),
        "employee_count": read(org, "get_employee_count"),
        "primary_email": read(org, "get_primary_email"),
        "website": read(org, "get_website"),
        "privacy_settings": read(org, "get_privacy_settings"),
        "hipaa_compliance_enabled": read(
            org, "get_hipaa_compliance_enabled"
        ),
        "multi_currency_enabled": read(org, "get_mc_status"),
        "translation_enabled": read(org, "get_translation_enabled"),
        "created_time": read(org, "get_created_time"),
        "license": {
            "paid": read(license_details, "get_paid"),
            "paid_type": read(license_details, "get_paid_type"),
            "paid_expiry": read(license_details, "get_paid_expiry"),
            "trial_type": read(license_details, "get_trial_type"),
            "trial_expiry": read(license_details, "get_trial_expiry"),
            "users_purchased": read(
                license_details, "get_users_license_purchased"
            ),
        } if license_details is not None else None,
    }


def get_org() -> dict:
    from zohocrmsdk.src.com.zoho.crm.api.org import (
        APIException,
        OrgOperations,
        ResponseWrapper,
    )

    response = OrgOperations().get_organization()
    if response is None:
        fail("Zoho SDK returned no response")
    status = response.get_status_code()
    obj = response.get_object()
    if isinstance(obj, APIException):
        return {"status_code": status, "error": api_error(obj)}
    orgs = obj.get_org() if isinstance(obj, ResponseWrapper) else []
    return {
        "status_code": status,
        "organizations": [org_row(org) for org in (orgs or [])],
    }


def main() -> int:
    args = parse_args()
    sdk_temp = load_official_sdk()
    try:
        import requests
        import zohocrmsdk

        if args.self_test:
            print(json.dumps({
                "ok": True,
                "sdk": "zohocrmsdk8_0 7.0.0",
                "requests": requests.__version__,
                "wheel_count": len(WHEELS),
            }, indent=2))
            return 0
        resource = initialize(args)
        try:
            if args.command == "org":
                result = get_org()
            elif args.command == "users":
                result = list_users(args)
            else:
                result = get_user(args)
        finally:
            resource.cleanup()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if "error" not in result else 1
    except SystemExit:
        raise
    except Exception as exc:
        fail(f"Zoho CRM SDK request failed: {type(exc).__name__}: {exc}")
    finally:
        sdk_temp.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
