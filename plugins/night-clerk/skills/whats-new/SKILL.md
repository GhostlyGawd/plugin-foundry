---
name: whats-new
description: Check installed foundry plugins for available updates. Use when the user asks are my plugins up to date, check for plugin updates, or what's new in the foundry.
---

# Check the shelf for updates

1. Read the bundled catalog at `data/catalog.json` inside this plugin's directory —
   each entry carries the shelf `version` as of the `snapshot` date.
2. Identify the active host from the session, then use only its native inventory:
   `claude plugin list`, `codex plugin list`, `copilot plugin list`, or
   `gemini extensions list`. For Cursor, direct the user to Settings → Plugins.
   If the host or CLI is unavailable, say so — never guess an installed version.
3. Compare only plugins whose source is the `foundry` marketplace. Report a short
   list: `name  installed → shelf` for anything behind, and say "up to date as of
   <snapshot>" when nothing is.
4. For each plugin behind the shelf, give only the native update path:
   `claude plugin update <name>`, the Codex Plugins Directory after
   `codex plugin marketplace upgrade foundry`, `copilot plugin update <name>`,
   `gemini extensions update <name>`, or a refreshed Cursor package/marketplace.
5. Always state the catalog snapshot date ("shelf as of <snapshot>") — the shelf
   may have moved since this snapshot shipped.
6. **NEVER invent a version, plugin, or changelog detail.** Each plugin's real
   changes live in its `CHANGELOG.md` in the marketplace repo; link there rather
   than summarizing from memory.
