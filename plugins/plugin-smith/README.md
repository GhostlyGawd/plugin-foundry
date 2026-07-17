# Plugin Smith

Two skills for building portable coding-agent plugins correctly: `scaffold`
generates one shared source plus host-native packages, and `doctor` audits an
existing source/package set against the target formats and a strict quality bar.

## Install

One shared source ships native packages for Claude Code, Codex, Gemini CLI, Cursor, and
GitHub Copilot. See [host-specific install paths](https://github.com/GhostlyGawd/plugin-foundry/blob/main/COMPATIBILITY.md).

```
/plugin marketplace add GhostlyGawd/plugin-foundry        # once, for this marketplace
/plugin install plugin-smith@foundry
```

Or try it for one session without installing:

```
claude --plugin-dir ./plugins/plugin-smith
```

## Skills

- **plugin-smith:scaffold** — give it a name, component list, and optional host set;
  it produces shared behavior, native manifests/packages, documentation, and
  validation commands without maintaining five forks.
- **plugin-smith:doctor** — point it at a source directory or native package set; it
  reports host-specific BLOCKER/WARN/NIT findings with exact fixes and a verdict.

No hooks, no MCP servers, nothing runs in the background.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## Manage

- **Update:** `/plugin marketplace update`, then `claude plugin update plugin-smith`
- **Disable / re-enable:** `claude plugin disable plugin-smith` / `claude plugin enable plugin-smith` (or the `/plugin` menu — no uninstall needed)
- **Uninstall:** `claude plugin uninstall plugin-smith` — removes everything the plugin added
