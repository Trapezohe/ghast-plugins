---
name: update-note
description: Find and update a standalone Carta CRM note, including explicitly requested link or unlink changes.
metadata:
  version: 1.0.0-ghast.1
---
# Update a Carta CRM note

Use Carta's current direct `search_notes`, `fetch_note_by_id`, `update_note`,
`link_note`, and `unlink_note` MCP tools. Do not route note edits through
`update_deal`; that behavior in Carta's pinned v1.5.3 skill is outdated.

## Workflow

1. Search narrowly, then resolve one exact note ID. Fetch the full current note
   and its links before proposing a change.
2. Inspect the live schemas and build a field-level diff. Preserve fields the
   user did not ask to change.
3. Show the note ID, current and proposed title/body changes, and exact link
   additions or removals. Wait for explicit confirmation.
4. Call `update_note` once with only confirmed changed fields. Apply confirmed
   `link_note` or `unlink_note` operations separately.
5. Fetch the note again and report the final content and links.

Deletion is outside this workflow. Use `delete_note` only after a separate,
fresh confirmation that names the exact note and explains that deletion is
irreversible. Never blindly retry an ambiguous write.
