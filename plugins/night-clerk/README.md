# Night Clerk

The marketplace's front desk, installed in your terminal. Two skills:

- `clerk` — ask "what plugin helps with X?" and get up to three real
  recommendations with exact install lines — from a bundled catalog snapshot,
  never from imagination.
- `whats-new` — ask "are my plugins up to date?" and the clerk compares what
  `claude plugin list` reports against the shelf versions in the snapshot,
  handing you `claude plugin update <name>` lines for anything behind.

## Install
```
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install night-clerk@foundry
```

## Recipes
- "what plugin helps with commit messages?" → commit-craft, with the install line
- "browse the foundry" → the shelf, three at a time, snapshot date stated
- "find me a plugin for handoffs" → session-recap, or an honest "nothing fits yet" + the idea route
- "are my foundry plugins up to date?" → installed vs shelf versions, update lines included

## Honest disclosures
The catalog is a **snapshot** (date stated in every answer), regenerated and
shipped with each clerk release; `/plugin marketplace update` pulls the freshest.
The clerk cannot install anything itself and will never invent a plugin.

See [CHANGELOG.md](./CHANGELOG.md).

## Manage

- **Update:** `/plugin marketplace update`, then `claude plugin update night-clerk`
- **Disable / re-enable:** `claude plugin disable night-clerk` / `claude plugin enable night-clerk` (or the `/plugin` menu — no uninstall needed)
- **Uninstall:** `claude plugin uninstall night-clerk` — removes everything the plugin added
- **Check for updates from inside a session:** ask "are my plugins up to date?" — the `whats-new` skill compares installed versions against the shelf.
