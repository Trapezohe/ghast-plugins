# Third-party Codex plugin audit

Source: `https://github.com/openai/plugins` at `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`.

## Scope

- Codex marketplace plugins: 180
- OpenAI-authored plugins excluded: 31
- Third-party developer plugins in scope: 149
- Implemented plugins with authenticated core not exercised: 129

A plugin is not considered complete merely because its Codex manifest is
present or says MIT. Completion requires an independently verified official
source, usable license, explicit capability comparison, and runnable Ghast
verification.

Implementation labels distinguish evidence depth:

- `implemented-verified`: official provenance, package integrity, and explicit recorded core runtime evidence are present.
- `implemented-contract-verified`: the official protocol or published capability contract and package are verified, but authenticated core operations were not exercised with a real account.
- `implemented-runtime-review-required`: a package exists, but the review has no explicit runtime-evidence declaration yet.
- `not-implemented`: no capability-equivalent, authorized package is published.

Audit labels distinguish source-review outcomes:

- `official-source-verified`: an official, licensed source or service contract supports the recorded Ghast implementation.
- `official-port-unavailable`: the official developer and capability are verified, but current license, authentication, entitlement, schema, product, or capability evidence does not permit an independently usable equivalent port.
- `official-source-research-required`: official provenance, licensing, or portability still needs research before a terminal decision can be made.
- `blocked-license`: the declared source is explicitly unavailable for redistribution under its current license.

## Acceptance criteria

- The source is controlled by the named plugin developer or is linked from its official documentation.
- Redistribution and modification are allowed by an identified license.
- The Ghast plugin uses an official API, MCP server, CLI, SDK, or developer-maintained skill source.
- Codex capabilities and Ghast capabilities are compared explicitly.
- Authentication, write actions, and high-risk operations have enforceable safety rules.
- The packaged plugin installs, and runtime claims do not exceed the explicitly recorded evidence.
- An implementation whose authenticated core was not exercised is labeled implemented-contract-verified rather than implemented-verified.

## Inventory

| Plugin | Developer | Codex transport | Declared license | Audit | Ghast | Runtime | Auth core |
| --- | --- | --- | --- | --- | --- | --- | --- |
| actively | Actively | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| aiera | Aiera | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| airtable | Airtable | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| alation | Alation | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| alpaca | Alpaca | appConnector | MIT | official-source-verified | implemented-verified | recorded-core-verification | no |
| amplitude | Amplitude | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| apollo | Apollo | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| asana | Asana, Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| atlassian-rovo | Atlassian | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| attio | Attio Ltd | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| base44 | base44 | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| binance | Binance | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| biorender | BioRender | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| boltz-api-cli | Boltz | skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| brand24 | Brand24 Global Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| brex | Brex Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| brighthire | BrightHire | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| calendly | Calendly | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| canva | Canva | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| carta-crm | Carta Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| catalyst-by-zoho | Catalyst by Zoho | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| cb-insights | CB Insights | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| channel99 | Channel99 Inc.  | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| chronograph-gp | Chronograph | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| chronograph-lp | Chronograph | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| circleback | Circleback AI, Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| circleci | CircleCI | skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| clay | Clay | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| clickup | ClickUp | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| close | Close | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| cloudflare | Cloudflare | mcpServers, skills, commands | MIT | official-source-verified | implemented-verified | recorded-core-verification | no |
| cloudinary | Cloudinary | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| coderabbit | CodeRabbit | skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| cogedim | ALTAREA PROMOTION MANAGEMENT | appConnector | MIT | official-source-verified | implemented-verified | recorded-core-verification | no |
| common-room | Common Room | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| conductor | Conductor Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| convex | Convex, Inc. | appConnector | UNLICENSED | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| coupler-io | Coupler.io | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| coveo | Coveo | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| cube | Cube | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| daloopa | Daloopa | appConnector, skills | Apache-2.0 | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| datadog | Datadog | appConnector | Apache-2.0 | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| datasite | Datasite | appConnector, skills | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| deepnote | Deepnote | appConnector, skills | Apache-2.0 | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| demandbase | Demandbase Inc | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| digitalocean | DigitalOcean | appConnector, skills | none | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| dnb-finance-analytics | Dun & Bradstreet | appConnector, skills | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| docket | Docket AI | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| docusign | Docusign | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| domotz-preview | Domotz | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| dovetail | Dovetail | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| dow-jones-factiva | Factiva, Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| egnyte | Egnyte Inc | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| expo | Expo | skills, commands | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| factset | FactSet | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| fal | Fal | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| figma | Figma | appConnector, mcpServers, skills, commands | LicenseRef-Figma-Developer-Terms | official-port-unavailable | not-implemented | not-implemented | n/a |
| finn | FINN GmbH | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| fireflies | Fireflies | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| fiscal-ai | Fiscal AI | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| fyxer | Fyxer | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| glean | Glean Technologies, Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| govtribe | Government Executive Media Group LLC | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| granola | Granola | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| happenstance | Happenstance, Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| hebbia | Hebbia | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| heygen | HeyGen | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| hg-insights | HG Insights | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| highlevel | HighLevel | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| hostinger | Hostinger | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| hubspot | HubSpot | appConnector, skills | MIT | official-source-verified | implemented-verified | recorded-core-verification | no |
| hugging-face | Hugging Face | appConnector, skills | MIT | official-source-verified | implemented-verified | recorded-core-verification | no |
| hyperframes | HeyGen | skills | Apache-2.0 | official-source-verified | implemented-verified | recorded-core-verification | no |
| intercom | Intercom | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| jam | Jam | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| keybid-puls | KeyBid | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| lovable | Lovable | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| lseg | LSEG | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| magicpath | MagicPathAI | skills | UNLICENSED | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| marcopolo | Immersa, Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| mem | Mem Labs, Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| meticulate | Meticulate | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| midpage | Midpage | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| mixpanel | Mixpanel | appConnector | MIT | official-source-verified | implemented-verified | recorded-core-verification | no |
| mixpanel-headless | Mixpanel | skills | MIT | official-source-verified | implemented-verified | recorded-core-verification | no |
| monday-com | Monday.com | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| moody-s | Moody's | appConnector, skills | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| morningstar | Morningstar | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| motherduck | MotherDuck Corporation | appConnector | MIT | official-source-verified | implemented-verified | recorded-core-verification | no |
| mt-newswires | MT Newswires | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| myregistry-com | MyRegistry.com | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| neon-postgres | Neon | appConnector, skills | Apache-2.0 | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| netlify | Netlify | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| network-solutions | Network Solutions | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| nvidia | NVIDIA | skills | Apache-2.0 AND CC-BY-4.0 | official-source-verified | implemented-verified | recorded-core-verification | n/a |
| omni-analytics | Omni Analytics | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| otter-ai | Otter.ai | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| outreach | Outreach | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| particl-market-research | Particl | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| picsart | Picsart | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| pitchbook | PitchBook | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| policynote | FiscalNote | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| posthog | PostHog | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| pylon | Pylon Labs Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| quartr | Quartr | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| quickbooks | QuickBooks | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| quicknode | Quicknode | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| ranked-ai | Ranked AI, LLC | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| razorpay | Razorpay Software Private Limited | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| read-ai | Read AI, Inc | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| readwise | Readwise Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| remotion | Remotion | skills | MIT | official-source-verified | implemented-verified | recorded-core-verification | n/a |
| render | Render | skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| replayio | Replay | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| replit | Replit | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| responsive | RFPIO Inc. (d/b/a Responsive) | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| rox | Rox Data Corp | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| s-p | S&P Global | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| scite | Scite | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| semrush | Semrush Holdings, Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| setu-bharat-connect-billpay | Setu | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| shopify | Shopify | appConnector, skills | MIT | official-source-verified | implemented-verified | recorded-core-verification | no |
| shutterstock | Shutterstock | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| signnow | airSlate Inc | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| similarweb | Similarweb | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| skywatch | SkyWatch Space Applications Inc. | appConnector | MIT | official-source-verified | implemented-verified | recorded-core-verification | no |
| statsig | Statsig, LLC | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| streak | Rewardly, Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| stripe | Stripe | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| supabase | Supabase | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| superhuman | Superhuman | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| superpowers | Jesse Vincent | skills | MIT | official-source-verified | implemented-verified | recorded-core-verification | n/a |
| taxdown | TAXDOWN S.L. | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| temporal | Temporal | skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| third-bridge | Third Bridge Group | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| thoughtspot | ThoughtSpot | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| tinman-ai | Better | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| twilio-developer-kit | Twilio | skills | MIT | official-source-verified | implemented-verified | recorded-core-verification | no |
| united-rentals | United Rentals | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| vantage | Vantage | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| vercel | Vercel Labs | appConnector, skills, commands | Apache-2.0 | official-source-verified | implemented-verified | recorded-core-verification | no |
| waldo | Curiosities, Inc. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| weatherpromise | WeatherPromise, Inc. | appConnector | MIT | official-port-unavailable | not-implemented | not-implemented | n/a |
| windsor-ai | Windsor.ai | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| wix | Wix | appConnector, skills | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| yepcode | YepCode S.L. | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| zoho | Zoho | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| zoom | Zoom | appConnector, skills, commands | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |
| zoominfo | ZoomInfo | appConnector | MIT | official-source-verified | implemented-contract-verified | authenticated-core-not-exercised | no |

The JSON report is the machine-readable source of truth. Human review
evidence lives in `third-party-plugin-reviews.json` and must be updated
before changing an item to `official-source-verified`.
