# TODO Ledger

One skill, `ledger`: turns the sediment of `TODO` / `FIXME` / `HACK` / `XXX`
comments scattered across a repo into a **ranked, dated ledger** — each hit
carries its git-blame age and author, sorted oldest-first, with a worst-offenders
summary and copyable `file:line` references. The five-year-old FIXME stops looking
like Friday's.

## Install

One shared source ships native packages for Claude Code, Codex, Gemini CLI, Cursor, and
GitHub Copilot. See [host-specific install paths](https://github.com/GhostlyGawd/plugin-foundry/blob/main/COMPATIBILITY.md).

```
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install todo-ledger@foundry
```

## Recipes
- "list the TODOs" → the full ledger, oldest debt first
- "what's the worst tech debt here?" → the worst-offenders top 5 with authors
- "save a TODO report" → writes a dated `TODO-LEDGER-<date>.md` (only when asked)

## Honest disclosures
- **Never invents a date.** Age and author come from `git blame`; an unblameable
  or uncommitted line is labeled "unknown"/"uncommitted", never a guessed date.
- **Read-only by default.** It reports; it never edits, deletes, or "fixes" a
  marker. The dated file is written only on an explicit request.
- Outside a git repo it still lists the markers, and says so — age and author are
  unavailable without history.

## Changelog
See [CHANGELOG.md](./CHANGELOG.md).

## Manage

- **Update:** `/plugin marketplace update`, then `claude plugin update todo-ledger`
- **Disable / re-enable:** `claude plugin disable todo-ledger` / `claude plugin enable todo-ledger` (or the `/plugin` menu — no uninstall needed)
- **Uninstall:** `claude plugin uninstall todo-ledger` — removes everything the plugin added
