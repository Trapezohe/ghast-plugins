---
name: website-fetcher
description: Use this skill when the user shares a URL or asks the assistant to read, summarize, or extract content from a webpage. Walks the model through using the built-in WebFetch tool to retrieve the page and process it without opening a browser.
version: 1.0.0
---

# Website Fetcher

Whenever the user pastes a URL or asks "what does this page say" / "summarize
this article" / "pull the headline from <url>", reach for this skill instead
of guessing what the page might contain.

## How to fetch

Call the built-in `WebFetch` tool with the URL the user provided. WebFetch
returns the page rendered as readable text (scripts and style blocks already
stripped). Treat the response as the ground truth — never paraphrase from
memory if you've actually fetched the page.

```
WebFetch(url="<the URL the user gave you>")
```

## Output guidance

- For "summarize" requests, produce a tight 3-5 bullet summary capturing
  the page's main claims. Quote key phrases verbatim when accuracy matters.
- For "extract X" requests, find the specific data point and quote it with
  the section heading it came from.
- Always cite the source URL at the end of your answer.
- If the page is paywalled, JS-rendered SPA, or returns an error, say so
  plainly — don't hallucinate the content.

## When NOT to use

- If the user is asking about a private/local resource (file path, intranet),
  use `Read` or `Bash` instead.
- If the user just wants the URL itself (e.g. "what's the GitHub URL for
  React"), don't fetch it — just answer.
