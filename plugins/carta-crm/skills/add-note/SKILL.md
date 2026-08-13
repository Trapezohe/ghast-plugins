---
name: add-note
description: >
  Create a standalone note in Carta CRM and optionally link it to the exact
  deal, company, contact, investor, or fundraising record the user chooses.
version: 1.0.0-ghast.1
---

# Add a Carta CRM note

Use Carta's current direct `create_note` and `link_note` MCP tools. The older
Carta v1.5.3 source skill stored text in a deal's `comment` field; Carta's
current official service now exposes standalone notes.

## Workflow

1. Resolve the exact target with a narrow search and show ambiguous matches.
2. Inspect the live `create_note` and `link_note` schemas. Collect only their
   required fields; never invent a folder, owner, entity type, or record ID.
3. Show the complete note title and body, the target record, and every link
   that will be created. Wait for explicit confirmation.
4. Call `create_note` once. If the user requested links, call `link_note` only
   for the confirmed records.
5. Read the returned note or use `fetch_note_by_id` when available, then report
   its ID, title, links, and any server URL.

Treat creation and linking as non-idempotent. If a response is interrupted or
ambiguous, search for the note and inspect its links before retrying. Do not
overwrite a deal comment as a substitute for a note.
