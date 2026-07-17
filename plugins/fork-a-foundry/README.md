# Fork a Foundry

One skill, `bootstrap`, that stands up your own self-running plugin workshop — the
same architecture that built and maintains this marketplace: loop protocol, role
rotation, stage-gated pipeline, executable QA, security laws, living window.

## Install

One shared source ships native packages for Claude Code, Codex, Gemini CLI, Cursor, and
GitHub Copilot. See [host-specific install paths](https://github.com/GhostlyGawd/plugin-foundry/blob/main/COMPATIBILITY.md).

```
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install fork-a-foundry@foundry
```

Then: "bootstrap a foundry in ~/my-foundry". The skill offers a fast fork path or a
from-spec scaffold, carries the laws over verbatim, and doesn't finish until the new
loop runs one green iteration. No hooks, nothing runs in the background.

## Recipes
- "bootstrap a foundry in ~/my-foundry" → fast fork path, laws carried verbatim
- "scaffold a foundry from spec" → the from-spec build when you want to read every law
- "turn this repo into a self-running workshop" → adapts the loop onto an existing repo

## Changelog
See [CHANGELOG.md](./CHANGELOG.md).

## Manage

- **Update:** `/plugin marketplace update`, then `claude plugin update fork-a-foundry`
- **Disable / re-enable:** `claude plugin disable fork-a-foundry` / `claude plugin enable fork-a-foundry` (or the `/plugin` menu — no uninstall needed)
- **Uninstall:** `claude plugin uninstall fork-a-foundry` — removes everything the plugin added
