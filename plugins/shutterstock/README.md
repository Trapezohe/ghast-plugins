# shutterstock

Search Shutterstock's official stock libraries and compare watermarked media
previews without licensing or downloading assets.

## Official source

Shutterstock maintains the MIT-licensed `shutterstock-cli` repository. Release
`v1.5.2` maps image, video, music, sound-effect, and bulk-image search commands
to the official public API. The current API reference is `v1.5.3`; its later
change concerns image license-history metadata and does not change these
search endpoints.

This package uses a small, independently authored standard-library client
instead of bundling the official CLI's `requests`, `click`, and `pygments`
dependencies. It calls the same official endpoints:

- `GET /v2/images/search`
- `GET /v2/videos/search`
- `GET /v2/audio/search`
- `GET /v2/sfx/search`
- `POST /v2/bulk_search/images`

## Capability comparison

- Codex: find candidate images, videos, music, and sound effects, including
  grouped image searches, and return watermarked previews with basic metadata.
- Ghast: perform the same read-only searches through Shutterstock's public API
  with self-service application credentials, preserve full official response
  metadata, and guide preview comparison.
- Both deliberately exclude generation, editing, licensing, purchasing, and
  downloading. The Ghast package exposes no write or licensing command.

## Authentication and verification

Create a Shutterstock API application, then set
`SHUTTERSTOCK_API_TOKEN` or both `SHUTTERSTOCK_KEY` and
`SHUTTERSTOCK_SECRET`. Credentials remain outside the package and command
arguments.

The importer pins OpenAI's marketplace evidence, Shutterstock CLI `v1.5.2`,
the official CLI license and search endpoint mappings, the current official
API reference, and the live authentication boundary for all five search
surfaces. The adapter is tested without network access for parameter,
authentication, and output behavior. Authenticated searches were not run
because no Shutterstock credential was supplied.

The MIT license in this package covers the Ghast-authored client, guidance,
metadata, documentation, and generic stock-media icon. Shutterstock's
official CLI license is included separately in `UPSTREAM_LICENSE.md`. No
Shutterstock logo, marketplace artwork, API credential, preview, asset,
customer data, or official CLI source is redistributed. API access, plans,
content availability, previews, and media licenses remain governed by
Shutterstock.
