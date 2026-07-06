# Plugin Smith

Two skills for building Claude Code plugins correctly: `scaffold` generates a new
plugin skeleton with the official layout, and `doctor` audits an existing plugin
directory against the official schema and a strict quality bar.

## Install

```
/plugin marketplace add GhostlyGawd/plugin-foundry        # once, for this marketplace
/plugin install plugin-smith@foundry
```

Or try it for one session without installing:

```
claude --plugin-dir ./plugins/plugin-smith
```

## Skills

- **plugin-smith:scaffold** — "Scaffold a new Claude Code plugin…" Give it a name
  and component list; it produces a correct tree, manifest, README, CHANGELOG, and
  prints the validate/test commands.
- **plugin-smith:doctor** — "Audit a Claude Code plugin directory…" Point it at a
  plugin path; it reports BLOCKER/WARN/NIT findings with exact fixes and a verdict.

No hooks, no MCP servers, nothing runs in the background.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).
