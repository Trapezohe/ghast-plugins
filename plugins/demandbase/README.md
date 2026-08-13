# demandbase

Research internal accounts and people, global companies and contacts,
account-level Intent, Buying Groups, opportunities, engagement, and
meeting-ready account briefs through Demandbase's official hosted MCP.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, metadata, and a generic GTM-research icon. It
does not redistribute Demandbase's hosted implementation, private Codex
connector, OAuth credentials, customer data, proprietary B2B intelligence,
official documentation text, trademarks, branded artwork, or marketplace
icons.

Demandbase's official MCP overview, custom-client guide, agent guidance,
credit guide, VS Code guide, and documentation index are pinned at raw
SHA-256 values `f41df5ef1529fdba14b31291f4ec5451f9a2cad7e6cf061916d6a41131505b41`,
`5ae757d63c7bde59650bdd74968ebe5318c4b47ec7f51c3155663c264953b1c2`,
`2662115095c3fe8c09190e5884c1284626fb666054fd8fe6150287fe7ffdffee`,
`f9bad376ffddb3cb4e5d6a67eafb4298ffd21b793a7e8f0107a734a1a0d63400`,
`1281d1b03daeb3883a7781340b92e6e44b43a153e0e6c43fa201f0ba18e01cf1`, and
`b41aeedced01687c464c2bb9c72e3af0e6b275cae744def6eba7c041c0f769a2`.

The documented ordered six-capability inventory is pinned at canonical JSON
SHA-256 `08e5b6428096ed366889f7c496108758b28fdf051d916636ac6e846c4811d8c1`. Protected-resource and
authorization-server metadata are pinned at canonical JSON SHA-256
`4b60860182132d35c24c8dc67e3bd8b4778cf03050f26d060f9e0088f27e7ef0` and `974b2f8f4944a95729ba1c680dc3580521a44d0265d75227a89caa4871d8c042`.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app ID or
marketplace artwork.

## Ghast compatibility

- Ghast connects directly to `https://gateway.demandbase.com/mcp/servers/db-mcp` over Streamable HTTP.
  Demandbase also publishes this exact URL for VS Code and documents custom
  MCP clients.
- The current official overview lists six capabilities for internal account
  search, internal person search, global company search, global contact
  search, tenant reference data, and Account Brief. Authenticated
  `tools/list` remains authoritative for exact machine names and schemas.
- This fully covers the Codex 1P and 3P surface for company and contact
  discovery, firmographics, technographics, corporate hierarchy, news,
  leadership profiles, CRM accounts and people, engagement, MQA-style
  qualification context, and pipeline opportunities.
- The public service additionally documents account-level Intent, Buying
  Group configuration and coverage, net-new contacts not represented in CRM,
  and consolidated Account 360, meeting, opportunity, renewal, and expansion
  briefs.
- All documented capabilities are read-only. Account Brief does not create
  tasks, update opportunities, send messages, or add Buying Group members;
  net-new contact discovery does not import records into CRM.
- Demandbase OAuth uses Dynamic Client Registration, authorization code,
  public clients, and PKCE S256. Unlike open-callback services, it requires a
  hosted HTTPS callback and manual Demandbase Support allowlisting of the
  exact callback for the generated client ID.
- On August 13, 2026, the registration endpoint returned the same public
  client ID for multiple disposable audit payloads and issued no secret or
  registration-management credential. The authorization endpoint then
  rejected an unallowlisted loopback callback with HTTP 400. Registration
  success alone must not be treated as completed OAuth setup.
- Missing and invalid Bearer initialize requests returned HTTP 401 with the
  official protected-resource challenge and identical body SHA-256
  `6ebd2775e150f6fb7b2a69d2690d75e1541eb2ec2309570b00dc9139c6ed0de5`.
- Demandbase must enable MCP for the organization. Administrators can grant
  Full Access, No Access, or Limited Access to Demandbase Data, Your Data, or
  both. Effective fields and tools depend on the user, tenant, product
  licenses, configuration, CRM data, permission set, and credit balance.
- Usage costs one shared organization credit per returned record. Results
  default to five records per page and can request up to 100. The included
  skill requires bounded limits and confirmation before material multi-record
  or multi-tool retrieval.
- Demandbase currently documents English support. Authenticated tools/list,
  private account or contact data, credit consumption, and real searches were
  not exercised because no Demandbase account or customer data was used.
- A generic GTM-research icon is used because no licensed Demandbase catalog
  artwork is redistributed.

The MIT license in this package applies only to the independently authored
Ghast adapter. Demandbase accounts, licenses, credits, hosted behavior,
customer and global data, permissions, trademarks, privacy policy, and terms
remain controlled by Demandbase and the applicable connected data providers.
