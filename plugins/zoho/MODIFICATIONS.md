# Modifications

Official source:

- `https://github.com/zoho/zohocrm-python-sdk-8.0` at `7dbcafa4f794a5c07b92cfcd6be6ca2d903e2296`

Unmodified official material:

- `LICENSE`
- the eight bundled official PyPI wheels listed in `README.md`

Ghast-authored adapter material:

- `.ghast-plugin/plugin.json`
- `.mcp.json`
- `README.md`
- `MODIFICATIONS.md`
- `NOTICE`
- `assets/icon.svg`
- `licenses/README.md`
- `skills/zoho/SKILL.md`
- `skills/zoho/scripts/zoho_crm_admin_read.py`

The helper script is an independently authored read-only adapter over Zoho's
official SDK. It does not copy the SDK samples or generated API source into the
adapter. Official wheel bytes are preserved exactly and verified by SHA-256.
Every wheel's license text is extracted byte-for-byte into `licenses/`.
