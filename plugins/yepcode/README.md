# yepcode

Build, expose, schedule, execute, and audit JavaScript or Python automation tools in YepCode's isolated environment through YepCode's official hosted MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/yepcode/mcp-server-js` at `15cf0527dda6c818a1528ed4467389e0962a1eea`.

The MIT license is copied from YepCode's pinned official MCP repository. Ghast connects directly to YepCode's hosted MCP endpoint and adds only adapter metadata, safety guidance, and a generic Ghast-authored code-execution icon; no YepCode service code or marketplace artwork is packaged.

## Ghast compatibility

- The Codex private app mapping is replaced by YepCode's official hosted MCP endpoint using a user-managed API Credential from the encrypted Profile Vault.
- Ghast enables run_code, yc_api, and the default mcp-tool process tag. This exposes 33 fixed official tools plus each eligible user process as a dynamic JSON Schema tool.
- The fixed surface covers JavaScript and Python sandbox execution, process and module creation, JSON Schema inputs, synchronous and asynchronous runs, schedules, execution logs, variables, and storage. It matches the Codex plugin's programmable, scheduled, auditable tool contract.
- The adapter intentionally does not enable yc_api_full. Process/module version and service-account administration are outside the Codex capability description and would expand credential and destructive-operation exposure.
- The source publishes no MCP safety annotations. Ghast therefore treats arbitrary code, dynamic process calls, execution, scheduling, upload, create, update, pause, resume, kill, rerun, and delete operations as writes.
- A generic code-execution icon is used because the official MIT repository does not publish a catalog icon.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
