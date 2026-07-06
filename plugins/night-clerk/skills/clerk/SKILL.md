---
name: clerk
description: Search the Nightshift Foundry catalog and recommend plugins for a task. Use when the user asks what plugin helps with X, browse the foundry, or find me a plugin.
---

# Work the front desk

1. Read the bundled catalog at `data/catalog.json` inside this plugin's directory
   (fields: snapshot date, plugins with name / one_liner / tags / install).
2. Match the user's task against one_liners and tags. Recommend **at most 3**,
   best fit first — each with its one_liner and the exact install line, e.g.
   `/plugin install commit-craft@foundry`. If the task maps to a curated bundle
   in the catalog's `kits` array (e.g. setting up a whole workflow), offer that
   kit as ONE of the three — its name, desc, and install lines verbatim.
3. Always state the catalog snapshot date ("catalog as of <snapshot>") — the
   shelf may have grown since; `/plugin marketplace update` refreshes.
4. **NEVER invent a plugin, capability, or install line.** If nothing in the
   catalog fits, say exactly that and offer the idea route: the foundry takes
   suggestions at the repo's `issues/new?template=idea.yml` (path in the catalog).
5. If the user asks what the foundry *is*, answer in one line and point at the
   window rather than improvising lore.
