# PR Narrator

One skill, `pr`: turns your branch's real commits and diff into a reviewer-ready
pull request — conventional title, Summary, grouped Changes, *honest* Test notes
("none" allowed, lies not), Risk & rollback. Offers `gh pr create` with the exact
command and runs it only on your yes.

## Install

One shared source ships native packages for Claude Code, Codex, Gemini CLI, Cursor, and
GitHub Copilot. See [host-specific install paths](https://github.com/GhostlyGawd/plugin-foundry/blob/main/COMPATIBILITY.md).
```
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install pr-narrator@foundry
```

## Recipes
- "write the PR" on a finished branch → full draft from evidence
- pair with **commit-craft**: clean commits in, clean narrative out
- pair with **dep-bump-brief** on a dependency PR: paste its risk line straight
  into the **Risk & rollback** section — same diff, one honest sentence
- "describe this branch for the changelog" → same evidence, changelog voice

No hooks, no pushes, nothing unasked. See [CHANGELOG.md](./CHANGELOG.md).

## Manage

- **Update:** `/plugin marketplace update`, then `claude plugin update pr-narrator`
- **Disable / re-enable:** `claude plugin disable pr-narrator` / `claude plugin enable pr-narrator` (or the `/plugin` menu — no uninstall needed)
- **Uninstall:** `claude plugin uninstall pr-narrator` — removes everything the plugin added
