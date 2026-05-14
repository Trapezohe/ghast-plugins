---
name: github-stats
description: Use this skill when the user asks about a public GitHub repository's stars, forks, issues, language, last commit, or topics; or about a GitHub user/organization's profile, follower count, or public repos. Hits the anonymous GitHub REST API.
version: 1.0.0
allowed-tools: [WebFetch, Bash]
---

# GitHub Stats

When the user references a public GitHub repo (`owner/repo`) or user/org login
and wants its public stats, use this skill instead of guessing from memory.

## Endpoints

Both are anonymous-accessible at 60 req/hr/IP. Use `WebFetch` or `curl`:

- Repo: `https://api.github.com/repos/<owner>/<repo>`
- User/org: `https://api.github.com/users/<login>`

For private/auth-required data, tell the user you can only see public info.

## What to extract

### From the repo response

`full_name`, `description`, `stargazers_count`, `forks_count`,
`open_issues_count`, `language`, `license.spdx_id`, `default_branch`,
`homepage`, `topics`, `pushed_at`, `archived`, `fork`, `html_url`.

### From the user response

`login`, `name`, `type` (User/Organization), `bio`, `company`, `location`,
`blog`, `public_repos`, `followers`, `following`, `html_url`, `created_at`.

## Output

Compact summary with the numbers the user is likely to care about, plus a
link to the repo/profile. Example:

> **vercel/next.js** — 130k ★ · 28k forks · 2.4k open issues · TypeScript · MIT
> Last push: 2 hours ago. <https://github.com/vercel/next.js>

## Failure cases

- HTTP 403 → "GitHub rate limit reached for this IP, retry in an hour."
- HTTP 404 → "Not found — check the spelling, or it might be a private repo."
- HTTP 451 → "GitHub blocked this repo (legal/DMCA), can't fetch."
