# magicpath

Search, inspect, install, create, and edit MagicPath UI components and canvas
projects through MagicPath's official pinned CLI.

## Official CLI adapter

This package contains only Ghast-authored workflow instructions,
documentation, metadata, and a generic canvas-code icon. It does not
redistribute the MagicPath CLI bundle, official agent-skill text, private
account data, credentials, access keys, generated components, hosted skills,
brand artwork, or marketplace icon.

The official npm package `magicpath-ai@2.6.1` is pinned at
tarball SHA-256 `a1fe8d745a103bf124c387044a6a66a4aea631266f3ed8d5e3c8c43d40f23ce7`, npm SHA-1
`d2d500234f9945a5689053d17b6c24f973737cf7`, and integrity
`sha512-e4CJvwmGcQZ6TtfM19ibPJMGg3jJJM5EU1qIS8oUa4qhrOMxivOu/tyyX2ThGeIvytahHokrEbZwjTWJAqr/RQ==`. Its three-file package payload contains the CLI
bundle, package metadata, and README at the hashes enforced by
`scripts/import-official-hosted-plugins.py`.

The npm registry and package metadata identify the package as
`magicpath-ai`, require Node.js 16 or newer, expose the `magicpath-ai`
binary, identify a MagicPath-domain author and maintainers, and declare MIT.
The package README also states `MIT - Jack Beoris` and identifies the
MagicPath team. The CLI package is fetched at runtime by the pinned
`npx --yes magicpath-ai@2.6.1` command; its source bundle is
not copied into this plugin.

MagicPath's official `MagicPathAI/agent-skills` repository is pinned to
signed revision `a1ced96ad9da6c65d9f57d9fef79d944f7192dfe` with Git tree
`aa1403f75088cc33f2815488ec475cf27e445b58` and complete 14-file inventory SHA-256
`09de3026dd652b76f9efc914e72d8f9d1bdc163ebfb6db8d67b46c4b4f24b7f1`. Its current Codex manifest declares
MIT, but the repository contains no LICENSE, NOTICE, or COPYING file at the
audited revision. This adapter therefore does not copy that repository's
skill text, references, image, or marketplace files.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` with complete seven-file inventory SHA-256
`21b0c4d5b51c44511e3955b6da2b058ada8c34e45b3173b635b18b8ab91da4fb`. The Codex snapshot itself declares
`UNLICENSED`; it is used only for capability comparison and none of its text
or artwork is redistributed.

## Ghast compatibility

- Run `npx --yes magicpath-ai@2.6.1 -o json info` to inspect
  authentication and workspace context. Use the official browser, headless
  code, or guest-pairing login flow directly in the user's terminal. Keep
  `MAGICPATH_TOKEN`, pairing codes, credentials, and clone access keys out of
  chat, logs, generated files, and source control.
- The official CLI searches accessible personal and team projects, lists
  projects and components, inspects component source and dependencies,
  produces preview or share links, and lists locally installed components.
- It can install React and TypeScript components into a repository. The
  included workflow requires source inspection and `add --dry-run`, then
  exact confirmation before files or dependencies are changed.
- It lists teams and members, retrieves themes and design-system variables,
  reads current canvas selection and active projects, and creates personal or
  team projects.
- Its `code` workflow reads component context, creates pending revisions,
  scaffolds bounded local workspaces, submits source and asset changes, and
  polls builds. The skill requires review and confirmation before every
  remote create or upload.
- It manages personal and team-hosted skills and supports image generation,
  canvas image operations, and one-time-key project cloning. These
  state-changing, potentially billable, or secret-bearing workflows require
  explicit scoping and confirmation.
- This is a functional superset of the audited Codex workflows for searching
  and inspecting UI components, installing React and TypeScript components,
  working with projects, teams, themes, and canvas context, and creating or
  editing canvas components from local code.
- For non-React projects, the official supported route is read-only
  `inspect`, followed by a separately reviewed translation into the target
  stack. The adapter does not misrepresent `add` as framework-neutral.
- On August 14, 2026, isolated smoke tests confirmed CLI version
  `2.6.1`, the complete top-level help surface, unauthenticated
  structured `info` output, and an empty structured `list-installed` result.
  No account login, private project access, paid image generation, component
  installation, remote create, edit, deletion, upload, or clone was run.
- The current install emits an npm warning that transitive `uuid@9.0.1` is
  deprecated. This is recorded as an upstream dependency warning; exact
  runtime and security impact should be re-evaluated when MagicPath updates
  the official package.
- A generic canvas-code icon is used because neither the unlicensed source
  repository artwork nor Codex marketplace artwork is redistributed.

The MIT license in this package applies only to the Ghast-authored adapter.
The official npm package has its own MIT declaration. MagicPath accounts,
plans, credits, hosted service behavior, projects, components, generated
assets, permissions, trademarks, privacy policy, and terms remain controlled
by MagicPath and the applicable content owners.
