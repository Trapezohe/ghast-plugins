---
name: myregistry-com
description: >-
  Find public wedding, baby, and gift-list registries through MyRegistry.com's
  official partner Registry API.
---

# MyRegistry.com

Use the bundled `scripts/myregistry_api.py` read-only adapter over
MyRegistry.com's official `GetRegistries2` Registry API. This is a Ghast
adapter to the official service, not MyRegistry-authored source or an MCP
server.

## Access

- The API is for authorized MyRegistry retail partners and requires a
  MyRegistry-issued `developerKey`. A normal consumer registry account does
  not necessarily include API access.
- Store the key as `MYREGISTRY_DEVELOPER_KEY` in the Ghast host environment.
  Never request it in chat, put it in a command argument, print it, log it,
  save it in a project file, or commit it.
- The official API requires the key in the HTTPS query string. Use only the
  fixed endpoint in the adapter and avoid proxy, shell, or debug logging that
  records full request URLs.

Resolve this skill's directory as `SKILL_DIR`, then:

```bash
MYREGISTRY_API="$SKILL_DIR/scripts/myregistry_api.py"
python3 "$MYREGISTRY_API" auth-check
```

`auth-check` checks local configuration only. It does not send a registry
query or expose the key.

## Find a registry

The official API requires both first and last name:

```bash
python3 "$MYREGISTRY_API" search \
  --first-name Jamie \
  --last-name Example \
  --state NY \
  --registry-type wedding
```

Optional filters are `--city`, `--state`, `--country`, and
`--registry-type wedding|baby|gift-list`. Use every known filter before
searching. For a common name or a potentially broad match, show the exact
search scope and obtain explicit user confirmation before the request.

The result contains only the official lookup fields: registrant,
co-registrant, registry type, event date, location, and public registry URL.
The local `--limit` defaults to 25 and only limits returned output; the
official endpoint does not document server-side pagination.

## Privacy and safety

- Registry results can reveal names, relationships, event types, event dates,
  and approximate locations. Retrieve only the minimum needed for the user's
  stated gifting purpose.
- Do not bulk enumerate names, build datasets, infer pregnancy, marital
  status, religion, sexuality, finances, home address, or other sensitive
  attributes, or use registry data for advertising, outreach, surveillance,
  eligibility, employment, housing, credit, insurance, or law enforcement.
- Do not disclose a match to a new recipient without authorization. When
  multiple people match, present minimal disambiguating fields and ask the
  user to choose rather than guessing.
- A returned result does not prove identity, relationship, event status, or
  current accuracy. Preserve the returned date and location exactly and state
  uncertainty.
- Do not scrape or automatically open returned registry pages. MyRegistry's
  public-site terms prohibit automated access without express permission.
  Use only the partner API covered by the user's developer key and Merchant
  Agreement.
- Password-protected registries, gift contents, purchase state, shipping
  addresses, member accounts, and registry mutations are outside this
  plugin's capability. Never try to bypass those boundaries.
- Do not automatically retry `401`, `403`, `417`, `429`, timeout, or ambiguous
  responses. Report the error without exposing the request URL or key.
