---
name: bilibili-search
description: Use this skill when the user asks to search Bilibili (B 站) for videos, look up trending Bilibili content, or find a specific Bilibili video by keyword. Uses Bilibili's public web search endpoint.
version: 1.0.0
allowed-tools: [WebFetch, Bash]
---

# Bilibili Search

When the user wants to search Bilibili — "搜一下 B 站的 <keyword>",
"Bilibili 上有什么关于 <X> 的视频", "B 站今天热门" — use this skill.

## Endpoints

### Keyword search

```
https://api.bilibili.com/x/web-interface/search/all/v2?keyword=<URL-encoded>&search_type=video
```

Requires a real browser-ish User-Agent and a `Referer: https://www.bilibili.com/`
header — Bilibili's defaults block obvious bot traffic. Use `curl` via `Bash`:

```bash
curl -sS \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36' \
  -H 'Referer: https://www.bilibili.com/' \
  'https://api.bilibili.com/x/web-interface/search/all/v2?keyword=...&search_type=video'
```

### Daily ranking (all categories)

```
https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all
```

## Response shape

Top-level: `{code, message, data}`. Check `code` first:

- `0` — success, parse `data`
- `-412` — rate-limited, wait 5-10 s and tell the user; don't retry blindly
- any other non-zero — surface the `message` verbatim

For search, find the entry in `data.result` with `result_type == "video"`,
then iterate its `data[]` array. Each item has `bvid`, `title` (with
`<em>...</em>` highlights — strip them), `author`, `mid`, `duration`,
`play`, `description`, `pubdate` (unix), `pic`.

For ranking, iterate `data.list[]`. Each entry has `bvid`, `title`,
`owner.name`, `stat.view`, `stat.danmaku`, `pubdate`, `pic`.

## Output

Compact numbered list with title, uploader, view count, and the playable URL
`https://www.bilibili.com/video/<bvid>`:

> 1. **该视频标题** — UP: 某某 · 12.4万 播放 · 2 天前
>    <https://www.bilibili.com/video/BV1xx411c7mD>

## Caveats

- Bilibili's web search occasionally requires a `wbi` signature for some
  queries; if calls start returning `-412` repeatedly even after waiting,
  tell the user this is a Bilibili-side change and suggest using the web UI.
- The `pic` thumbnail URL often starts with `//` — prepend `https:` if you
  need to render it.
