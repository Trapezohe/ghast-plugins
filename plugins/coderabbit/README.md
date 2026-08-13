# coderabbit

Review local code changes with CodeRabbit's official CLI and safely triage or apply unresolved CodeRabbit GitHub PR feedback through the official code-review and autofix skills.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/coderabbitai/skills` at `aa49953c4cb2590e35480637b1b6a29cf4187cfa`.

Both portable skills, the GitHub thread workflow reference, official icon, and MIT license are copied from CodeRabbit's canonical multi-agent skills repository. Ghast updates only stale CLI scope examples to the verified v0.7.2 command surface and replaces host-specific question calls with portable explicit approval language.

## Ghast compatibility

- The older Codex snapshot contains only a code-review skill. The current official MIT repository adds a guarded autofix workflow for unresolved, current CodeRabbit PR threads.
- Code review uses the separately installed official CodeRabbit CLI. It sends selected code diffs to CodeRabbit's service and requires CodeRabbit authentication.
- Ghast uses the current CLI scope flags: default tracked changes, --committed, --uncommitted, and --include-untracked. The repository's older -t examples are not retained.
- Autofix requires authenticated git and gh access, an open GitHub pull request, and CodeRabbit review threads. Every code change, commit, push, PR creation, and posted summary remains separately user-approved.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
