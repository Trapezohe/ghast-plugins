# skywatch

Search orderable satellite imagery, compare scene pricing, and browse
satellites, sensors, providers, and products through SkyWatch's official
hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It does not copy or
redistribute SkyWatch's hosted MCP implementation, imagery catalog, private
Codex connector, or marketplace artwork.

The adapter is pinned to SkyWatch's official MCP documentation. Its SHA-256 is
`f4ed1fbadb7c6190d3fa399cd694f0d7456e7c653f33535c4933716fde023a05`. The client-integration documentation has SHA-256
`a16e47fecde3dcb2e73ae339acdacc22695f0da76183ea8971546db70b837655`. The live official `tools/list` response is
pinned at canonical JSON SHA-256
`c6b9fe481f168d9066778500895fa233161bfe94436dd2f88dc9234448ce6123`.

## Ghast compatibility

- Ghast connects directly to `https://api.skywatch.co/mcp` using Streamable HTTP.
  SkyWatch provides guest access, so no API key or account setup is required.
- Four read-only tools cover archive-imagery search, archive or tasking price
  estimates, satellite and sensor browsing, and product-offering discovery.
- Search supports natural-language locations, coordinates, bounding boxes,
  GeoJSON, dates, cloud cover, coverage, resolution, data type, sorting, and
  comparison modes, with direct SkyWatch Explore links for viewing or ordering.
- A live verification search for the Golden Gate Bridge returned current
  orderable scenes, provider and resolution data, per-scene prices, and an
  Explore link, fully covering the Codex app's example and description.
- A generic satellite-search icon is used because no licensed catalog icon is
  included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
SkyWatch's hosted service, imagery, prices, providers, Explore ordering,
permissions, trademarks, and terms remain controlled by SkyWatch.
