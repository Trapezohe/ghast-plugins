#!/usr/bin/env python3
"""Import audited plugins directly from their developers' repositories."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path


PLUGIN_DIR = Path("plugins")
ASANA_MCP_URL = "https://mcp.asana.com/v2/mcp"
ASANA_MCP_RESOURCE = "https://mcp.asana.com/v2"
ASANA_TOOLS_URL = "https://developers.asana.com/docs/mcp-tools-reference.md"
ASANA_TOOLS_SHA256 = (
    "64d25be8eff00131b92e24d02bfad8db653e061408a31f169547f33d231d5ec0"
)
ASANA_INTEGRATION_URL = (
    "https://developers.asana.com/docs/integrating-with-asanas-mcp-server.md"
)
ASANA_INTEGRATION_SHA256 = (
    "58090c76a3f1fa2047d2de5297845042b4eb372d613ab5cdc39943d9e6529a03"
)
ASANA_CLIENTS_URL = (
    "https://developers.asana.com/docs/"
    "connecting-mcp-clients-to-asanas-v2-server.md"
)
ASANA_CLIENTS_SHA256 = (
    "15c6d5297fbeaccf858858bd5249624bb4d1060d0595bc682b67b06834cbcf35"
)
ASANA_OAUTH_METADATA_URL = (
    "https://mcp.asana.com/.well-known/oauth-protected-resource/v2"
)
ASANA_OAUTH_METADATA_SHA256 = (
    "346303ad06f141cdbcb982e56d6b718d59f4d4590f185208c4a3920fb5d498c8"
)
ASANA_AUTH_SERVER_URL = (
    "https://app.asana.com/.well-known/oauth-authorization-server"
)
ASANA_AUTH_SERVER_SHA256 = (
    "fc3164fa57de5e3b9a24826e88f2167cce73a04b5c6e622ea8d7bba154c696b5"
)
ASANA_MCP_REMOTE_URL = (
    "https://registry.npmjs.org/mcp-remote/-/mcp-remote-0.1.38.tgz"
)
ASANA_MCP_REMOTE_SHA256 = (
    "d8e7034ed4ddf1f1b5efd928b74e7165ab427f7b21ab86ce79bcb82a4d9560aa"
)
ASANA_MCP_LAUNCHER = """\
const fs = require("node:fs");
const path = require("node:path");
const { spawn } = require("node:child_process");
const clientFile = process.env.ASANA_OAUTH_CLIENT_FILE;
if (!clientFile) {
  console.error("Set ASANA_OAUTH_CLIENT_FILE to an absolute OAuth client JSON path.");
  process.exit(1);
}
if (!path.isAbsolute(clientFile)) {
  console.error("ASANA_OAUTH_CLIENT_FILE must be an absolute path.");
  process.exit(1);
}
let clientInfo;
let stat;
try {
  stat = fs.statSync(clientFile);
  clientInfo = JSON.parse(fs.readFileSync(clientFile, "utf8"));
} catch {
  console.error("ASANA_OAUTH_CLIENT_FILE must point to readable valid JSON.");
  process.exit(1);
}
if (
  typeof clientInfo.client_id !== "string" ||
  !clientInfo.client_id ||
  typeof clientInfo.client_secret !== "string" ||
  !clientInfo.client_secret
) {
  console.error("Asana OAuth JSON must contain client_id and client_secret.");
  process.exit(1);
}
if (process.platform !== "win32" && (stat.mode & 0o077) !== 0) {
  console.error("Protect the Asana OAuth JSON with chmod 600.");
  process.exit(1);
}
const executable = process.platform === "win32" ? "npx.cmd" : "npx";
const child = spawn(
  executable,
  [
    "--yes",
    "mcp-remote@0.1.38",
    "https://mcp.asana.com/v2/mcp",
    "3334",
    "--static-oauth-client-info",
    `@${clientFile}`,
    "--resource",
    "https://mcp.asana.com/v2",
  ],
  { stdio: "inherit" },
);
child.on("error", (error) => {
  console.error(`Unable to start Asana MCP bridge: ${error.message}`);
  process.exit(1);
});
for (const signal of ["SIGINT", "SIGTERM"]) {
  process.on(signal, () => child.kill(signal));
}
child.on("exit", (code, signal) => {
  if (signal) process.kill(process.pid, signal);
  else process.exit(code === null ? 1 : code);
});
"""
PLUGINS = {
    "airtable": {
        "directory": "airtable-skills",
        "revision": "812ee67f1fd3d76fb45ff8df40afaa0448602ba8",
        "repository": "https://github.com/airtable/skills",
        "plugin_root": "plugins/airtable",
        "manifest": ".codex-plugin/plugin.json",
        "license": "../../LICENSE.md",
        "icon": "assets/icon.svg",
        "category": "productivity",
        "mcp": ".mcp.json",
        "license_name": "MIT",
    },
    "asana": {
        "directory": "asana-cursor-marketplace-plugin",
        "revision": "caf02337846594b6af5221ea5165c1dd0d273d9b",
        "repository": "https://github.com/Asana/cursor-marketplace-plugin",
        "plugin_root": ".",
        "manifest": ".cursor-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/logo.svg",
        "category": "productivity",
        "extra_directories": ["rules"],
        "mcp_inline": {
            "mcpServers": {
                "asana": {
                    "command": "node",
                    "args": ["-e", ASANA_MCP_LAUNCHER],
                },
            },
        },
        "license_name": "MIT",
        "author": {
            "name": "Asana, Inc.",
            "url": "https://asana.com",
        },
        "homepage": "https://developers.asana.com/docs/using-asanas-mcp-server",
        "description": (
            "Read and manage Asana tasks, subtasks, comments, due dates, "
            "projects, portfolios, status updates, teams, users, and "
            "workspace priorities through Asana's official V2 MCP server."
        ),
        "compatibility_notes": [
            (
                "Ghast imports Asana's three official skills, MIT-licensed "
                "logo, and behavioral rules from the pinned Asana repository."
            ),
            (
                "Cursor-specific setup is rewritten for Asana's official "
                "Codex V2 flow through pinned mcp-remote@0.1.38. The bridge "
                "reads an absolute, permission-restricted OAuth JSON path "
                "from ASANA_OAUTH_CLIENT_FILE, so the client secret is never "
                "stored in the plugin or passed as a process argument."
            ),
            (
                "Asana's official rules are retained and merged into the "
                "active usage skill because Ghast does not execute Cursor "
                "rule files directly."
            ),
            (
                "Only https://mcp.asana.com/v2/mcp is used. The older V1 "
                "beta endpoint was retired on August 5, 2026."
            ),
        ],
    },
    "atlassian-rovo": {
        "directory": "atlassian-mcp",
        "revision": "94a30436435fb526a29f820f5f46250870eb75a0",
        "repository": "https://github.com/atlassian/atlassian-mcp-server",
        "plugin_root": ".",
        "manifest": ".claude-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/logo.svg",
        "category": "productivity",
        "mcp": ".mcp.json",
        "license_name": "Apache-2.0",
        "author": {
            "name": "Atlassian",
            "url": "https://www.atlassian.com",
        },
        "description": (
            "Search and manage Jira, Confluence, Jira Service Management, "
            "Bitbucket, Compass, and Teamwork Graph through Atlassian's "
            "official Rovo MCP server and workflow skills."
        ),
        "compatibility_notes": [
            (
                "The Codex private app mapping is replaced by Atlassian's "
                "official public Rovo MCP endpoint with OAuth 2.1 and "
                "supported API-token authentication."
            ),
            (
                "The pinned official suite adds a Jira sprint dashboard "
                "skill beyond the five workflows in the Codex snapshot."
            ),
        ],
    },
    "base44": {
        "directory": "base44-skills",
        "revision": "773a301cfb79112141add32d19c024f2bafc44ee",
        "repository": "https://github.com/base44/skills",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/base44-logo.png",
        "category": "development",
        "license_name": "MIT",
    },
    "boltz-api-cli": {
        "directory": "boltz-api-skills",
        "revision": "70e480ebb14baecfc4456b49eb8b724611470b7c",
        "repository": "https://github.com/boltz-bio/boltz-api-skills",
        "plugin_root": "plugins/boltz-api-cli",
        "manifest": ".codex-plugin/plugin.json",
        "license": "../../LICENSE",
        "icon": "assets/app-icon.png",
        "category": "research",
        "license_name": "MIT",
    },
    "cloudflare": {
        "directory": "cloudflare-skills",
        "revision": "f96bff754e428838818017f75817f0f9428acd48",
        "repository": "https://github.com/cloudflare/skills",
        "plugin_root": ".",
        "manifest": ".claude-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "logo.svg",
        "category": "development",
        "homepage": "https://workers.cloudflare.com",
        "author": {
            "name": "Cloudflare",
            "url": "https://workers.cloudflare.com",
        },
        "description": (
            "Build and operate on Cloudflare with official skills, slash "
            "commands, and five official MCP servers."
        ),
        "commands": "commands",
        "mcp": ".mcp.json",
        "license_name": "Apache-2.0",
    },
    "cloudinary": {
        "directory": "cloudinary-mcp-servers",
        "revision": "dca5790c0af2bcde291d732af05c47ad7f75d341",
        "repository": "https://github.com/cloudinary/mcp-servers",
        "plugin_root": ".",
        "manifest_inline": {
            "version": "1.0.0",
            "description": "Official Cloudinary MCP server collection.",
            "author": {
                "name": "Cloudinary",
                "url": "https://cloudinary.com",
            },
            "homepage": "https://cloudinary.com/documentation/cloudinary_llm_mcp",
        },
        "license": "LICENSE",
        "generated_icon": "./assets/icon.svg",
        "category": "creativity",
        "no_skills": True,
        "mcp_inline": {
            "mcpServers": {
                "cloudinary-asset-management": {
                    "type": "http",
                    "url": "https://asset-management.mcp.cloudinary.com/mcp",
                },
                "cloudinary-environment-config": {
                    "type": "http",
                    "url": "https://environment-config.mcp.cloudinary.com/mcp",
                },
                "cloudinary-structured-metadata": {
                    "type": "http",
                    "url": "https://structured-metadata.mcp.cloudinary.com/mcp",
                },
                "cloudinary-analysis": {
                    "type": "http",
                    "url": "https://analysis.mcp.cloudinary.com/mcp",
                },
                "cloudinary-mediaflows": {
                    "type": "http",
                    "url": "https://mediaflows.mcp.cloudinary.com/v2/mcp",
                },
            },
        },
        "license_name": "MIT",
        "description": (
            "Upload, search, transform, analyze, organize, and automate "
            "Cloudinary media through five official hosted MCP servers."
        ),
        "compatibility_notes": [
            (
                "The Codex private app mapping is replaced by Cloudinary's "
                "five official hosted MCP servers with OAuth2 or supported "
                "API-key authentication."
            ),
            (
                "A generic media-library icon is used because the official "
                "MCP collection repository does not publish a catalog icon."
            ),
        ],
    },
    "daloopa": {
        "directory": "daloopa-plugin-codex",
        "revision": "1f112599065abb7cac3489c30f9e4bb27c68ad8e",
        "repository": "https://github.com/daloopa/daloopa-plugin-codex",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "generated_icon": "./assets/icon.png",
        "category": "finance",
        "mcp": ".mcp.json",
        "license_name": "Apache-2.0",
        "compatibility_notes": [
            (
                "The official source repository does not publish an icon, so "
                "the developer-branded Codex marketplace icon is retained as "
                "catalog presentation metadata."
            ),
        ],
    },
    "expo": {
        "directory": "expo-skills",
        "revision": "dcff9e7cd61f79ee821e18b5b215d5585eaac441",
        "repository": "https://github.com/expo/skills",
        "plugin_root": "plugins/expo",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/expo.png",
        "category": "development",
        "mcp": ".mcp.json",
        "license_name": "MIT",
        "compatibility_notes": [
            (
                "The Expo telemetry status command uses Ghast's "
                "host-resolved <SKILL_DIR> placeholder instead of the "
                "Claude-only CLAUDE_PLUGIN_ROOT environment variable."
            ),
            (
                "Claude hooks and Codex-only agent metadata are not included "
                "because Ghast does not execute those client extension points."
            ),
        ],
    },
    "hyperframes": {
        "directory": "hyperframes",
        "revision": "9b0c5e85596efaf93823bf5f19b7f1d1216ca7d5",
        "repository": "https://github.com/heygen-com/hyperframes",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/icon.png",
        "category": "creativity",
        "license_name": "Apache-2.0",
    },
    "heygen": {
        "directory": "heygen-skills",
        "revision": "1bd5e4d33a028dfed3abf504c5e3dd644fb9ea8a",
        "repository": "https://github.com/heygen-com/skills",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/icon.png",
        "category": "creativity",
        "mcp": ".mcp.json",
        "license_name": "MIT",
        "skills_root": ".",
    },
    "hubspot": {
        "directory": "hubspot-agent-cli-skills",
        "revision": "71f2bdefcc0247b1f378cb98186800dc57b6f6b1",
        "repository": "https://github.com/HubSpot/agent-cli-skills",
        "plugin_root": ".",
        "manifest_inline": {
            "version": "0.11.0",
            "description": (
                "Operate HubSpot CRM data with HubSpot's official Agent CLI "
                "skills."
            ),
            "author": {
                "name": "HubSpot",
                "url": "https://www.hubspot.com",
            },
            "homepage": "https://developers.hubspot.com/docs/developer-tooling/local-development/agent-cli/guide",
        },
        "license": "LICENSE",
        "generated_icon": "./assets/icon.svg",
        "category": "productivity",
        "license_name": "Apache-2.0",
        "skills_root": ".",
        "description": (
            "Operate HubSpot CRM records, pipelines, activities, workflows, "
            "reports, data quality, sales execution, support, retention, "
            "ownership, and quote-to-cash through all 15 official Agent CLI "
            "skills."
        ),
        "compatibility_notes": [
            (
                "The Codex private app mapping is replaced by HubSpot's "
                "official Agent CLI, which authenticates through browser "
                "OAuth or a supported HUBSPOT_ACCESS_TOKEN service key."
            ),
            (
                "The beta CLI binary is installed separately from HubSpot's "
                "official distribution and is not redistributed in this "
                "Apache-2.0 skills package; this port was verified against "
                "hubspot 0.11.0."
            ),
            (
                "A generic CRM icon is used because the licensed skills "
                "repository does not publish a catalog icon and the CLI "
                "public-home repository does not grant redistribution rights "
                "for its social-preview asset."
            ),
        ],
    },
    "mixpanel-headless": {
        "directory": "mixpanel-headless",
        "revision": "6c2c2f975d51628bdbc75802fb879d4f6cb66f69",
        "repository": "https://github.com/mixpanel/mixpanel-headless",
        "plugin_root": "mixpanel-plugin",
        "manifest": ".claude-plugin/plugin.json",
        "license": "../LICENSE",
        "category": "data",
        "license_name": "MIT",
        "commands": "commands",
        "extra_directories": ["docs"],
        "generated_icon": "./assets/icon.png",
        "compatibility_notes": [
            (
                "Skill-local helper paths use Ghast's host-resolved "
                "<SKILL_DIR> placeholder instead of Claude-only variables."
            ),
            (
                "The auth slash command routes through the official mp CLI, "
                "so it remains runnable without a plugin-root environment "
                "variable."
            ),
            (
                "The setup dependency list explicitly includes click>=8.1 "
                "because the pinned official CLI imports click directly but "
                "does not declare it as a direct package dependency."
            ),
        ],
    },
    "monday-com": {
        "directory": "monday-cowork-plugin",
        "revision": "ce381e93a0a6c2ed3b9942ff1803b8078ba89389",
        "repository": "https://github.com/mondaycom/monday-claude-cowork-plugin",
        "plugin_root": ".",
        "manifest": ".claude-plugin/plugin.json",
        "license": "LICENSE",
        "generated_icon": "./assets/icon.svg",
        "category": "productivity",
        "mcp": ".mcp.json",
        "license_name": "MIT",
        "description": (
            "Manage monday.com boards, items, status reporting, docs, and "
            "WorkForms with five official workflow skills and monday.com's "
            "hosted OAuth MCP server."
        ),
        "compatibility_notes": [
            (
                "The Codex private app mapping is replaced by monday.com's "
                "official hosted OAuth MCP endpoint."
            ),
            (
                "The current official suite adds board setup, task "
                "management, project status, monday docs, and WorkForms "
                "guidance beyond the connector-only Codex snapshot."
            ),
            (
                "A generic work-management icon is used because the portable "
                "official plugin repository does not include a catalog icon."
            ),
        ],
    },
    "motherduck": {
        "directory": "motherduck-mcp",
        "revision": "b43ad1473fc5a3ca29317bf6df2db40a9a80eb90",
        "repository": "https://github.com/motherduckdb/mcp-server-motherduck",
        "plugin_root": ".",
        "manifest_inline": {
            "version": "1.0.7",
            "description": "Official MotherDuck MCP server.",
            "author": {
                "name": "MotherDuck",
                "url": "https://motherduck.com",
            },
            "homepage": "https://motherduck.com/docs/sql-reference/mcp/",
        },
        "license": "LICENSE",
        "icon": "src/mcp_server_motherduck/assets/duck_feet_square.png",
        "category": "data",
        "no_skills": True,
        "mcp_inline": {
            "mcpServers": {
                "motherduck": {
                    "type": "http",
                    "url": "https://api.motherduck.com/mcp",
                },
            },
        },
        "license_name": "MIT",
        "description": (
            "Explore, query, manage, analyze, and visualize MotherDuck data "
            "with the official hosted OAuth MCP server, including Dives."
        ),
        "compatibility_notes": [
            (
                "Ghast uses MotherDuck's official hosted MCP endpoint rather "
                "than the narrower local server so database management, "
                "iterative analysis, and Dives remain available."
            ),
            (
                "The hosted service is operated by MotherDuck and remains "
                "subject to MotherDuck account permissions, service terms, "
                "and plan limits; it is not redistributed by this package."
            ),
        ],
    },
    "neon-postgres": {
        "directory": "neon-agent-skills",
        "revision": "af27b52659c3c5bbf05d6c626b166163eb351e19",
        "repository": "https://github.com/neondatabase/agent-skills",
        "plugin_root": ".",
        "manifest": "plugin.json",
        "license": "LICENSE",
        "icon": "plugins/neon-postgres/assets/logo.svg",
        "category": "development",
        "mcp": "mcp.json",
        "license_name": "Apache-2.0",
        "description": (
            "Manage Neon Lakebase Postgres projects, branches, schemas, SQL, "
            "migrations, Auth, Object Storage, Functions, AI Gateway, and "
            "database performance with official Neon skills and MCP."
        ),
        "compatibility_notes": [
            (
                "The Codex private app mapping is replaced by Neon's official "
                "public Streamable HTTP MCP server with OAuth, API-key, "
                "project-scoped, category-scoped, and read-only modes."
            ),
        ],
    },
    "nvidia": {
        "directory": "nvidia-skills",
        "revision": "aa116673017bf75f9885edabab34d8ec883c0a3a",
        "repository": "https://github.com/NVIDIA/skills",
        "plugin_root": "plugins/nvidia-skills",
        "manifest": ".codex-plugin/plugin.json",
        "license": "../../LICENSE-APACHE",
        "additional_licenses": [
            ["../../LICENSE-CC-BY-4.0", "LICENSE-CC-BY-4.0"]
        ],
        "icon": "assets/nvidia.png",
        "category": "development",
        "license_name": "Apache-2.0 AND CC-BY-4.0",
        "skills_root": "skills",
        "skills_from_repository_root": True,
        "preserve_agent_metadata": True,
        "compatibility_notes": [
            (
                "NVIDIA's signed skill directories, agent metadata, skill "
                "cards, evaluations, and detached signatures are retained "
                "byte-for-byte so the official trust chain is not broken."
            ),
        ],
        "extra_repository_files": [
            ["nv-agent-root-cert.pem", "nv-agent-root-cert.pem"]
        ],
        "description": (
            "Complete pinned catalog of NVIDIA-verified skills for GPU "
            "acceleration, CUDA, AI, data, training, inference, robotics, "
            "Physical AI, Omniverse, simulation, networking, and more."
        ),
    },
    "remotion": {
        "directory": "remotion",
        "revision": "a23672203e00db3d9ad905b2b2088bdc6aa2f2ac",
        "repository": "https://github.com/remotion-dev/remotion",
        "plugin_root": "packages/codex-plugin",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/icon.png",
        "category": "creativity",
        "remotion_build": True,
        "license_name": "MIT",
        "compatibility_notes": [
            (
                "The official generated skill build is reproduced without "
                "Codex-only agent metadata and with preview guidance adapted "
                "to Ghast's browser."
            ),
        ],
    },
    "netlify": {
        "directory": "netlify-context",
        "revision": "47848e2d6405291caeed0b23689878ec5253bb6f",
        "repository": "https://github.com/netlify/context-and-tools",
        "plugin_root": "agent-plugin",
        "manifest": "plugin.json",
        "license": "LICENSE",
        "generated_icon": "./assets/icon.svg",
        "category": "development",
        "mcp": "mcp.json",
        "license_name": "MIT",
        "description": (
            "Build, deploy, and operate Netlify projects with official skills "
            "for Functions, Edge Functions, Blobs, Database, Identity, Image "
            "CDN, Forms, configuration, caching, AI Gateway, and deployment, "
            "plus the official Netlify MCP server."
        ),
        "compatibility_notes": [
            (
                "The Codex private app mapping is replaced by Netlify's "
                "official hosted OAuth MCP server."
            ),
            (
                "A generic deployment-service icon is used because the "
                "portable official plugin source does not include a catalog "
                "icon with explicit redistribution metadata."
            ),
        ],
    },
    "render": {
        "directory": "render",
        "revision": "14032768453fd21c57f7e3a9c0e7659a2c7dce9d",
        "repository": "https://github.com/renderinc/render-codex-plugin",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/logo.svg",
        "category": "development",
        "mcp": ".mcp.json",
        "license_name": "MIT",
    },
    "quicknode": {
        "directory": "quicknode-cli",
        "revision": "4265b0a97048d8e64dae0124013c66b8dd34533f",
        "repository": "https://github.com/quicknode/cli",
        "plugin_root": ".",
        "manifest_inline": {
            "version": "0.6.1",
            "description": "Official Quicknode CLI guide for AI agents.",
            "author": {
                "name": "Quicknode",
                "url": "https://www.quicknode.com",
            },
            "homepage": "https://www.quicknode.com/docs",
        },
        "license": "LICENSE",
        "generated_icon": "./assets/icon.svg",
        "category": "development",
        "root_skill_only": True,
        "root_skill": {
            "source": "src/commands/agent/context.md",
            "name": "quicknode",
            "description": (
                "Manage Quicknode endpoints, logs, usage, security, rate "
                "limits, billing, streams, webhooks, storage, teams, and RPC "
                "through Quicknode's official qn CLI. Use when a user asks "
                "to inspect or change Quicknode infrastructure."
            ),
        },
        "license_name": "MIT",
        "description": (
            "Manage Quicknode endpoints, logs, usage, security, rate limits, "
            "billing, streams, webhooks, storage, teams, and RPC through the "
            "official qn CLI and its official agent guide."
        ),
        "compatibility_notes": [
            (
                "The Codex private app mapping is replaced by Quicknode's "
                "official qn CLI, whose embedded agent guide covers the same "
                "infrastructure workflows and additional official services."
            ),
            (
                "The user authenticates qn outside the conversation; the "
                "Ghast skill never asks for or handles a Quicknode API key."
            ),
            (
                "A generic node-infrastructure icon is used because the "
                "official CLI repository does not publish a redistributable "
                "catalog icon."
            ),
        ],
    },
    "replayio": {
        "directory": "replayio-plugins",
        "revision": "c6cd28ff3d47f4e8e8b23040c69925ec2a820695",
        "repository": "https://github.com/replayio/plugins",
        "plugin_root": "codex/replayio",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/replayio.svg",
        "category": "development",
        "mcp": ".mcp.json",
        "license_name": "MIT",
        "extra_directories": ["scripts"],
        "additional_repository_skill_roots": [
            "codex/replay-qa/skills",
        ],
        "description": (
            "Record and inspect Replay browser runs, create verified MP4 "
            "evidence, debug uploaded recordings through Replay MCP, and run "
            "Replay QA project, bug, journey, and exploration workflows."
        ),
        "compatibility_notes": [
            (
                "Ghast does not execute Codex PostToolUse or Stop hooks, so "
                "browser recording and cleanup use the same official "
                "browser-open.js and browser-close.js scripts explicitly."
            ),
            (
                "The official Replay.io Pro and Replay QA packages are "
                "combined so Ghast retains both recording/debugging and "
                "hosted QA workflows."
            ),
        ],
    },
    "shopify": {
        "directory": "shopify-ai-toolkit",
        "revision": "cc5af6505c27939222072449278f6356857cb064",
        "repository": "https://github.com/Shopify/Shopify-AI-Toolkit",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/shopify_glyph.svg",
        "category": "development",
        "license_name": "MIT",
        "compatibility_notes": [
            (
                "Shopify's skill-local telemetry hook paths use Ghast's "
                "host-resolved <SKILL_DIR> placeholder instead of the "
                "Claude-only CLAUDE_PLUGIN_ROOT variable."
            ),
            (
                "Official Shopify scripts send documented usage telemetry by "
                "default; users can set OPT_OUT_INSTRUMENTATION=true."
            ),
        ],
    },
    "stripe": {
        "directory": "stripe-ai",
        "revision": "1953b6cce7344d880a054c42b8dd21ca3e50ebd5",
        "repository": "https://github.com/stripe/ai",
        "plugin_root": "providers/codex/plugin",
        "manifest": ".codex-plugin/plugin.json",
        "license": "../../../LICENSE",
        "icon": "assets/parallelogram.png",
        "category": "finance",
        "mcp_inline": {
            "mcpServers": {
                "stripe": {
                    "type": "http",
                    "url": "https://mcp.stripe.com",
                },
            },
        },
        "license_name": "MIT",
        "description": (
            "Build and operate Stripe payments, subscriptions, invoices, "
            "Connect platforms, apps, and API integrations with all seven "
            "official Stripe skills and Stripe's hosted OAuth MCP server."
        ),
        "compatibility_notes": [
            (
                "The official Stripe repository publishes the hosted MCP "
                "endpoint in its README while its Codex package uses a "
                "private app mapping; Ghast declares the same official "
                "OAuth endpoint directly."
            ),
        ],
    },
    "statsig": {
        "directory": "statsig-agent-skills",
        "revision": "e720bbb3fc7bb4f5d50ad6175e050138ddb1a1c6",
        "repository": "https://github.com/statsig-io/agent-skills",
        "plugin_root": ".",
        "manifest_inline": {
            "version": "1.0.0",
            "description": "Official Statsig agent skills and MCP access.",
            "author": {
                "name": "Statsig",
                "url": "https://statsig.com",
            },
            "homepage": "https://docs.statsig.com/",
        },
        "license": "LICENSE",
        "generated_icon": "./assets/icon.svg",
        "category": "development",
        "skills_root": "skills",
        "excluded_skills": ["statsig-create-cloud-metric"],
        "mcp_inline": {
            "mcpServers": {
                "statsig": {
                    "command": "npx",
                    "args": [
                        "--yes",
                        "mcp-remote@0.1.38",
                        "https://api.statsig.com/v1/mcp",
                        "--header",
                        "statsig-api-key: ${STATSIG_CONSOLE_API_KEY}",
                    ],
                },
            },
        },
        "license_name": "ISC",
        "description": (
            "Inspect and manage Statsig experiments, feature gates, dynamic "
            "configs, segments, metrics, results, audit logs, and dashboards "
            "through official skills and the official Statsig MCP server."
        ),
        "compatibility_notes": [
            (
                "The Codex private app mapping is replaced by Statsig's "
                "official Console-key MCP endpoint through pinned "
                "mcp-remote@0.1.38."
            ),
            (
                "The MCP bridge expands STATSIG_CONSOLE_API_KEY inside its "
                "own process, so the secret is not written into the plugin."
            ),
            (
                "The experimental statsig-create-cloud-metric skill is "
                "excluded because its curl example expands an API key into "
                "a process argument; core Codex capabilities remain covered "
                "and the official dashboard skill is retained."
            ),
            (
                "A generic experimentation icon is used because the official "
                "skills repository does not publish a catalog icon."
            ),
        ],
    },
    "supabase": {
        "directory": "supabase-agent-skills",
        "revision": "8331f910845103c08d51f6ca1d86ebb7d1f745e3",
        "repository": "https://github.com/supabase/agent-skills",
        "plugin_root": ".",
        "manifest": "package.json",
        "license": "LICENSE",
        "generated_icon": "./assets/icon.svg",
        "category": "development",
        "mcp_inline": {
            "mcpServers": {
                "supabase": {
                    "type": "http",
                    "url": "https://mcp.supabase.com/mcp",
                },
            },
        },
        "license_name": "MIT",
        "author": {
            "name": "Supabase",
            "url": "https://supabase.com",
        },
        "homepage": "https://supabase.com",
        "description": (
            "Develop and operate Supabase projects with the complete current "
            "official Supabase and Postgres best-practice skills plus "
            "Supabase's hosted OAuth MCP server."
        ),
        "compatibility_notes": [
            (
                "The Codex private app mapping is replaced by Supabase's "
                "official hosted OAuth 2.1 MCP server."
            ),
            (
                "Ghast declares the official unfiltered MCP endpoint so "
                "project, database, debugging, development, functions, "
                "branching, storage, and documentation tools remain "
                "available; the skills repository's root .mcp.json is a "
                "documentation-only example."
            ),
            (
                "The developer-branded Codex marketplace SVG is retained as "
                "catalog presentation metadata because the canonical skills "
                "repository publishes only a wide social-preview image."
            ),
        ],
    },
    "superhuman": {
        "directory": "superhuman-mcp-mail",
        "revision": "a83580e994604edca1cd5661a4a1865f3f39abc9",
        "repository": "https://github.com/superhuman/mcp-mail",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/superhuman-mail-small.svg",
        "category": "productivity",
        "mcp": ".mcp.json",
        "license_name": "MIT",
    },
    "temporal": {
        "directory": "temporal-codex-plugin",
        "revision": "a3fa2bdff73a93e60e1077c08bde2b682cd0f5ae",
        "repository": "https://github.com/temporalio/codex-temporal-plugin",
        "plugin_root": "plugins/temporal",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/temporal-logo.svg",
        "category": "development",
        "license_name": "MIT",
    },
    "superpowers": {
        "directory": "superpowers",
        "revision": "b36e0829c6d0140e93cfef2ca599b1b07d4a7797",
        "repository": "https://github.com/obra/superpowers",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/app-icon.png",
        "category": "development",
        "license_name": "MIT",
    },
    "twilio-developer-kit": {
        "directory": "twilio-ai",
        "revision": "d7b0f231468cd9a6a0bab9ebcde8c1a5c9220bba",
        "repository": "https://github.com/twilio/ai",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "category": "development",
        "license_name": "MIT",
        "recursive_skills": True,
        "generated_icon": "./assets/icon.svg",
        "frontmatter_overrides": {
            "twilio-agent-connect": (
                "Integrate agentic applications with Twilio Agent Connect "
                "across identity, memory, orchestration, Voice, SMS, RCS, "
                "WhatsApp, and Chat."
            )
        },
        "compatibility_notes": [
            (
                "A minimal Ghast-compatible frontmatter block is added to "
                "twilio-agent-connect because that official skill is the "
                "only source skill without one."
            ),
        ],
    },
    "hugging-face": {
        "directory": "huggingface-skills",
        "revision": "ec0108293521ef698e451ec044e8b4feba6b732b",
        "repository": "https://github.com/huggingface/skills",
        "plugin_root": ".",
        "manifest": ".claude-plugin/plugin.json",
        "license": "LICENSE",
        "generated_icon": "./assets/icon.svg",
        "category": "development",
        "mcp": ".mcp.json",
        "license_name": "Apache-2.0",
        "additional_repository_skill_roots": [
            "hf-mcp/skills",
        ],
        "description": (
            "Explore and manage Hugging Face models, datasets, Spaces, jobs, "
            "papers, evaluations, training, Gradio apps, local models, and "
            "Hub workflows with the complete official skill catalog and "
            "official Hugging Face MCP server."
        ),
        "compatibility_notes": [
            (
                "The Codex private app mapping is replaced by Hugging Face's "
                "official public MCP endpoint with browser login or bearer "
                "token authentication."
            ),
            (
                "A generic machine-learning icon is used because the skills "
                "repository does not publish a small catalog icon."
            ),
        ],
    },
    "vercel": {
        "directory": "vercel-plugin",
        "revision": "11c32588786a9d49791372657433b88d49561874",
        "repository": "https://github.com/vercel/vercel-plugin",
        "plugin_root": ".",
        "manifest": ".claude-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/vercel.svg",
        "category": "development",
        "command_files": [
            "commands/bootstrap.md",
            "commands/deploy.md",
            "commands/env.md",
            "commands/status.md",
        ],
        "mcp": ".mcp.json",
        "license_name": "Apache-2.0",
        "compatibility_notes": [
            (
                "Vercel's Claude hooks and specialist-agent declarations are "
                "not included because Ghast does not execute those client "
                "extension points; all official skills, four user commands, "
                "and the public Vercel MCP server are retained."
            ),
        ],
    },
    "wix": {
        "directory": "wix-skills",
        "revision": "d9b73923907f91989335cf4f26dce52095faeea4",
        "repository": "https://github.com/wix/skills",
        "plugin_root": ".",
        "manifest": ".codex-plugin/plugin.json",
        "license": "LICENSE",
        "icon": "assets/logo.svg",
        "category": "development",
        "mcp": ".mcp.json",
        "license_name": "MIT",
    },
    "zoom": {
        "directory": "zoom-skills",
        "revision": "1858eadc17d9bd0d1279ce7f66304362a774e3b4",
        "repository": "https://github.com/zoom/skills",
        "plugin_root": ".",
        "manifest": ".claude-plugin/plugin.json",
        "license": "LICENSE",
        "generated_icon": "./assets/icon.svg",
        "category": "development",
        "mcp": ".mcp.json",
        "license_name": "MIT",
        "skills_root": "skills",
        "root_skill": {
            "source": "skills/SKILL.md",
            "name": "zoom-skills",
        },
        "description": (
            "Build Zoom integrations and access meeting search, transcripts, "
            "recordings, assets, Team Chat, Canvas, Tasks, Whiteboard, and "
            "Revenue Accelerator through Zoom's official skills and MCP "
            "servers."
        ),
        "author": {
            "name": "Zoom",
            "url": "https://github.com/zoom",
        },
        "homepage": "https://developers.zoom.us/",
        "compatibility_notes": [
            (
                "The older Codex app mapping is replaced by Zoom's seven "
                "official public Streamable HTTP MCP servers."
            ),
            (
                "A generic video-service catalog icon is used because Zoom's "
                "official MCP registry states that its logo is proprietary "
                "and does not grant redistribution rights."
            ),
        ],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        required=True,
        help="Directory containing the pinned official repository checkouts.",
    )
    return parser.parse_args()


def main() -> int:
    source_root = parse_args().source_root.resolve()
    verify_asana_evidence()
    for name, config in PLUGINS.items():
        import_plugin(name, config, source_root)
    print(f"imported {len(PLUGINS)} plugins from official developer repositories")
    return 0


def import_plugin(name: str, config: dict, source_root: Path) -> None:
    repository = source_root / config["directory"]
    actual_remote = normalized_git_remote(repository)
    expected_remote = normalized_repository_url(config["repository"])
    if actual_remote != expected_remote:
        raise ValueError(
            f"{repository}: expected origin {config['repository']}, "
            f"found {actual_remote}"
        )
    revision = git_revision(repository)
    if revision != config["revision"]:
        raise ValueError(
            f"{repository}: expected revision {config['revision']}, found {revision}"
        )

    plugin_root = repository / config["plugin_root"]
    if config.get("manifest"):
        source_manifest = json.loads(
            (plugin_root / config["manifest"]).read_text()
        )
    else:
        source_manifest = config["manifest_inline"]
    license_path = plugin_root / config["license"]
    if not license_path.is_file():
        raise ValueError(f"{license_path}: license is missing")

    with tempfile.TemporaryDirectory(prefix=f".{name}-", dir=PLUGIN_DIR) as temp:
        staging = Path(temp)
        if not config.get("no_skills"):
            skills_target = staging / "skills"
            if config.get("root_skill_only"):
                skills_target.mkdir()
                copy_root_skill(
                    repository,
                    skills_target,
                    config["root_skill"],
                )
            elif config.get("remotion_build"):
                build_remotion_skills(repository, skills_target)
            else:
                skills_root = (
                    repository / config["skills_root"]
                    if config.get("skills_from_repository_root")
                    else plugin_root / config.get("skills_root", "skills")
                )
                copy_skill_tree(
                    skills_root,
                    skills_target,
                    recursive=config.get("recursive_skills", False),
                    preserve_agent_metadata=config.get(
                        "preserve_agent_metadata", False
                    ),
                    frontmatter_overrides=config.get(
                        "frontmatter_overrides", {}
                    ),
                )
                for excluded_skill in config.get("excluded_skills", []):
                    excluded_path = skills_target / excluded_skill
                    if not excluded_path.is_dir():
                        raise ValueError(
                            f"{excluded_path}: excluded skill is missing"
                        )
                    shutil.rmtree(excluded_path)
                for additional_root in config.get(
                    "additional_repository_skill_roots", []
                ):
                    copy_skill_tree(
                        repository / additional_root,
                        skills_target,
                        recursive=False,
                        preserve_agent_metadata=False,
                        frontmatter_overrides={},
                        merge=True,
                    )
                if config.get("root_skill"):
                    copy_root_skill(
                        repository,
                        skills_target,
                        config["root_skill"],
                    )

        if config.get("commands"):
            shutil.copytree(
                plugin_root / config["commands"],
                staging / "commands",
                copy_function=shutil.copy2,
            )
        elif config.get("command_files"):
            commands_target = staging / "commands"
            commands_target.mkdir()
            for command_name in config["command_files"]:
                command_source = plugin_root / command_name
                if not command_source.is_file():
                    raise ValueError(
                        f"{command_source}: declared command is missing"
                    )
                shutil.copy2(command_source, commands_target / command_source.name)
        if config.get("mcp"):
            shutil.copy2(plugin_root / config["mcp"], staging / ".mcp.json")
        elif config.get("mcp_inline"):
            (staging / ".mcp.json").write_text(
                json.dumps(
                    config["mcp_inline"],
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n"
            )
        for directory in config.get("extra_directories", []):
            shutil.copytree(
                plugin_root / directory,
                staging / directory,
                copy_function=shutil.copy2,
            )

        apply_ghast_compatibility(name, staging)

        shutil.copy2(license_path, staging / "LICENSE")
        for source_name, target_name in config.get("additional_licenses", []):
            shutil.copy2(plugin_root / source_name, staging / target_name)
        for source_name, target_name in config.get(
            "extra_repository_files", []
        ):
            shutil.copy2(repository / source_name, staging / target_name)

        if config.get("icon"):
            icon_source = plugin_root / config["icon"]
            icon_target = staging / "assets" / f"icon{icon_source.suffix.lower()}"
            icon_target.parent.mkdir()
            shutil.copy2(icon_source, icon_target)
            icon_manifest_path = f"./{icon_target.relative_to(staging)}"
        else:
            icon_manifest_path = config["generated_icon"]

        manifest = {
            "name": name,
            "version": f"{source_manifest.get('version', '1.0.0')}-ghast.1",
            "description": config.get(
                "description", source_manifest["description"]
            ),
            "category": config["category"],
            "author": config.get("author", source_manifest.get("author")),
            "homepage": config.get(
                "homepage",
                source_manifest.get("homepage", config["repository"]),
            ),
            "repository": config["repository"],
            "upstreamRevision": revision,
            "upstreamPath": config["plugin_root"],
            "license": config["license_name"],
            "icon": icon_manifest_path,
        }
        if not config.get("no_skills"):
            manifest["skills"] = "./skills/"
        if config.get("commands") or config.get("command_files"):
            manifest["commands"] = "./commands/"
        if config.get("mcp") or config.get("mcp_inline"):
            manifest["mcpServers"] = "./.mcp.json"

        manifest_dir = staging / ".ghast-plugin"
        manifest_dir.mkdir()
        (manifest_dir / "plugin.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        )
        (staging / "README.md").write_text(
            render_readme(name, source_manifest, manifest, config)
        )

        target = PLUGIN_DIR / name
        if target.exists():
            shutil.rmtree(target)
        staging.rename(target)


def copy_skill_tree(
    source: Path,
    target: Path,
    *,
    recursive: bool,
    preserve_agent_metadata: bool,
    frontmatter_overrides: dict[str, str],
    merge: bool = False,
) -> None:
    if not source.is_dir():
        raise ValueError(f"{source}: skills directory is missing")
    target.mkdir(exist_ok=merge)
    copied = 0
    source_skills = (
        sorted(path.parent for path in source.rglob("SKILL.md"))
        if recursive
        else sorted(path for path in source.iterdir() if path.is_dir())
    )
    names = [path.name for path in source_skills if (path / "SKILL.md").is_file()]
    if len(names) != len(set(names)):
        raise ValueError(f"{source}: recursive skill names are not unique")
    for source_skill in source_skills:
        if not (source_skill / "SKILL.md").is_file():
            continue
        target_skill = target / source_skill.name
        if target_skill.exists():
            raise ValueError(
                f"{source_skill}: duplicate imported skill {target_skill.name}"
            )
        shutil.copytree(
            source_skill,
            target_skill,
            copy_function=shutil.copy2,
            ignore=(
                None
                if preserve_agent_metadata
                else shutil.ignore_patterns(
                    "openai.yaml", "__pycache__", "*.pyc"
                )
            ),
        )
        if not preserve_agent_metadata:
            remove_empty_directories(target_skill)
        ensure_skill_frontmatter(
            target_skill / "SKILL.md",
            skill_name=source_skill.name,
            description=frontmatter_overrides.get(source_skill.name),
        )
        copied += 1
    if not copied:
        raise ValueError(f"{source}: no valid skills")


def copy_root_skill(
    repository: Path, target: Path, root_skill: dict
) -> None:
    source = repository / root_skill["source"]
    if not source.is_file():
        raise ValueError(f"{source}: root skill is missing")
    target_skill = target / root_skill["name"]
    if target_skill.exists():
        raise ValueError(f"{target_skill}: duplicate imported root skill")
    target_skill.mkdir()
    target_path = target_skill / "SKILL.md"
    shutil.copy2(source, target_path)
    ensure_skill_frontmatter(
        target_path,
        skill_name=root_skill["name"],
        description=root_skill.get("description"),
    )


def ensure_skill_frontmatter(
    skill_path: Path, *, skill_name: str, description: str | None
) -> None:
    text = skill_path.read_text()
    if text.startswith("---\n") and text.find("\n---\n", 4) >= 0:
        return
    if not description:
        raise ValueError(
            f"{skill_path}: official skill lacks frontmatter and no "
            "compatibility description is configured"
        )
    frontmatter = (
        "---\n"
        f"name: {skill_name}\n"
        "description: >-\n"
        f"  {description}\n"
        "---\n\n"
    )
    skill_path.write_text(frontmatter + text)


def apply_ghast_compatibility(name: str, staging: Path) -> None:
    if name == "expo":
        rewrite_text(
            staging / "skills/expo-skill-feedback/SKILL.md",
            {
                '"${CLAUDE_PLUGIN_ROOT}/skills/expo-skill-feedback/scripts/telemetry.cjs"': (
                    '"<SKILL_DIR>/scripts/telemetry.cjs"'
                )
            },
        )
    elif name == "asana":
        (staging / "skills/asana-setup/SKILL.md").write_text(
            render_asana_setup_skill()
        )
        (staging / "skills/asana-mcp-troubleshooting/SKILL.md").write_text(
            render_asana_troubleshooting_skill()
        )
        usage_skill = staging / "skills/asana-usage/SKILL.md"
        rewrite_text(
            usage_skill,
            {
                (
                    "Best practices for using Asana MCP tools in Cursor."
                ): "Best practices for using Asana MCP tools in Ghast.",
            },
        )
        usage_skill.write_text(
            usage_skill.read_text().rstrip()
            + "\n\n"
            + render_asana_usage_appendix()
        )
    elif name == "mixpanel-headless":
        for markdown in (staging / "skills").rglob("*.md"):
            rewrite_text(
                markdown,
                {"${CLAUDE_SKILL_DIR}": "<SKILL_DIR>"},
                require_all=False,
            )
        rewrite_text(
            staging / "skills/setup/SKILL.md",
            {
                (
                    "python3 <SKILL_DIR>/../mixpanelyst/scripts/"
                    "auth_manager.py session"
                ): "mp session --format json",
                (
                    "python3 <SKILL_DIR>/../mixpanelyst/scripts/"
                    "auth_manager.py account test"
                ): "mp account test",
            },
        )
        rewrite_text(
            staging / "skills/setup/scripts/setup.sh",
            {
                (
                    "DEPS=(pandas numpy matplotlib seaborn 'networkx>=3.0' "
                    "'anytree>=2.8.0' scipy)"
                ): (
                    "DEPS=(pandas numpy matplotlib seaborn 'networkx>=3.0' "
                    "'anytree>=2.8.0' 'click>=8.1' scipy)"
                )
            },
        )
        (staging / "commands/auth.md").write_text(
            render_mixpanel_auth_command()
        )
    elif name == "shopify":
        for markdown in (staging / "skills").rglob("*.md"):
            rewrite_text(
                markdown,
                {"$CLAUDE_PLUGIN_ROOT/scripts": "<SKILL_DIR>/scripts"},
                require_all=False,
            )
    elif name == "statsig":
        rewrite_text(
            staging / "skills/statsig/SKILL.md",
            {
                """## Setup Statsig MCP
Important: you must check to see if the Statsig MCP server is running. If not, tell the user how to configure Statsig:

Add this to `~/.codex/config.toml` and replace the API key:

```toml
[mcp_servers.statsig]
command = "npx"
args = ["--yes", "mcp-remote", "https://api.statsig.com/v1/mcp", "--header", "statsig-api-key: console-YOUR-CONSOLE-API-KEY"]
trust_level = "trusted"
```

Use a Statsig Console API key with the permissions you need (read-only for viewing, write for changes). Statsig API keys can be created under Settings -> Keys & Environments. Restart Codex after editing the config.
""": """## Statsig MCP setup

This plugin already declares the official Statsig MCP bridge. It reads
`STATSIG_CONSOLE_API_KEY` from the host environment. Never ask for, print,
log, or write the key. Use a Console API key with only the permissions needed
for the requested read or write workflow. If the MCP is unavailable, ask the
user to set the environment variable and reload the active Ghast profile.
"""
            },
        )
        rewrite_text(
            staging / "skills/statsig/references/statsig-mcp.md",
            {
                """## Setup (Codex CLI / IDE extension)

See `statsig-mcp/SKILL.md` for the Codex MCP config snippet and API key notes.
""": """## Setup

See `../SKILL.md` for the Ghast MCP environment and API key guidance.
"""
            },
        )
    elif name == "replayio":
        replayio_skill = staging / "skills/replayio/SKILL.md"
        rewrite_text(
            replayio_skill,
            {
                (
                    "The Codex `Stop` hook also runs close/upload cleanup as "
                    "a safety net when a turn ends."
                ): (
                    "Ghast does not execute Codex hooks, so always run "
                    "`browser-close.js` explicitly before reporting results."
                ),
                "When Codex lists this skill": "When Ghast lists this skill",
                (
                    "| `replayio_browser_lifecycle_hook.sh` | Codex post-tool "
                    "hook that starts capture after raw `playwright-cli open` "
                    "and cleans up after raw close commands. |"
                ): (
                    "| `replayio_browser_lifecycle_hook.sh` | Upstream Codex "
                    "hook helper retained for source completeness; Ghast does "
                    "not invoke it automatically. |"
                ),
                (
                    "| `close_browsers_and_upload.sh` | Codex stop hook that "
                    "closes lingering sessions and uploads pending Replay "
                    "recordings. |"
                ): (
                    "| `close_browsers_and_upload.sh` | Manual fallback that "
                    "closes lingering sessions and uploads pending Replay "
                    "recordings. |"
                ),
                (
                    "The Codex `Stop` hook still attempts pending Replay "
                    "uploads as a safety net, but video capture is only "
                    "automatic for lifecycle-script browser sessions."
                ): (
                    "Ghast has no automatic Stop hook; lifecycle-script "
                    "browser sessions must be closed explicitly."
                ),
                (
                    "If you forget, the Codex `Stop` hook attempts to stop "
                    "capture, close lingering sessions, transcode video, and "
                    "upload pending Replay recordings as a safety net."
                ): (
                    "Ghast has no automatic cleanup hook, so run "
                    "`browser-close.js` or `close_browsers_and_upload.sh` "
                    "before ending the task."
                ),
                (
                    "Let the Codex `Stop` hook run cleanup only as a safety "
                    "net, not as the main way to get artifact paths."
                ): (
                    "Run explicit cleanup and capture its artifact paths "
                    "before reporting the result."
                ),
                (
                    "In Codex memory-enabled hosts, write the note only "
                    "through the allowed memory-update path; do not edit "
                    "memory registry files directly."
                ): (
                    "Use only the host-supported memory mechanism; do not "
                    "edit memory registry files directly."
                ),
                (
                    "Codex connects to the Replay HTTP MCP server configured "
                    "in `.mcp.json`; the connected Replay app id remains "
                    "available in `.app.json` for app-level authentication "
                    "and compatibility."
                ): (
                    "Ghast connects directly to the official Replay HTTP MCP "
                    "server configured in `.mcp.json`."
                ),
            },
        )
        rewrite_text(
            staging / "skills/replayio/references/workflows.md",
            {
                (
                    "Use the Codex stop hook only as a cleanup safety net."
                ): (
                    "Run browser-close.js explicitly and use "
                    "close_browsers_and_upload.sh only as a manual fallback."
                ),
            },
        )
        replay_qa_skill = staging / "skills/replay-qa/SKILL.md"
        rewrite_text(
            replay_qa_skill,
            {
                "from Codex": "from Ghast",
                "This Codex package": "This Ghast package",
                "When Codex lists this skill": "When Ghast lists this skill",
            },
        )
    elif name == "quicknode":
        quicknode_skill = staging / "skills/quicknode/SKILL.md"
        rewrite_text(
            quicknode_skill,
            {
                "# qn — usage guide for agents": """## Ghast runtime rules

- Use the official `qn` executable. Check `qn --version` before account work.
  If it is unavailable, ask the user to install it from Quicknode's official
  release channels; on macOS the documented command is
  `brew install quicknode/tap/qn`.
- Authentication is user-managed. Never ask for, print, store, or pass a
  Quicknode API key. Ask the user to run `qn auth login` themselves, then
  verify only with `qn auth whoami`.
- Before any create, update, pause, resume, archive, delete, security,
  rate-limit, billing-affecting, wallet, or paid-RPC action, show the planned
  command and obtain explicit confirmation. Inspect current state first and
  verify the result afterward.
- Never generate or fund a wallet, buy credits, open or top up a payment
  channel, or use `--x402`, `--mpp`, `--x402-drawdown`, or `--mpp-session`
  unless the user explicitly requests that exact paid workflow and confirms
  the amount, asset, and network. Prefer test networks when available.
- Run `qn agent context` after installation and prefer its version-matched
  guide if it differs from this pinned reference.

# qn — usage guide for agents""",
                "qn v{{VERSION}}": "qn v0.6.1",
            },
        )
    elif name == "zoom":
        root_skill = staging / "skills/zoom-skills/SKILL.md"
        text = root_skill.read_text()
        text = re.sub(
            r"\]\((?!https?://|#|/)([^)]+)\)",
            r"](../\1)",
            text,
        )
        root_skill.write_text(text)


def rewrite_text(
    path: Path,
    replacements: dict[str, str],
    *,
    require_all: bool = True,
) -> None:
    text = path.read_text()
    for old, new in replacements.items():
        if require_all and old not in text:
            raise ValueError(f"{path}: expected compatibility marker is missing: {old}")
        text = text.replace(old, new)
    path.write_text(text)


def render_asana_setup_skill() -> str:
    return """---
name: asana-setup
description: Detect and configure Asana V2 MCP credentials for Ghast. Run before using Asana when the connection is not already active.
---

# Asana MCP Setup

This plugin connects to Asana's official V2 MCP server through the Codex flow
documented by Asana. V2 requires a pre-registered Asana MCP app and does not
support dynamic client registration.

## Security boundary

- Never ask the user to paste a client ID, client secret, access token, or
  refresh token into conversation.
- Never print, log, or inspect credential values.
- The plugin reads only `ASANA_OAUTH_CLIENT_FILE`, which must be an absolute
  path to a user-managed JSON file outside the project and plugin.
- The file must contain `client_id` and `client_secret` and should be readable
  only by the current user.

## Setup

1. Ask the user to open Asana's developer console and create an **MCP app**.
2. Configure the exact redirect URI:

   `http://localhost:3334/oauth/callback`

3. Configure the app for the intended workspace or for any workspace.
4. Ask the user to create a private JSON file outside the repository:

```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

5. On macOS or Linux, ask the user to protect it with:

```bash
chmod 600 /absolute/path/to/asana-mcp-oauth.json
```

6. Ask the user to set the file path in the host environment:

```bash
export ASANA_OAUTH_CLIENT_FILE="/absolute/path/to/asana-mcp-oauth.json"
```

7. Reload the active Ghast profile after setting the variable.

## Safe verification

Check only whether the variable and file are present. Do not print the file:

```bash
test -n "$ASANA_OAUTH_CLIENT_FILE" &&
test -f "$ASANA_OAUTH_CLIENT_FILE" &&
echo "Asana OAuth client file is configured"
```

The plugin launcher validates that the path is absolute, the JSON has both
required keys, and Unix permissions are restricted. It passes only the file
path to pinned `mcp-remote@0.1.38`; the secret does not enter the process
arguments.

After the browser authorization succeeds, verify with `get_me` or
`get_my_tasks`. Do not create or modify a record merely to test connectivity.
"""


def render_asana_troubleshooting_skill() -> str:
    return """---
name: asana-mcp-troubleshooting
description: Diagnose Asana V2 MCP connection, OAuth app, credential-file, workspace, and tool availability failures in Ghast.
---

# Asana MCP Troubleshooting

Work through these checks in order and stop at the first failure.

## 1. Confirm the supported endpoint

The plugin must use `https://mcp.asana.com/v2/mcp`. Do not fall back to the
deprecated V1 beta endpoint; Asana retired it on August 5, 2026.

An unauthenticated request should return HTTP 401 with an Asana Bearer
challenge. A timeout or DNS failure indicates a local network problem.

## 2. Confirm the credential file without exposing it

Never run `cat`, `echo $ASANA_CLIENT_SECRET`, or any command that displays the
JSON. Check only:

```bash
test -n "$ASANA_OAUTH_CLIENT_FILE" || echo "ASANA_OAUTH_CLIENT_FILE is unset"
test -f "$ASANA_OAUTH_CLIENT_FILE" || echo "Asana OAuth client file is missing"
```

The path must be absolute. On macOS and Linux, repair overly broad permissions
with `chmod 600 /absolute/path/to/asana-mcp-oauth.json`.

If the launcher says required keys are missing, ask the user to correct the
file themselves. Do not request its contents.

## 3. Confirm the Asana MCP app

- The app type must be **MCP app**, not a standard API app.
- The redirect URI must exactly match
  `http://localhost:3334/oauth/callback`.
- The app must be distributed to the selected workspace or to any workspace.
- The client ID and secret must belong to the same app.
- If the secret was rotated, the private JSON file must be updated by the
  user and the active profile reloaded.

## 4. Confirm authorization and workspace scope

The browser flow asks the user to select and authorize one workspace. Tokens
are workspace-scoped. A different workspace requires a separate authorization
session.

Enterprise administrators can block the MCP app. Report the exact Asana
policy or permission error and let the user request administrator approval.

## 5. Confirm local prerequisites

The compatibility bridge requires Node.js, npm, and pinned
`mcp-remote@0.1.38`. Check `node --version` and `npm --version`; do not install
or upgrade software without the user's approval.

OAuth tokens are managed by `mcp-remote` under the user's local MCP auth
storage. Do not read or display those files. Clear stored authorization only
when the user explicitly asks to reconnect or switch accounts.

## 6. Confirm tools

After authorization, use `get_me` or `get_my_tasks` for a read-only test. If
tools are missing, reload the active profile and inspect the concrete launcher
error. Do not create, update, comment on, or delete Asana work as a connection
test.
"""


def render_asana_usage_appendix() -> str:
    return """## Ghast and Asana V2 rules

- Never expose raw Asana GIDs in conversational responses when a human-readable
  name is available.
- Prefer the most specific tool. Use `search_objects` only to resolve unknown
  identifiers, and use `get_my_tasks` for "what is on my plate" requests.
- Read current state before changing tasks, dependencies, project membership,
  followers, custom fields, completion, dates, assignees, or parent links.
- Obtain explicit confirmation before every create, update, comment, project
  status update, archive, or delete operation. Show the target names and exact
  proposed values first.
- `delete_task` is permanent and can also remove subtasks that are not members
  of another project. Require a fresh, explicit confirmation immediately
  before calling it.
- For up to 50-task batch creates or updates, list every affected task and
  field change before confirmation. Split vague "do everything" requests into
  reviewable steps.
- Use comments only for discussion or context, not for events Asana already
  records automatically. Show the full proposed comment before posting it.
- Interactive preview tools may be unavailable outside Claude and ChatGPT.
  In Ghast, perform the equivalent preview in conversation and call standard
  write tools only after confirmation.
- Do not blindly retry a failed write. Read current state first to avoid
  duplicate tasks, comments, projects, or status updates.
- Advanced `search_tasks` requires an eligible Premium workspace. Fall back to
  filtered `get_tasks` when the service reports that limitation.
- Access is limited to the authorized user's existing permissions and the
  workspace selected during OAuth. Never claim broader visibility.
"""


def fetch_bytes(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def verify_asana_evidence() -> None:
    tools_bytes = fetch_bytes(ASANA_TOOLS_URL)
    if sha256_bytes(tools_bytes) != ASANA_TOOLS_SHA256:
        raise ValueError(
            "Asana MCP tools documentation changed; re-audit required"
        )
    tools = tools_bytes.decode("utf-8")
    for marker in (
        "The Asana V2 MCP server exposes a set of tools",
        "Read tools",
        "Write tools",
        "Interactive tools",
        "search_objects",
        "get_task",
        "get_tasks",
        "get_my_tasks",
        "search_tasks",
        "get_project",
        "get_projects",
        "get_portfolio",
        "get_portfolios",
        "get_items_for_portfolio",
        "get_status_overview",
        "get_attachments",
        "get_user",
        "get_me",
        "get_users",
        "get_teams",
        "get_agent",
        "get_workspace_agents",
        "create_tasks",
        "create_project",
        "update_tasks",
        "delete_task",
        "add_comment",
        "create_project_status_update",
        "create_task_preview",
        "create_project_preview",
        "search_tasks_preview",
    ):
        if marker not in tools:
            raise ValueError(f"Asana MCP tools evidence is missing {marker!r}")

    integration_bytes = fetch_bytes(ASANA_INTEGRATION_URL)
    if sha256_bytes(integration_bytes) != ASANA_INTEGRATION_SHA256:
        raise ValueError(
            "Asana MCP integration documentation changed; re-audit required"
        )
    integration = integration_bytes.decode("utf-8")
    for marker in (
        ASANA_MCP_URL,
        ASANA_MCP_RESOURCE,
        "Wed 5 Aug 2026",
        "Dynamic client registration is not supported",
        "client id and client secret",
    ):
        if marker not in integration:
            raise ValueError(
                f"Asana MCP integration evidence is missing {marker!r}"
            )

    clients_bytes = fetch_bytes(ASANA_CLIENTS_URL)
    if sha256_bytes(clients_bytes) != ASANA_CLIENTS_SHA256:
        raise ValueError(
            "Asana MCP client documentation changed; re-audit required"
        )
    clients = clients_bytes.decode("utf-8")
    for marker in (
        "## Codex",
        "mcp-remote@latest",
        "--static-oauth-client-info",
        "http://localhost:3334/oauth/callback",
        "The `@` prefix tells `mcp-remote` to read the client credentials",
        "This keeps your client secret out of the process command line",
    ):
        if marker not in clients:
            raise ValueError(
                f"Asana Codex integration evidence is missing {marker!r}"
            )

    metadata = json.loads(fetch_bytes(ASANA_OAUTH_METADATA_URL))
    if canonical_json_sha256(metadata) != ASANA_OAUTH_METADATA_SHA256:
        raise ValueError(
            "Asana OAuth protected-resource metadata changed; re-audit required"
        )
    if metadata.get("resource") != ASANA_MCP_URL:
        raise ValueError("Asana OAuth resource URI changed")
    if metadata.get("authorization_servers") != ["https://app.asana.com"]:
        raise ValueError("Asana OAuth authorization server changed")
    if metadata.get("bearer_methods_supported") != ["header"]:
        raise ValueError("Asana OAuth bearer method changed")

    auth_server = json.loads(fetch_bytes(ASANA_AUTH_SERVER_URL))
    if canonical_json_sha256(auth_server) != ASANA_AUTH_SERVER_SHA256:
        raise ValueError(
            "Asana OAuth authorization metadata changed; re-audit required"
        )
    if auth_server.get("issuer") != "https://app.asana.com":
        raise ValueError("Asana OAuth issuer changed")
    grants = auth_server.get("grant_types_supported", [])
    if "authorization_code" not in grants or "refresh_token" not in grants:
        raise ValueError("Asana OAuth grant support changed")
    if auth_server.get("code_challenge_methods_supported") != ["S256"]:
        raise ValueError("Asana OAuth server no longer requires PKCE S256")
    if "registration_endpoint" in auth_server:
        raise ValueError("Asana unexpectedly enabled dynamic registration")

    bridge = fetch_bytes(ASANA_MCP_REMOTE_URL)
    if sha256_bytes(bridge) != ASANA_MCP_REMOTE_SHA256:
        raise ValueError(
            "Pinned mcp-remote package changed; re-audit required"
        )


def render_mixpanel_auth_command() -> str:
    return """---
name: mixpanel-headless:auth
description: Manage Mixpanel authentication, accounts, projects, workspaces, targets, and bridge status through the official mp CLI.
argument-hint: [session|login|account|project|workspace|target|bridge] [...]
---

# Mixpanel Authentication Management

Use the official `mp` CLI installed by `mixpanel-headless`. Parse
`$ARGUMENTS`, run the matching command below, and present the result
conversationally. Never invent an account, project, workspace, or target ID.

## Security rules

- Never ask for passwords, API secrets, or bearer tokens in conversation.
- Never pass a secret as a CLI argument.
- Prefer `mp login` for interactive OAuth.
- For service accounts, instruct the user to run `mp account add` themselves;
  it prompts with hidden input or accepts `--secret-stdin`.
- Use environment variables for non-interactive credentials.

## Routing

With no arguments or `session`, run:

```bash
mp session --format json
```

For `login`, tell the user the browser flow may open, then run:

```bash
mp login
```

Useful login flags are `--name`, `--region us|eu|in`, `--project`,
`--service-account`, `--token-env`, `--secret-stdin`, and `--no-browser`.

### Accounts

```bash
mp account list --format json
mp account show <NAME>
mp account use <NAME>
mp account test <NAME>
mp account login <NAME>
mp account logout <NAME>
```

For account creation, guide the user to one of these official flows:

```bash
mp login --name <NAME> --region <REGION>
mp account add <NAME> --type service_account --username <USERNAME> --project <PROJECT_ID> --region <REGION>
mp account add <NAME> --type oauth_token --token-env <ENV_VAR> --project <PROJECT_ID> --region <REGION>
```

Do not run `account add` on the user's behalf when it would require handling a
secret. After the user completes it, verify with `mp account test <NAME>`.

### Projects

```bash
mp project list --format json
mp project show
mp project use <PROJECT_ID>
```

If `project use` has no ID, list projects first and ask the user to choose.

### Workspaces

```bash
mp workspace list --format json
mp workspace show
mp workspace use <WORKSPACE_ID>
```

If `workspace use` has no ID, list workspaces first and ask the user to choose.

### Targets

```bash
mp target list --format json
mp target show <NAME> --format json
mp target add <NAME> --account <ACCOUNT> --project <PROJECT_ID> [--workspace <WORKSPACE_ID>]
mp target use <NAME>
```

Before adding a target, collect its name, account, project, and optional
workspace. These are identifiers, not secrets.

### Bridge

For bridge status, run:

```bash
mp session --bridge --format json
```

To create a bridge at an explicit path, guide the user to:

```bash
mp account export-bridge [<ACCOUNT>] --to <PATH> [--project <PROJECT_ID>] [--workspace <WORKSPACE_ID>]
```

## Non-interactive authentication

Supported environment combinations include:

```text
MP_USERNAME + MP_SECRET + MP_PROJECT_ID + MP_REGION
MP_OAUTH_TOKEN + MP_PROJECT_ID + MP_REGION
```

Never print their values. When a command fails, report the CLI's concrete error
and suggest the smallest matching recovery command.
"""


def build_remotion_skills(repository: Path, target: Path) -> None:
    source = repository / "packages/skills/skills"
    target.mkdir()
    for source_skill in sorted(path for path in source.iterdir() if path.is_dir()):
        target_skill = target / source_skill.name
        shutil.copytree(
            source_skill,
            target_skill,
            copy_function=shutil.copy2,
            ignore=ignore_remotion_build_files,
        )
        remove_empty_directories(target_skill)

    prepare_remotion_embedded_skills(target)
    remotion_create = target / "remotion-create/SKILL.md"
    text = remotion_create.read_text()
    preview_phrases = [
        "Instead of rendering the video, consider starting the preview server for faster iteration:",
        "Start the preview server after building the composition:",
    ]
    for phrase in preview_phrases:
        if phrase in text:
            text = text.replace(
                phrase,
                "After creating or updating the video, start the preview server by default:",
            )
            break
    text = text.replace(
        "If an in-harness browser is available, open it there.",
        (
            "Open the exact URL in Ghast's available browser. If no browser "
            "tool is available, keep the preview server running and provide "
            "the URL to the user."
        ),
    )
    remotion_create.write_text(text)


def ignore_remotion_build_files(directory: str, names: list[str]) -> set[str]:
    ignored = {name for name in names if name.endswith(".tsx")}
    if Path(directory).name == "agents":
        ignored.add("openai.yaml")
    return ignored


def prepare_remotion_embedded_skills(skills_root: Path) -> None:
    roots = [
        (
            skills_root / "remotion-best-practices/remotion-markup",
            "REFERENCE.md",
        ),
        (skills_root / "remotion-markup", "SKILL.md"),
        (skills_root / "remotion-best-practices", "SKILL.md"),
    ]
    for embedded_root, parent_entry in roots:
        if not embedded_root.exists():
            continue
        embedded_names = sorted(
            child.name
            for child in embedded_root.iterdir()
            if child.is_dir()
            and child.name != "rules"
            and (child / "SKILL.md").is_file()
        )
        parent_name = embedded_root.name
        for markdown in embedded_root.rglob("*.md"):
            text = markdown.read_text()
            text = text.replace(
                f"../{parent_name}/SKILL.md", f"../{parent_entry}"
            ).replace(f"../{parent_name}/", "../")
            if parent_name == "remotion-markup":
                text = text.replace(
                    "../../../remotion-interactivity/SKILL.md",
                    "../../../../remotion-interactivity/SKILL.md",
                )
            for skill_name in embedded_names:
                text = text.replace(
                    f"{skill_name}/SKILL.md",
                    f"{skill_name}/REFERENCE.md",
                )
            markdown.write_text(text)
        for skill_name in embedded_names:
            (embedded_root / skill_name / "SKILL.md").rename(
                embedded_root / skill_name / "REFERENCE.md"
            )


def remove_empty_directories(root: Path) -> None:
    directories = sorted(
        (path for path in root.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    )
    for directory in directories:
        try:
            directory.rmdir()
        except OSError:
            pass


def render_readme(
    name: str,
    source_manifest: dict,
    manifest: dict,
    config: dict,
) -> str:
    display_name = (source_manifest.get("interface") or {}).get(
        "displayName", name
    )
    lines = [
            f"# {display_name}",
            "",
            manifest["description"],
            "",
            "## Official Ghast port",
            "",
            (
                "This package is generated directly from the developer-owned "
                f"repository `{manifest['repository']}` at "
                f"`{manifest['upstreamRevision']}`."
            ),
            "",
    ]
    if config.get("preserve_agent_metadata"):
        lines.extend(
            [
                (
                    "Ghast replaces only the marketplace manifest. Signed "
                    "skill directories and their developer metadata remain "
                    "byte-for-byte from the pinned official repository."
                ),
                "",
            ]
        )
    elif config.get("no_skills"):
        lines.extend(
            [
                (
                    "The public MCP declaration is generated from the "
                    "developer's official documentation and pinned source "
                    "evidence. No private connector mapping is copied."
                ),
                "",
            ]
        )
    else:
        lines.extend(
            [
                (
                    "Skills, references, scripts, commands, and public MCP "
                    "declarations remain sourced from the pinned official "
                    "repository. Unsupported client metadata is omitted."
                ),
                "",
            ]
        )
    compatibility_notes = config.get("compatibility_notes", [])
    if compatibility_notes:
        lines.extend(["## Ghast compatibility", ""])
        lines.extend(f"- {note}" for note in compatibility_notes)
        lines.append("")
    lines.extend(
        [
            (
                "External CLIs, accounts, credentials, paid services, and "
                "platform permissions remain user-managed dependencies."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def git_revision(repository: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def normalized_git_remote(repository: Path) -> str:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return normalized_repository_url(result.stdout.strip())


def normalized_repository_url(url: str) -> str:
    value = url.removesuffix(".git").rstrip("/")
    if value.startswith("git@github.com:"):
        value = f"https://github.com/{value.removeprefix('git@github.com:')}"
    return value


if __name__ == "__main__":
    raise SystemExit(main())
