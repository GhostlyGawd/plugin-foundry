# Session Recap

One skill, `recap`: ends a working session with a dated, append-only handoff in
`SESSION-RECAP.md` — what changed (from git evidence, not memory), decisions made,
open questions, and checkboxed next steps someone else could pick up cold.

## Install
```
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install session-recap@foundry
```

## Recipes
- "recap this session" → appends today's section
- "where did we leave off?" → reads the latest section back before starting
- "hand this off to Sam" → recap with next steps written for a stranger

No hooks, nothing runs in the background. See [CHANGELOG.md](./CHANGELOG.md).

## Manage

- **Update:** `/plugin marketplace update`, then `claude plugin update session-recap`
- **Disable / re-enable:** `claude plugin disable session-recap` / `claude plugin enable session-recap` (or the `/plugin` menu — no uninstall needed)
- **Uninstall:** `claude plugin uninstall session-recap` — removes everything the plugin added
