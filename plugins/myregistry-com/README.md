# myregistry-com

Find public wedding, baby, and general gift-list registries through
MyRegistry.com's official Registry API.

## Official interface

MyRegistry's public developer documentation publishes `GetRegistries2` at
`https://api.myregistry.com/RegistryApi/1/0/json/GetRegistries2`. The endpoint
requires first and last name, accepts optional city, state, country, and
registry-type filters, and returns registrant, co-registrant, type, event
date, location, and registry URL. Authentication uses a partner
`developerKey`.

The developer index, integration guide, Registry API overview,
`GetRegistries2` OpenAPI page, and Merchant API server-side guidance are
pinned by `scripts/import-myregistry-plugin.py`. On August 14, 2026, an
anonymous request returned HTTP 417 with `Developer Key is not valid.`,
confirming the independent official API boundary without using the Codex
private app connector.

## Capability comparison

- Codex: find relevant MyRegistry.com registry details through private app ID
  `asdk_app_69c1b82faf2c81919e80900a7443dcfd`.
- Ghast: search the official public partner API by exact first and last name,
  narrow by city, state, country, or wedding/baby/gift-list type, and return
  the documented registry identity, date, location, and URL fields.
- Ghast intentionally excludes account access, gift-item retrieval, purchase
  marking, shipping addresses, registry creation, and any web scraping.

## Authentication and licensing

Set `MYREGISTRY_DEVELOPER_KEY` in the local host environment. API access,
Merchant Agreement acceptance, partner eligibility, data permissions,
service limits, and key issuance remain controlled by MyRegistry.com. An
ordinary consumer account may not include developer access.

The bundled standard-library adapter has SHA-256 `fc2d2b42924ac064ce6291e0a57fb7e20d302a2c0de1ead2ae5432a7f41b245e`. The MIT
license covers only the Ghast-authored adapter, workflow, metadata,
documentation, and generic gift-search icon. It does not license or
redistribute MyRegistry's service, private connector, API key, customer data,
developer documentation, web content, logos, or trademarks.
