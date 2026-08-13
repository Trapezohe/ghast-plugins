# Third-party Codex plugin audit

Source: `https://github.com/openai/plugins` at `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`.

## Scope

- Codex marketplace plugins: 180
- OpenAI-authored plugins excluded: 31
- Third-party developer plugins in scope: 149

A plugin is not considered complete merely because its Codex manifest is
present or says MIT. Completion requires an independently verified official
source, usable license, explicit capability comparison, and runnable Ghast
verification.

## Acceptance criteria

- The source is controlled by the named plugin developer or is linked from its official documentation.
- Redistribution and modification are allowed by an identified license.
- The Ghast plugin uses an official API, MCP server, CLI, SDK, or developer-maintained skill source.
- Codex capabilities and Ghast capabilities are compared explicitly.
- Authentication, write actions, and high-risk operations have enforceable safety rules.
- The packaged plugin installs and its supported core workflows pass recorded verification.

## Inventory

| Plugin | Developer | Codex transport | Declared license | Audit | Ghast |
| --- | --- | --- | --- | --- | --- |
| actively | Actively | appConnector | MIT | official-source-verified | implemented-verified |
| aiera | Aiera | appConnector | MIT | official-source-verified | implemented-verified |
| airtable | Airtable | appConnector, skills | MIT | official-source-verified | implemented-verified |
| alation | Alation | appConnector | MIT | official-source-verified | implemented-verified |
| alpaca | Alpaca | appConnector | MIT | official-source-verified | implemented-verified |
| amplitude | Amplitude | appConnector | MIT | official-source-verified | implemented-verified |
| apollo | Apollo | appConnector | MIT | official-source-verified | implemented-verified |
| asana | Asana, Inc. | appConnector | MIT | official-source-verified | implemented-verified |
| atlassian-rovo | Atlassian | appConnector, skills | MIT | official-source-verified | implemented-verified |
| attio | Attio Ltd | appConnector | MIT | official-source-verified | implemented-verified |
| base44 | base44 | appConnector, skills | MIT | official-source-verified | implemented-verified |
| binance | Binance | appConnector | MIT | official-source-verified | implemented-verified |
| biorender | BioRender | appConnector | MIT | official-source-research-required | not-implemented |
| boltz-api-cli | Boltz | skills | MIT | official-source-verified | implemented-verified |
| brand24 | Brand24 Global Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| brex | Brex Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| brighthire | BrightHire | appConnector, skills | MIT | blocked-license | not-implemented |
| calendly | Calendly | appConnector | MIT | official-source-verified | implemented-verified |
| canva | Canva | appConnector, skills | MIT | official-source-research-required | not-implemented |
| carta-crm | Carta Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| catalyst-by-zoho | Catalyst by Zoho | appConnector, skills | MIT | official-source-research-required | not-implemented |
| cb-insights | CB Insights | appConnector | MIT | official-source-research-required | not-implemented |
| channel99 | Channel99 Inc.  | appConnector | MIT | official-source-research-required | not-implemented |
| chronograph-gp | Chronograph | appConnector, skills | MIT | official-source-research-required | not-implemented |
| chronograph-lp | Chronograph | appConnector, skills | MIT | official-source-research-required | not-implemented |
| circleback | Circleback AI, Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| circleci | CircleCI | skills | MIT | official-source-verified | implemented-verified |
| clay | Clay | appConnector | MIT | official-source-research-required | not-implemented |
| clickup | ClickUp | appConnector | MIT | official-source-verified | implemented-verified |
| close | Close | appConnector | MIT | official-source-research-required | not-implemented |
| cloudflare | Cloudflare | mcpServers, skills, commands | MIT | official-source-verified | implemented-verified |
| cloudinary | Cloudinary | appConnector | MIT | official-source-verified | implemented-verified |
| coderabbit | CodeRabbit | skills | MIT | official-source-verified | implemented-verified |
| cogedim | ALTAREA PROMOTION MANAGEMENT | appConnector | MIT | official-source-research-required | not-implemented |
| common-room | Common Room | appConnector | MIT | official-source-research-required | not-implemented |
| conductor | Conductor Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| convex | Convex, Inc. | appConnector | UNLICENSED | blocked-license | not-implemented |
| coupler-io | Coupler.io | appConnector | MIT | official-source-research-required | not-implemented |
| coveo | Coveo | appConnector | MIT | official-source-research-required | not-implemented |
| cube | Cube | appConnector | MIT | official-source-research-required | not-implemented |
| daloopa | Daloopa | appConnector, skills | Apache-2.0 | official-source-verified | implemented-verified |
| datadog | Datadog | appConnector | Apache-2.0 | official-source-verified | implemented-verified |
| datasite | Datasite | appConnector, skills | MIT | official-source-research-required | not-implemented |
| deepnote | Deepnote | appConnector, skills | Apache-2.0 | official-source-verified | implemented-verified |
| demandbase | Demandbase Inc | appConnector | MIT | official-source-research-required | not-implemented |
| digitalocean | DigitalOcean | appConnector, skills | none | blocked-license | not-implemented |
| dnb-finance-analytics | Dun & Bradstreet | appConnector, skills | MIT | official-source-research-required | not-implemented |
| docket | Docket AI | appConnector | MIT | official-source-research-required | not-implemented |
| docusign | Docusign | appConnector | MIT | official-source-research-required | not-implemented |
| domotz-preview | Domotz | appConnector | MIT | official-source-research-required | not-implemented |
| dovetail | Dovetail | appConnector | MIT | official-source-research-required | not-implemented |
| dow-jones-factiva | Factiva, Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| egnyte | Egnyte Inc | appConnector | MIT | official-source-research-required | not-implemented |
| expo | Expo | skills, commands | MIT | official-source-verified | implemented-verified |
| factset | FactSet | appConnector | MIT | official-source-research-required | not-implemented |
| fal | Fal | appConnector | MIT | official-source-research-required | not-implemented |
| figma | Figma | appConnector, mcpServers, skills, commands | LicenseRef-Figma-Developer-Terms | blocked-license | not-implemented |
| finn | FINN GmbH | appConnector | MIT | official-source-research-required | not-implemented |
| fireflies | Fireflies | appConnector | MIT | official-source-research-required | not-implemented |
| fiscal-ai | Fiscal AI | appConnector | MIT | official-source-research-required | not-implemented |
| fyxer | Fyxer | appConnector | MIT | official-source-research-required | not-implemented |
| glean | Glean Technologies, Inc. | appConnector | MIT | official-source-verified | implemented-verified |
| govtribe | Government Executive Media Group LLC | appConnector | MIT | official-source-research-required | not-implemented |
| granola | Granola | appConnector | MIT | official-source-research-required | not-implemented |
| happenstance | Happenstance, Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| hebbia | Hebbia | appConnector | MIT | official-source-research-required | not-implemented |
| heygen | HeyGen | appConnector, skills | MIT | official-source-verified | implemented-verified |
| hg-insights | HG Insights | appConnector | MIT | official-source-research-required | not-implemented |
| highlevel | HighLevel | appConnector | MIT | official-source-research-required | not-implemented |
| hostinger | Hostinger | appConnector | MIT | official-source-research-required | not-implemented |
| hubspot | HubSpot | appConnector, skills | MIT | official-source-verified | implemented-verified |
| hugging-face | Hugging Face | appConnector, skills | MIT | official-source-verified | implemented-verified |
| hyperframes | HeyGen | skills | Apache-2.0 | official-source-verified | implemented-verified |
| intercom | Intercom | appConnector | MIT | official-source-research-required | not-implemented |
| jam | Jam | appConnector | MIT | official-source-research-required | not-implemented |
| keybid-puls | KeyBid | appConnector | MIT | official-source-research-required | not-implemented |
| lovable | Lovable | appConnector | MIT | official-source-research-required | not-implemented |
| lseg | LSEG | appConnector | MIT | official-source-research-required | not-implemented |
| magicpath | MagicPathAI | skills | UNLICENSED | blocked-license | not-implemented |
| marcopolo | Immersa, Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| mem | Mem Labs, Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| meticulate | Meticulate | appConnector | MIT | official-source-research-required | not-implemented |
| midpage | Midpage | appConnector, skills | MIT | official-source-research-required | not-implemented |
| mixpanel | Mixpanel | appConnector | MIT | official-source-verified | implemented-verified |
| mixpanel-headless | Mixpanel | skills | MIT | official-source-verified | implemented-verified |
| monday-com | Monday.com | appConnector | MIT | official-source-verified | implemented-verified |
| moody-s | Moody's | appConnector, skills | MIT | official-source-research-required | not-implemented |
| morningstar | Morningstar | appConnector, skills | MIT | blocked-license | not-implemented |
| motherduck | MotherDuck Corporation | appConnector | MIT | official-source-verified | implemented-verified |
| mt-newswires | MT Newswires | appConnector | MIT | official-source-research-required | not-implemented |
| myregistry-com | MyRegistry.com | appConnector | MIT | official-source-research-required | not-implemented |
| neon-postgres | Neon | appConnector, skills | Apache-2.0 | official-source-verified | implemented-verified |
| netlify | Netlify | appConnector, skills | MIT | official-source-verified | implemented-verified |
| network-solutions | Network Solutions | appConnector | MIT | official-source-research-required | not-implemented |
| nvidia | NVIDIA | skills | Apache-2.0 AND CC-BY-4.0 | official-source-verified | implemented-verified |
| omni-analytics | Omni Analytics | appConnector | MIT | official-source-research-required | not-implemented |
| otter-ai | Otter.ai | appConnector | MIT | official-source-research-required | not-implemented |
| outreach | Outreach | appConnector | MIT | official-source-research-required | not-implemented |
| particl-market-research | Particl | appConnector | MIT | official-source-research-required | not-implemented |
| picsart | Picsart | appConnector | MIT | official-source-research-required | not-implemented |
| pitchbook | PitchBook | appConnector | MIT | official-source-research-required | not-implemented |
| policynote | FiscalNote | appConnector | MIT | official-source-research-required | not-implemented |
| posthog | PostHog | appConnector, skills | MIT | official-source-verified | implemented-verified |
| pylon | Pylon Labs Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| quartr | Quartr | appConnector | MIT | official-source-verified | implemented-verified |
| quickbooks | QuickBooks | appConnector | MIT | official-source-research-required | not-implemented |
| quicknode | Quicknode | appConnector | MIT | official-source-verified | implemented-verified |
| ranked-ai | Ranked AI, LLC | appConnector | MIT | official-source-research-required | not-implemented |
| razorpay | Razorpay Software Private Limited | appConnector | MIT | official-source-research-required | not-implemented |
| read-ai | Read AI, Inc | appConnector | MIT | official-source-verified | implemented-verified |
| readwise | Readwise Inc. | appConnector | MIT | official-source-verified | implemented-verified |
| remotion | Remotion | skills | MIT | official-source-verified | implemented-verified |
| render | Render | skills | MIT | official-source-verified | implemented-verified |
| replayio | Replay | appConnector, skills | MIT | official-source-verified | implemented-verified |
| replit | Replit | appConnector | MIT | official-source-research-required | not-implemented |
| responsive | RFPIO Inc. (d/b/a Responsive) | appConnector | MIT | official-source-research-required | not-implemented |
| rox | Rox Data Corp | appConnector | MIT | official-source-research-required | not-implemented |
| s-p | S&P Global | appConnector | MIT | official-source-research-required | not-implemented |
| scite | Scite | appConnector | MIT | official-source-research-required | not-implemented |
| semrush | Semrush Holdings, Inc. | appConnector | MIT | official-source-verified | implemented-verified |
| setu-bharat-connect-billpay | Setu | appConnector | MIT | official-source-research-required | not-implemented |
| shopify | Shopify | appConnector, skills | MIT | official-source-verified | implemented-verified |
| shutterstock | Shutterstock | appConnector | MIT | official-source-research-required | not-implemented |
| signnow | airSlate Inc | appConnector | MIT | official-source-verified | implemented-verified |
| similarweb | Similarweb | appConnector | MIT | official-source-verified | implemented-verified |
| skywatch | SkyWatch Space Applications Inc. | appConnector | MIT | official-source-verified | implemented-verified |
| statsig | Statsig, LLC | appConnector | MIT | official-source-verified | implemented-verified |
| streak | Rewardly, Inc. | appConnector | MIT | official-source-verified | implemented-verified |
| stripe | Stripe | appConnector, skills | MIT | official-source-verified | implemented-verified |
| supabase | Supabase | appConnector, skills | MIT | official-source-verified | implemented-verified |
| superhuman | Superhuman | appConnector, skills | MIT | official-source-verified | implemented-verified |
| superpowers | Jesse Vincent | skills | MIT | official-source-verified | implemented-verified |
| taxdown | TAXDOWN S.L. | appConnector | MIT | official-source-research-required | not-implemented |
| temporal | Temporal | skills | MIT | official-source-verified | implemented-verified |
| third-bridge | Third Bridge Group | appConnector | MIT | official-source-research-required | not-implemented |
| thoughtspot | ThoughtSpot | appConnector | MIT | official-source-research-required | not-implemented |
| tinman-ai | Better | appConnector | MIT | official-source-research-required | not-implemented |
| twilio-developer-kit | Twilio | skills | MIT | official-source-verified | implemented-verified |
| united-rentals | United Rentals | appConnector | MIT | official-source-research-required | not-implemented |
| vantage | Vantage | appConnector | MIT | official-source-verified | implemented-verified |
| vercel | Vercel Labs | appConnector, skills, commands | Apache-2.0 | official-source-verified | implemented-verified |
| waldo | Curiosities, Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| weatherpromise | WeatherPromise, Inc. | appConnector | MIT | official-source-research-required | not-implemented |
| windsor-ai | Windsor.ai | appConnector | MIT | official-source-research-required | not-implemented |
| wix | Wix | appConnector, skills | MIT | official-source-verified | implemented-verified |
| yepcode | YepCode S.L. | appConnector | MIT | official-source-verified | implemented-verified |
| zoho | Zoho | appConnector | MIT | official-source-research-required | not-implemented |
| zoom | Zoom | appConnector, skills, commands | MIT | official-source-verified | implemented-verified |
| zoominfo | ZoomInfo | appConnector | MIT | official-source-research-required | not-implemented |

The JSON report is the machine-readable source of truth. Human review
evidence lives in `third-party-plugin-reviews.json` and must be updated
before changing an item to `official-source-verified`.
