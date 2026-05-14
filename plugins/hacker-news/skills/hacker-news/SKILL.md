---
name: hacker-news
description: Use this skill when the user asks "what's on Hacker News", "show me HN top stories", "what's trending in tech", or asks to dig into a specific HN story or comment thread. Hits HN's public Firebase API (no auth).
version: 1.0.0
allowed-tools: [WebFetch, Bash]
---

# Hacker News

When the user wants to read Hacker News, use this skill — don't make up
headlines.

## Endpoints (no auth, JSON)

Base: `https://hacker-news.firebaseio.com/v0`

| What | URL |
| --- | --- |
| Top story IDs | `/topstories.json` |
| New story IDs | `/newstories.json` |
| Best story IDs | `/beststories.json` |
| Ask HN IDs | `/askstories.json` |
| Show HN IDs | `/showstories.json` |
| Jobs | `/jobstories.json` |
| Single item (story or comment) | `/item/<id>.json` |
| User profile | `/user/<username>.json` |

The list endpoints return a flat array of integer IDs. Fetch the first N
and resolve each with `/item/<id>.json` to get title/url/score/author/etc.

## How to use

1. Hit the list endpoint matching the user's request (default `topstories`).
2. Slice the first 5-15 IDs.
3. For each ID, `WebFetch` the `/item/<id>.json` endpoint.
4. Present as a numbered list with title, score, comment count, author,
   and the HN discussion URL: `https://news.ycombinator.com/item?id=<id>`.

For a single story dive: fetch the story, then fetch the first N kids (each
is a comment ID). Strip HTML tags from `text` fields before quoting.

## Example output

```
1. **Show HN: a thing I built** — 412 ↑, 89 comments, by alice (2h ago)
   <https://example.com>
   <https://news.ycombinator.com/item?id=12345678>
```

## Notes

- The HN API rounds scores and has no rate limit headers, but be polite
  (don't fan out to 100+ items at once).
- Stories sometimes have `text` instead of `url` (Ask/Tell HN). Show both
  in that case.
