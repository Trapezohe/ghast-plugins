# Modifications

Ghast depends on Razorpay's official MIT-licensed MCP server at revision
`7950d51d118ca164c32b7cf0cfaa14f34f24849f` through the exact Go module
pseudo-version `v0.0.0-20260326095236-7950d51d118c`.

The official source is not copied into this package. The adapter:

- enables only the official `payments`, `payment_links`, `orders`, `refunds`,
  `payouts`, `qr_codes`, and `settlements` toolsets in strict read-only mode;
- excludes all official write tools, registration links, and checkout code
  generation helpers;
- adds one Ghast-authored `fetch_tokens` tool using Razorpay's official Go SDK;
- requires `customer_id`, rejects `contact`, and performs only the same two GET
  requests used by the official customer-ID branch;
- adds local build, credential, source-integrity, safety, catalog, and
  packaging files under the Ghast MIT license.

This is an explicitly labeled read-only adaptation, not an unchanged upstream
binary and not a claim that Ghast authored Razorpay's official tools.
