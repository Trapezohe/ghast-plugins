# setu-bharat-connect-billpay

Discover, fetch, pay, and track Bharat Connect bills through Setu's official
hosted Bill Payments MCP server.

## Official service

Setu publishes `https://billpay-mcp.setu.co/mcp` as its OAuth-enabled remote
MCP endpoint for ChatGPT, Claude, Perplexity, and other compatible clients.
Authentication uses a Setu-hosted mobile-number and OTP flow.

The current official tool guide documents:

- `List Billers`
- `List Categories`
- `Get Saved Bills`
- `Fetch Bill`
- `Pay Bill`
- `Check Payment Status`
- `Get Transaction Receipt`
- `List Payment History`

## Capability comparison

- Codex: find billers, fetch exact bill amounts, review pending bills and
  expenses, pay with confirmation, and check transaction success through a
  private app connector.
- Ghast: connect directly to the same developer-operated MCP and use all eight
  officially documented discovery, fetch, payment, status, receipt, and
  history workflows.
- The official remote MCP is capability-equivalent to the Codex description
  and makes the portable endpoint and OAuth flow public.

## Verification and licensing

The importer pins Setu's official integration guide, exact eight-tool guide,
transaction and AI terms, protected-resource metadata, OAuth and OpenID
metadata, anonymous MCP authentication boundary, and the complete OpenAI
marketplace snapshot. An optional disposable registration check verifies that
authorization reaches Setu's own phone and OTP page. Authenticated bill and
payment calls were not executed.

The OAuth metadata publishes authorization, token, and dynamic registration
endpoints plus PKCE S256. Disposable registration currently returns a client
secret and does not echo `token_endpoint_auth_method`; this adapter stores no
client credential and leaves OAuth handling to the host MCP client.

The MIT license in this package covers only the Ghast-authored endpoint
declaration, safety guidance, metadata, documentation, and generic bill icon.
It does not license or redistribute Setu's hosted implementation, private
Codex connector, service data, credentials, documentation, logos, trademarks,
marketplace artwork, biller data, or payment-network content. Access, identity
verification, payments, fees, settlement, refunds, disputes, service limits,
and terms remain controlled by Setu and the relevant regulated participants.
