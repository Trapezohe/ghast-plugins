# fyxer

Search authorized email and meeting context, retrieve summaries and
transcripts, resolve contacts, and draft personalized email through Fyxer's
official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored configuration, safety instructions,
documentation, metadata, and a generic email-context icon. It does not
redistribute Fyxer's hosted implementation, private Codex connector, account
data, OAuth credentials, writing-style model, branded artwork, or marketplace
icon.

Fyxer's official MCP and add-ons pages are pinned at normalized visible-text
SHA-256 `524a8683cf7b177c93966c82226574351dd4d6e998d74a333050fa50829fb928` and `d1b55e0ef54e828f61c8811619b97a1c7898050230232c0dbe759d7f678ae8c0`. The documented
six-tool order is pinned at `dc4f1638f900ca0062c48861b22e1ce0c05104d7d19fb477357c57d8b61c1054`. Protected-resource and
authorization-server metadata are pinned at canonical JSON SHA-256
`c0a99fecb69d163d71ce9bde9b33ee2aa2fa90710ab25e180e391bddcbdd3036` and `fde6773cf90838ed70eaf796663bdf7141be68e6691a592fa2ea8bace1d3c20a`.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app identifier or
marketplace artwork.

## Ghast compatibility

- Ghast connects directly to `https://app.fyxer.com/mcp` over Streamable HTTP and uses
  Fyxer browser OAuth.
- The official six tools search email, meetings, and documents; find
  meetings and recordings; retrieve meeting summaries and full transcripts;
  resolve contacts; and draft email adapted to the user's writing style.
- This is a functional superset of the Codex workflow for following up after
  a meeting. It can resolve the intended person and meeting, inspect relevant
  context, and produce a personalized draft.
- Fyxer states that `draft_email` returns the draft in chat and does not send
  email. The user must select Open in Outlook or Gmail, then review, edit, and
  send it. The included skill never reports a message as saved or sent.
- OAuth publishes six scopes, Dynamic Client Registration, authorization
  code, refresh tokens, public clients, and PKCE S256. On August 13, 2026, a
  loopback public client registered with HTTP 200 without a client secret,
  and its PKCE request reached Fyxer's `/auth/mcp` login page.
- Fyxer warns that other cloud-hosted products may require an approved OAuth
  callback URL. The successful local loopback probe establishes desktop
  compatibility, not blanket approval for every deployment.
- Missing and invalid credentials returned HTTP 401 with Fyxer's exact OAuth
  challenge. Authenticated tools/list and private email or meeting operations
  were not run because no Fyxer account or user data was used.
- A generic email-context icon is used because no licensed Fyxer catalog
  artwork is redistributed.

The MIT license in this package applies only to the Ghast-authored adapter.
Fyxer accounts, connected inboxes and calendars, hosted behavior, private
data, permissions, trademarks, privacy policy, and terms remain controlled
by Fyxer and the connected service providers.
