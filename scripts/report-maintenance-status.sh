#!/usr/bin/env bash
set -euo pipefail
title='Official upstream maintenance needs attention'
issue=$(gh issue list --state open --search "$title in:title" --json number,title --jq '.[] | select(.title == "Official upstream maintenance needs attention") | .number' | head -n 1)
if [[ "$FAILED" == true ]]; then
  body=$(mktemp)
  printf 'The latest maintenance run found failed checks or could not prepare a validated update.\n\nInspect the run and report artifact: %s\n\nAuthentication-required endpoint observations are not account validation.\n' "$RUN_URL" > "$body"
  if [[ -n "$issue" ]]; then gh issue edit "$issue" --body-file "$body";
  else gh issue create --title "$title" --body-file "$body"; fi
  rm "$body"
elif [[ -n "$issue" && "${FULL_SCAN:-false}" == true ]]; then
  gh issue close "$issue" --comment "Maintenance recovered: $RUN_URL"
fi
