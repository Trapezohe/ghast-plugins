# Plugin catalog acceptance — 2026-09-08

Catalog commit: `b313de887d750b67432fe2a8646d42f86fe5faab`  
Catalog SHA-256: `ff69e42b7c9c46aa1a4dbd55c22cf0a7481731bc884918c6c2c61855ad5f1074`

## Verified scope

- 501 plugin manifests and packages; 1,384 skills. Count is plugins, not MCP servers or authenticated accounts.
- Repository build and validator completed successfully. Two existing NVIDIA script warnings concern macOS Bash 3.2 parsing of byte-identical signed container scripts.
- All 501 plugins passed isolated installation and uninstallation through Ghast's actual PluginManager. Every plugin loaded its image data URI, English and Chinese introduction fields, display name and category. Source directories were preserved and each test install was removed.
- MCP contributions were registered with an in-memory test receiver. Credential templates were checked through the actual FileMcpServerManager resolver with fixture values. These checks do not claim service initialization, account authorization or business operations for all providers.
- The live Electron UI displayed the 501-entry catalog. Scite's refreshed official logo and version were observed; its list and detail descriptions switched between Chinese and English without bilingual concatenation. The detail view remained inside the store. The original Chinese preference was restored.
- Missing database, design, marketing and system category translations were repaired in the local Ghast application and checked in the rendered UI. Application changes remain in its separate working tree; this plugin-repository publication is not a desktop release.
- All manifests contain image assets and separate `en`/`zh-CN` introductions. The earlier 86-item generic-logo review was completed. Brand assets retain provider ownership.
- Linear, Notion, Sentry and Android testing now contain Ghast-maintained workflows rather than copied OpenAI plugin implementations. No manifest repository points to `github.com/openai/plugins`.

## Source evidence coverage

311 plugins declare `officialConnectorSource`; 132 more have `official-source-verified` entries with officiality evidence in `third-party-plugin-reviews.json`. The following 46 legacy MCP configurations were checked against their primary provider documentation or repositories during this acceptance pass. This verifies published endpoint provenance, not current account entitlements or successful business operations.

The remaining 12 are Ghast-authored local or public-API utilities: github-stats, hacker-news, seo-meta, steam-search, uptime-check, stock-quote, mermaid-mindmap, current-datetime, bilibili-search, realtime-weather, defillama and website-fetcher. They are not represented as provider-operated MCP servers. Public endpoint availability and usage restrictions remain external dependencies.

| Plugin | Official source | Configured endpoints |
| --- | --- | --- |
| cal-com | [Provider source](https://cal.com/docs/mcp-server) | `https://mcp.cal.com/mcp` |
| contentful | [Provider source](https://www.contentful.com/developers/docs/tools/mcp-server/) | `https://mcp.contentful.com/mcp` |
| clickhouse | [Provider source](https://github.com/ClickHouse/agentic-data-stack/blob/main/librechat.yaml) | `https://mcp.clickhouse.cloud/mcp` |
| webflow | [Provider source](https://developers.webflow.com/mcp/reference/getting-started) | `https://mcp.webflow.com/mcp` |
| deepwiki | [Provider source](https://docs.devin.ai/work-with-devin/deepwiki-mcp) | `https://mcp.deepwiki.com/mcp` |
| ref | [Provider source](https://docs.ref.tools/context/install/index) | `https://api.ref.tools/mcp` |
| crawl4ai | [Provider source](https://gate.crawl4ai.com/) | `https://gate.crawl4ai.com/mcp` |
| svelte | [Provider source](https://svelte.dev/docs/ai/remote-setup) | `https://mcp.svelte.dev/mcp` |
| mux | [Provider source](https://www.mux.com/docs/integrations/mcp-server) | `https://mcp.mux.com` |
| tomtom | [Provider source](https://docs.tomtom.com/tomtom-maps-mcp/documentation/quick-setup) | `https://mcp.tomtom.com/maps` |
| context7 | [Provider source](https://context7.com/docs/resources/all-clients) | `https://mcp.context7.com/mcp/oauth` |
| dune | [Provider source](https://dune.com/blog/dune-mcp) | `https://api.dune.com/mcp/v1` |
| bitly | [Provider source](https://dev.bitly.com/bitly-mcp/overview/quickstart/) | `https://api-ssl.bitly.com/v4/mcp` |
| firecrawl | [Provider source](https://github.com/firecrawl/firecrawl-mcp-server) | `https://mcp.firecrawl.dev/v2/mcp-oauth` |
| klaviyo | [Provider source](https://developers.klaviyo.com/en/docs/klaviyo_mcp_server) | `https://mcp.klaviyo.com/mcp` |
| wrike | [Provider source](https://developers.wrike.com/docs/setup-other-mcp-clients-with-wrike-mcp) | `https://mcp.wrike.com/v2` |
| smartsheet | [Provider source](https://developers.smartsheet.com/ai-mcp/smartsheet/install-the-smartsheet-mcp-server/manually-configure-the-mcp-server) | `https://mcp.smartsheet.com` |
| square | [Provider source](https://developer.squareup.com/docs/mcp) | `https://mcp.squareup.com/mcp` |
| pipedrive | [Provider source](https://support.pipedrive.com/en/article/mcp-chatgpt) | `https://mcp.pipedrive.ai/mcp` |
| exa | [Provider source](https://exa.ai/docs/reference/exa-mcp) | `https://mcp.exa.ai/mcp` |
| prisma | [Provider source](https://github.com/prisma/mcp) | `https://mcp.prisma.io/mcp` |
| miro | [Provider source](https://developers.miro.com/docs/miro-mcp-server-frequently-asked-questions) | `https://mcp.miro.com/` |
| postman | [Provider source](https://learning.postman.com/latest-v-12/docs/reference/postman-api/postman-mcp-server/postman-mcp-remote-server) | `https://mcp.postman.com/minimal` |
| wolfram | [Provider source](https://github.com/WolframResearch/AgentTools/blob/main/AgentSkills/Skills/wolfram-language/references/SetUpWolframMCPServer.md) | `https://services.wolfram.com/api/mcp` |
| honeycomb | [Provider source](https://docs.honeycomb.io/integrations/mcp/configuration-guide) | `https://mcp.honeycomb.io/mcp` |
| se-ranking | [Provider source](https://seranking.com/api/integrations/mcp/) | `https://api.seranking.com/mcp` |
| axiom | [Provider source](https://axiom.co/docs/console/intelligence/mcp-server) | `https://mcp.axiom.co/mcp` |
| financial-datasets | [Provider source](https://docs.financialdatasets.ai/mcp-server) | `https://mcp.financialdatasets.ai/` |
| coingecko | [Provider source](https://mcp.api.coingecko.com/) | `https://mcp.api.coingecko.com/mcp` |
| sanity | [Provider source](https://www.sanity.io/docs/ai/mcp-server) | `https://mcp.sanity.io` |
| todoist | [Provider source](https://developer.todoist.com/api/v1/#tag/Todoist-MCP) | `https://ai.todoist.net/mcp` |
| jina-ai | [Provider source](https://github.com/jina-ai/MCP) | `https://mcp.jina.ai/v1` |
| github | [Provider source](https://github.com/github/github-mcp-server) | `https://api.githubcopilot.com/mcp/` |
| lucid | [Provider source](https://help.lucid.co/hc/en-us/articles/42578801807508-Integrate-Lucid-with-AI-tools-using-the-Lucid-MCP-server) | `https://mcp.lucid.app/mcp` |
| microsoft-learn | [Provider source](https://learn.microsoft.com/en-us/training/support/mcp) | `https://learn.microsoft.com/api/mcp` |
| paypal | [Provider source](https://paypal.gitbook.com/agent-toolkit-and-mcp-server/mcp-server/set-up-a-remote-mcp-server) | `https://mcp.paypal.com/sse` |
| excalidraw-plus | [Provider source](https://plus.excalidraw.com/docs/mcp) | `https://api.excalidraw.com/api/v1/mcp` |
| fathom | [Provider source](https://developers.fathom.ai/mcp-docs) | `https://api.fathom.ai/mcp` |
| astro | [Provider source](https://docs.astro.build/en/guides/build-with-ai/) | `https://mcp.docs.astro.build/mcp` |
| tavily | [Provider source](https://docs.tavily.com/documentation/mcp) | `https://mcp.tavily.com/mcp/` |
| bright-data | [Provider source](https://brightdata.com/blog/ai/trueforge-with-bright-data) | `https://mcp.brightdata.com/mcp` |
| aws-knowledge | [Provider source](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server) | `https://knowledge-mcp.global.api.aws` |
| imagekit | [Provider source](https://imagekit.io/docs/build-with-ai) | `https://api-mcp.imagekit.io/mcp`, `https://devtools-mcp.imagekit.io/mcp` |
| apify | [Provider source](https://docs.apify.com/integrations/mcp) | `https://mcp.apify.com` |
| resend | [Provider source](https://github.com/resend/resend-mcp) | `https://mcp.resend.com/mcp` |
| buffer | [Provider source](https://buffer.com/integrations/claude) | `https://mcp.buffer.com/mcp` |

Contentful, Dune and Lucid blocked direct command-line document retrieval, but their provider pages were read through the web reader and explicitly listed the configured endpoints. Miro documents its root URL without a trailing slash; the configured trailing slash denotes the same root resource. No endpoint changes were needed in this pass.

## Isolated installation results

These results validate local installation and cleanup, not authenticated provider calls.

```text
1inch: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
aave: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
abtasty: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
actively: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
adobe-analytics: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
adobe-express: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
adobe-target: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
agentmail: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
agilitycms: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
aiera: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
airbyte: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
airtable: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
airwallex: install, logo, bilingual introduction, 3 MCP registrations and uninstall PASS
aiven: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
akiflow: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
alation: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
alchemy: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
algolia: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
allium: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
alpaca: install, logo, bilingual introduction, 3 MCP registrations and uninstall PASS
amplitude: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
angular: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
ankr: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
anytype: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
apify: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
apollo: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
appsflyer: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
appwrite: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
arcjet: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
asana: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
ashby: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
assemblyai-docs: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
astro: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
atlassian-rovo: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
attio: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
avalanche: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
avaza: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
aws-knowledge: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
axiom: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
azure: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
balsamiq: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
base44: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
basedash: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
beehiiv: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
better-stack: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
bilibili-search: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
binance: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
biorender: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
bird: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
birdeye: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
bitget: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
bitly: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
bitquery: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
blockscout: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
boltz-api-cli: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
bonsai: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
box: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
braintrust: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
brand24: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
brave-search: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
braze: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
brevo: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
brex: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
bright-data: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
brighthire: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
browserless: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
browserstack: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
buffer: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
bugsnag: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
buildkite: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
bybit: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
cal-com: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
calendly: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
campfire: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
canny: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
canva: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
capacities: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
carta-crm: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
cartesia: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
catalyst-by-zoho: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
cb-insights: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
censys: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
chainstack: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
channel99: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
checkly: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
chroma: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
chrome-devtools: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
chronograph-gp: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
chronograph-lp: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
circleback: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
circleci: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
clay: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
clerk: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
clickhouse: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
clickup: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
clockify: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
close: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
cloudflare: install, logo, bilingual introduction, 5 MCP registrations and uninstall PASS
cloudinary: install, logo, bilingual introduction, 5 MCP registrations and uninstall PASS
cobo: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
cockroachdb: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
coda: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
coderabbit: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
cogedim: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
coinbase-developer: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
coingecko: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
coinglass: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
coinmarketcap: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
coinpaprika: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
coinstats: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
cometchat: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
common-room: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
conductor: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
configcat: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
confluent: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
consensus: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
contentful: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
contentstack: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
context7: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
convex: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
coresignal: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
couchbase: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
coupler-io: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
courier: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
coveo: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
craft: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
crawl4ai: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
crisp: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
crossmint: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
crowdin: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
crypto-com: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
cryptohopper: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
cryptoquant: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
cryptorank: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
cube: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
current-datetime: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
customer-io: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
daloopa: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
dartai: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
datadog: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
dataforseo: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
deel: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
deepnote: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
deepwiki: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
defillama: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
demandbase: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
descope: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
descript: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
devcycle: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
devexpress: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
dexpaprika: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
digitalocean: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
dingtalk: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
directus: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
docusign: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
dodopayments: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
domotz-preview: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
doppler: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
dovetail: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
dow-jones-factiva: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
drawio: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
dropbox: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
duda: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
dune: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
egnyte: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
elevenlabs: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
enterpret: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
eraser: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
etherscan: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
everhour: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
exa: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
excalidraw-plus: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
expo: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
factset: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
fal: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
fathom: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
featurebase: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
feishu-lark: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
fellow: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
fibery: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
financial-datasets: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
firebase: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
firecrawl: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
fireflies: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
fiscal-ai: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
fish-audio-docs: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
folk: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
formbricks: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
freshworks-developer: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
front: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
fullstory: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
fyxer: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
gainium: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
gate: install, logo, bilingual introduction, 5 MCP registrations and uninstall PASS
gitbook: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
github: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
github-stats: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
gitlab: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
glassnode: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
glean: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
goldrush: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
google-ads: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
google-analytics: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
google-calendar: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
google-chat: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
google-contacts: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
google-docs: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
google-drive: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
google-gmail: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
google-sheets: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
google-slides: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
gorgias: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
govtribe: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
grafana: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
granola: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
graphlit: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
greenhouse: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
growthbook: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
guru: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
hacker-news: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
happenstance: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
harness: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
harvest: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
hebbia: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
hedera: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
helicone: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
helius: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
help-scout: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
heptabase: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
hex: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
heygen: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
hg-insights: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
hibob: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
higgsfield: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
highlevel: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
honeycomb: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
hostinger: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
hubspot: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
hugging-face: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
hygraph: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
hyperframes: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
ideogram: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
imagekit: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
incident-io: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
infisical: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
influxdb: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
infobip: install, logo, bilingual introduction, 7 MCP registrations and uninstall PASS
inngest: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
instantly: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
intercom: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
jam: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
jina-ai: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
jotform: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
justcall: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
kagi: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
kittl: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
klaviyo: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
knock: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
knowify: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
kong-konnect: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
kontent-ai: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
kraken: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
kustomer: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
langfuse: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
langsmith: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
launchdarkly: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
lemlist: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
linear: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
linearb: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
livekit-docs: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
logrocket: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
lokalise: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
loops: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
lottiefiles: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
lovable: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
lucid: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
magicpath: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
magnific: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mailchimp-transactional: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mailerlite: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mailgun: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mailtrap: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
make: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mapbox: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
marcopolo: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
maze: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
meilisearch: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mem: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mem0: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mercury: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mermaid-mindmap: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
messari: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
meteomatics: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
microsoft-learn: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
microsoft-release-communications: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
microsoft-workiq: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
midpage: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
miro: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
missive: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mixpanel: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mixpanel-headless: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
monday-com: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mongodb: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
moonpay: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
moralis: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
morningstar: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
motherduck: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mt-newswires: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
mux: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
myregistry-com: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
nansen: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
neon-postgres: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
netlify: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
nextjs: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
notion: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
novu: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
nuclino: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
nuxt: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
nvidia: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
nylas: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
okx: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
omni-analytics: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
onesignal: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
onlyoffice: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
optimizely: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
ordinal: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
otter-ai: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
outreach: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
paddle: install, logo, bilingual introduction, 3 MCP registrations and uninstall PASS
pagerduty: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
particl-market-research: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
paypal: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
pendo: install, logo, bilingual introduction, 5 MCP registrations and uninstall PASS
penpot: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
perplexity: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
phantom: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
phoenix: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
photoroom: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
picsart: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
pinecone: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
pipedrive: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
plaid: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
plain: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
planetscale: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
playwright: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
polar: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
policynote: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
posthog: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
postman: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
postmark: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
prefect: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
prisma: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
prismic: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
privy: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
productboard: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
productive: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
pulumi: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
pumble: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
pylon: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
qdrant: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
quartr: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
questdb: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
quicknode: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
railway: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
ramp: install, logo, bilingual introduction, 3 MCP registrations and uninstall PASS
ranked-ai: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
razorpay: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
read-ai: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
readwise: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
realtime-weather: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
reclaim: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
recraft: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
recurly: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
redis: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
redis-docs: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
redpanda: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
ref: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
relume: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
remote: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
remotion: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
render: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
replayio: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
replicate: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
replit: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
resend: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
responsive: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
risingwave: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
rollbar: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
rootly: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
rudderstack: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
runway: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
s-p: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
sanity: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
santiment: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
scite: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
se-ranking: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
sei: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
semgrep: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
semrush: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
sentry: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
seo-meta: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
serpstat: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
setu-bharat-connect-billpay: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
shopify: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
shortcut: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
shutterstock: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
signnow: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
similarweb: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
singlestore: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
sitecore: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
skywatch: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
slack: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
slite: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
smartsheet: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
snyk: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
socket: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
solana: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
square: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
starrocks: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
statsig: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
steam-search: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
stellar: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
stock-quote: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
storyblok: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
streak: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
stripe: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
stytch: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
sunsama: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
supabase: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
superhuman: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
superpowers: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
suprsend: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
surrealdb: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
survicate: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
svelte: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
swagger: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
tally: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
tallyfy: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
tana: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
taskade: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
tatum: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
tavily: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
tavus-docs: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
teamwork: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
tella: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
telnyx: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
temporal: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
tenderly: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
tenzo: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
terraform: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
test-android-apps: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
third-bridge: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
thoughtspot: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
tigerdata-pg-aiguide: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
timing: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
todoist: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
toggl: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
token-terminal: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
tomtom: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
trust-wallet: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
turso: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
twilio-developer-kit: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
uniform: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
unleash: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
upstash: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
uptime-check: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
vantage: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
vapi: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
veed: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
vercel: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
visily: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
vonage: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
waldo: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
wandb: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
weatherapi: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
webex: install, logo, bilingual introduction, 4 MCP registrations and uninstall PASS
webflow: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
website-fetcher: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
whimsical: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
windsor-ai: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
wingify: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
wistia: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
wix: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
wolfram: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
wordpress-com: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
workfront: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
workos: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
wrike: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
writer: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
xata: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
xero: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
yepcode: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
you-com: install, logo, bilingual introduction, 2 MCP registrations and uninstall PASS
youcam: install, logo, bilingual introduction, 3 MCP registrations and uninstall PASS
zapier: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
zep: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
zerion: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
zilliz: install, logo, bilingual introduction, 1 MCP registrations and uninstall PASS
zoho: install, logo, bilingual introduction, 4 MCP registrations and uninstall PASS
zoom: install, logo, bilingual introduction, 7 MCP registrations and uninstall PASS
zoominfo: install, logo, bilingual introduction, 0 MCP registrations and uninstall PASS
```

## Additional source refresh

A subsequent read of all 311 declared official source pages found the configured
endpoint or the actual stdio package name in 273 primary pages. Android App
Testing has no MCP declaration; its official SDK provenance and CLI version/help
were independently checked in commit `b313de88`.

All 37 follow-ups are now resolved against the primary sources below. Together
with the 273 direct matches and the independently verified Android SDK, all 311
declared source records have been reviewed. This closes the provenance refresh;
it does not assert authenticated business-operation coverage. No plugin runtime
or package changed during this documentation-only follow-up.

| Plugin | Additional primary evidence | Result |
| --- | --- | --- |
| airwallex | [Source 1](https://www.airwallex.com/docs/developer-tools/ai/developer-mcp) | Configured endpoint or official package confirmed. |
| algolia | [Source 1](https://docsearch.algolia.com/docs/mcp/overview/) | Configured endpoint or official package confirmed. |
| ankr | [Source 1](https://www.ankr.com/docs/rpc-service/getting-started/management-mcp/) | Configured endpoint or official package confirmed. |
| appsflyer | [Source 1](https://support.appsflyer.com/hc/en-us/articles/36349070304785--Beta-AppsFlyer-MCP) | Configured endpoint or official package confirmed. |
| appwrite | [Source 1](https://appwrite.io/docs/tooling/ai/mcp-servers) | Configured endpoint or official package confirmed. |
| assemblyai-docs | [Source 1](https://www.assemblyai.com/docs/coding-agent-prompts) | Docs use the bare domain. Both bare and configured www endpoints returned AssemblyAI 1.0.0 from MCP initialize (protocol 2025-03-26). HEAD returned 405 and was not treated as an MCP failure. |
| beehiiv | [Source 1](https://beehiivhelp.zendesk.com/hc/en-us/articles/39255979546263-Getting-started-with-the-beehiiv-MCP) | Configured endpoint or official package confirmed. |
| birdeye | [Source 1](https://docs.birdeye.so/docs/birdeye-ai) | Configured endpoint or official package confirmed. |
| brevo | [Source 1](https://help.brevo.com/hc/en-us/articles/27978590646802-What-is-Model-Context-Protocol-MCP) | Configured endpoint or official package confirmed. |
| coda | [Source 1](https://help.coda.io/hc/en-us/articles/44722661982989-Connect-to-the-Coda-MCP) | Configured endpoint or official package confirmed. |
| consensus | [Source 1](https://docs.consensus.app/consensus-mcp) | Configured endpoint or official package confirmed. |
| cryptorank | [Source 1](https://cryptorank.io/insights/analytics/how-to-use-CryptoRank-MCP-server) | Configured endpoint or official package confirmed. |
| elevenlabs | [Source 1](https://elevenlabs.io/mcp) | Configured endpoint or official package confirmed. |
| fish-audio-docs | [Source 1](https://fish.audio/zh-CN/blog/llms-txt-mcp-agent-skills/) | Provider blog documents the docs endpoint; live initialize returned Fish Audio 1.0.0. This remains the documentation service, separate from the newer API MCP. |
| fullstory | [Source 1](https://developer.fullstory.com/mcp/faq/index.html) | Configured endpoint or official package confirmed. |
| gitlab | [Source 1](https://docs.gitlab.com/user/model_context_protocol/mcp_server/) | Documentation explicitly substitutes gitlab.com into its instance URL template. |
| harness | [Source 1](https://github.com/harness/mcp-server) | Configured endpoint or official package confirmed. |
| harvest | [Source 1](https://support.getharvest.com/api/v2/help_center/en-us/articles/46293697226381.json) | Read the public provider Help Center API representation of the same article after the HTML reader failed. |
| hibob | [Source 1](https://www.hibob.com/platform/core/ai/mcp/) | Configured endpoint or official package confirmed. |
| influxdb | [Source 1](https://docs.influxdata.com/influxdb/v2/tools/mcp-server/) | Configured endpoint or official package confirmed. |
| kittl | [Source 1](https://www.kittl.com/mcp) | Configured endpoint or official package confirmed. |
| knowify | [Source 1](https://knowify.zendesk.com/hc/en-us/articles/49623682048660-Getting-started-with-the-Knowify-AI-Connector) | Configured endpoint or official package confirmed. |
| linearb | [Source 1](https://linearb.zendesk.com/hc/en-us/articles/45537283788827-MCP-Server), [Source 2](https://linearb.zendesk.com/hc/en-us/articles/45552138846491-2026-Release-Notes) | Installation article supplies endpoint; March 2026 release notes supersede its older API-key setup with OAuth. |
| magnific | [Source 1](https://www.magnific.com/ai/docs/magnific-mcp) | Configured endpoint or official package confirmed. |
| microsoft-workiq | [Source 1](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/quickstart/github-copilot-cli) | Configured endpoint or official package confirmed. |
| paddle | [Source 1](https://developer.paddle.com/sdks/ai/docs-mcp/) | Configured endpoint or official package confirmed. |
| phantom | [Source 1](https://docs.phantom.com/resources/mcp-server) | Configured endpoint or official package confirmed. |
| ramp | [Source 1](https://agents.ramp.com/docs/guides/connecting), [Source 2](https://docs.ramp.com/developer-api/v1/developer-mcp), [Source 3](https://docs.ramp.com/developer-api/v1/ramp-data-mcp) | All three configured service endpoints are documented separately. |
| replicate | [Source 1](https://mcp.replicate.com/) | Configured endpoint or official package confirmed. |
| risingwave | [Source 1](https://github.com/risingwavelabs/risingwave-mcp/blob/c148f80dae9070782bd4393c4a4b729e863e4718/src/main.py) | The audit incorrectly treated uv as a server package. This plugin runs bundled official src/main.py; bytes match the pinned provider commit. uv only supplies the isolated Python runtime. |
| runway | [Source 1](https://help.runwayml.com/hc/en-us/articles/51931843164691-Connecting-to-Runway-MCP) | Configured endpoint or official package confirmed. |
| serpstat | [Source 1](https://serpstat.com/blog/best-seo-mcp-servers-comparison/) | Configured endpoint or official package confirmed. |
| tenderly | [Source 1](https://tenderly.co/blog/validating-agentic-workflows-with-tenderly-mcp-server/) | Configured endpoint or official package confirmed. |
| veed | [Source 1](https://github.com/veedstudio/veed-fabric-mcp/blob/main/docs/authentication.md) | Configured endpoint or official package confirmed. |
| webex | [Source 1](https://developer.webex.com/meeting/docs/meetings-mcp-server), [Source 2](https://developer.webex.com/mcp/docs/messaging-mcp-server), [Source 3](https://developer.webex.com/mcp/docs/vidcast-mcp-server), [Source 4](https://developer.webex.com/mcp/docs/workspaces-mcp-server) | All four configured service endpoints are documented separately. |
| zapier | [Source 1](https://zapier.com/) | Configured endpoint or official package confirmed. |
| zilliz | [Source 1](https://docs.zilliz.com/docs/zilliz-mcp-server) | Configured endpoint or official package confirmed. |

Current Logo ownership statements in 92 published plugin review entries were
updated to agree with their README provenance. Historical runtime observations
and records for plugins that are not published were retained.
