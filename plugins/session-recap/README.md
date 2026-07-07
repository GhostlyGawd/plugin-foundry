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
- pairs with **test-gap-nudge**: source changed without tests lands under the
  recap's Open questions, so the gap survives the handoff

## The hooks, honestly
Two read-only hooks, both **fail open** (exit 0 always, never block a session):
a `Stop` nudge that suggests a recap once per session when there's uncommitted
work and none was written today, and a `SessionStart` recall that surfaces the
last handoff's title. Silence both with `SESSION_RECAP_SILENT=1`
(`SESSION_RECAP_DEBUG=1` writes a decision trail to `${TMPDIR}`). See
[CHANGELOG.md](./CHANGELOG.md).

## Manage

- **Update:** `/plugin marketplace update`, then `claude plugin update session-recap`
- **Disable / re-enable:** `claude plugin disable session-recap` / `claude plugin enable session-recap` (or the `/plugin` menu — no uninstall needed)
- **Silence the hooks** (keep the skill): `export SESSION_RECAP_SILENT=1`
- **Uninstall:** `claude plugin uninstall session-recap` — removes everything the plugin added
