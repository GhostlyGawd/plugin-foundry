---
name: whats-new
description: Check installed foundry plugins for available updates. Use when the user asks are my plugins up to date, check for plugin updates, or what's new in the foundry.
---

# Check the shelf for updates

1. Read the bundled catalog at `data/catalog.json` inside this plugin's directory —
   each entry carries the shelf `version` as of the `snapshot` date.
2. Find what's installed: run `claude plugin list` (it prints each installed
   plugin's version and source marketplace). If the CLI isn't available in this
   session, say so and point the user at the `/plugin` menu to read versions —
   never guess an installed version.
3. Compare only plugins whose source is the `foundry` marketplace. Report a short
   list: `name  installed → shelf` for anything behind, and say "up to date as of
   <snapshot>" when nothing is.
4. For each plugin behind the shelf, give the exact update line:
   `claude plugin update <name>` — and note that `/plugin marketplace update`
   refreshes the marketplace itself first if the shelf version looks stale.
5. Always state the catalog snapshot date ("shelf as of <snapshot>") — the shelf
   may have moved since this snapshot shipped.
6. **NEVER invent a version, plugin, or changelog detail.** Each plugin's real
   changes live in its `CHANGELOG.md` in the marketplace repo; link there rather
   than summarizing from memory.
