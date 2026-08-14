# zoho

Manage Zoho CRM through Zoho's four official hosted MCP servers. A bundled
read-only adapter over Zoho's official Apache-2.0 Python SDK fills the Codex
organization and user access-audit capability that the hosted MCP OAuth scopes
do not currently expose.

## Official sources

- Zoho CRM MCP overview, raw SHA-256 `c1e19ceac01d59e7d12aea921cfcb61930f85f03a551df3ab35aa2c8c4287237`.
- Zoho CRM VS Code setup, raw SHA-256 `fdda793cfdd72fb8a9ab394d8326914a53fe1f0801c71fb1ef91d45aabcbb82d`.
- Zoho CRM Claude setup, raw SHA-256 `86aca1f932b534099b0d478036d670a3f74f45c3e06b0bfd34b42ccbb7ce3b7e`.
- Zoho CRM Users API v8, raw SHA-256 `7f4a7939702cefb97a875d32daf148754100cb89ad16a62d987dccba77a7be5a`.
- Zoho CRM Organization API v8, raw SHA-256 `66d54af619ba140c199d9f7cc079fd306d72de49dff2639bc27c5c33f40a8f17`.
- Zoho official Python SDK: `https://github.com/zoho/zohocrm-python-sdk-8.0` at `7dbcafa4f794a5c07b92cfcd6be6ca2d903e2296`, Git tree
  `b3b7f3ca3a1270d2458f3101164da08abd87b836`, 15578 files, Apache-2.0.
- Codex capability snapshot: `github.com/openai/plugins` at
  `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`, three-file inventory SHA-256
  `152039eaa680f38a6fb42944e14055c2d183249c42b8dfa238a52bba0c566767`.

## Portable hosted MCP

Zoho documents four pre-built Streamable HTTP servers:

- `zoho-crm-data-insights`: `https://zoho-crm-data-insights-60065097786.zohomcp.in/mcp/d17dfe13292e0414a929516bb8f8e797/message`
- `zoho-crm-data-operations`: `https://zoho-crm-data-operations-60065097786.zohomcp.in/mcp/fe46ddbc48fec3713c8754cea8ec9ac5/message`
- `zoho-crm-module-customization`: `https://zoho-crm-module-customization-60065097786.zohomcp.in/mcp/8057776f5d548a33b892c533d4278d17/message`
- `zoho-crm-automation`: `https://zoho-crm-automation-60065097786.zohomcp.in/mcp/c139be028c224f75a9077e6473a62f3b/message`

Each endpoint returned HTTP 401 with its own standards-based protected-resource
challenge. The four OAuth servers publish dynamic client registration,
authorization-code and refresh-token grants, public clients, and PKCE S256.
On August 14, 2026, four disposable public clients registered with HTTP 200
and no client secret, then redirected to Zoho's official MCP login route. No
Zoho login, authorization code, access token, CRM account, record, or user data
was obtained or retained.

The current protected-resource scope counts are 22 for Data Insights, 83 for
Data Operations, 12 for Module Customization, and 7 for Automation. The active
skill therefore prefers the read-only Data Insights server and requires exact
confirmation for every state-changing operation.

## Official SDK supplement

The Codex snapshot asks for organization settings and users. The hosted MCP
scope lists do not include `ZohoCRM.org.READ` or `ZohoCRM.users.READ`, while
Zoho's official v8 API and SDK expose both read operations. Ghast includes a
small read-only adapter that invokes only the official SDK's organization and
user operations.

The adapter stores refreshed tokens only in memory and SDK resources only in
temporary directories. It reads credentials from environment variables and
never runs pip at use time. These official wheels are bundled and hash checked:

- `zohocrmsdk8_0-7.0.0-py2.py3-none-any.whl` SHA-256 `0a12dc153a7ac063fafed2834dc91e93d151bd0c58fc5f8003ebcad772b915a1`
- `requests-2.32.5-py3-none-any.whl` SHA-256 `2462f94637a34fd532264295e186976db0f5d453d1cdd31473c85a6a161affb6`
- `urllib3-2.6.0-py3-none-any.whl` SHA-256 `c90f7a39f716c572c4e3e58509581ebd83f9b59cced005b7db7ad2d22b0db99f`
- `python_dateutil-2.8.2-py2.py3-none-any.whl` SHA-256 `961d03dc3453ebbc59dbdea9e4e11c5651520a876d0f4db161e8674aae935da9`
- `certifi-2025.8.3-py3-none-any.whl` SHA-256 `f6c12493cfb1b06ba2ff328595af9350c65d6644968e5d3a2ffd78699af217a5`
- `charset_normalizer-3.4.3-py3-none-any.whl` SHA-256 `ce571ab16d890d23b5c278547ba694193a45011ff86a9162a71307ed9f86759a`
- `idna-3.10-py3-none-any.whl` SHA-256 `946d195a0d259cbba61165e88e65941f16e9b36ea6ddb97f00452bae8b1287d3`
- `six-1.17.0-py2.py3-none-any.whl` SHA-256 `4721f391ed90541fddacab5acf947aa0d3dc7d27b2e1e8eda2be8970586c3274`

Run `python3 <skill-dir>/scripts/zoho_crm_admin_read.py --self-test` to verify
the bundled runtime without credentials or network access to Zoho CRM.

## Capability comparison

- Codex open-deal and account/contact prompts are covered by the official Data
  Insights server, including COQL, module and field discovery, filtering,
  sorting, grouping, pagination, and record retrieval.
- Codex organization and user access-audit reads are covered by Zoho's official
  SDK and v8 `/org` and `/users` APIs with separately managed read scopes.
- Zoho's current hosted MCP adds official record CRUD and bulk operations,
  related records, custom modules and fields, layouts, workflow rules, rule
  ordering, workflow tasks, and workflow configuration.
- This is an equivalent hybrid official MCP plus official SDK implementation,
  with additional official write, customization, and automation capabilities.

## Limits

A Zoho CRM account, correct organization, data center, environment, OAuth
authorization, user permissions, role, profile, edition, feature access, API
credits, and service limits remain user-managed. Authenticated MCP tool schemas
and live CRM operations were not run because no Zoho CRM account was supplied.

The SDK credentials are separate from the hosted MCP OAuth sessions. Access and
refresh tokens are data-center and environment specific. The plugin does not
create OAuth clients, obtain refresh tokens, or store credentials for users.

The hosted MCP implementation is operated by Zoho and is not redistributed.
The plugin's Apache-2.0 license covers Zoho's public SDK and the Ghast adapter
files. Bundled dependency wheels retain their Apache-2.0, MIT, MPL-2.0,
BSD-3-Clause, or dual Apache/BSD license texts under `licenses/`. These
licenses do not cover Zoho's hosted service, CRM data, private Codex connector,
trademarks, or marketplace artwork. A generic multi-color CRM icon is used.
