#!/usr/bin/env bash
set -euo pipefail
branch=codex/official-upstream-maintenance
if [[ -z "$(git status --porcelain -- plugins packages plugin-catalog.json maintenance)" ]]; then
  echo 'No maintenance changes.'
  exit 0
fi
# This branch is exclusively generated; reviewer fixes belong in main's mappings.
git checkout -B "$branch"
git config user.name 'Ghast Maintenance'
git config user.email 'ghast-maintenance@users.noreply.github.com'
git add plugins packages plugin-catalog.json maintenance
# Avoid rewriting/renotifying an unchanged pending update.
if git show-ref --verify --quiet "refs/remotes/origin/$branch" && git diff --cached --quiet "origin/$branch"; then
  echo 'Existing PR already contains these changes.'
  exit 0
fi
git commit -m 'Maintain official plugin upstreams'
gh auth setup-git
git push --force-with-lease origin "HEAD:$branch"
pr=$(gh pr list --head "$branch" --state open --json number --jq '.[0].number // empty')
body=$(mktemp)
printf '%s\n\n' 'Automated official-source observations and explicitly mapped plugin updates.' 'Review maintenance/UPDATES.md for source changes, failed checks and adaptation work. Mappings preserve Ghast metadata and authentication settings. This PR requires review; no automatic merge is enabled.' > "$body"
if [[ -n "$pr" ]]; then
  gh pr edit "$pr" --body-file "$body"
else
  gh pr create --base main --head "$branch" --title 'Maintain official plugin upstreams' --body-file "$body"
fi
rm "$body"
