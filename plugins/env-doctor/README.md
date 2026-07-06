# Env Doctor

One skill, `envcheck`: compares your machine against what the repo *actually
declares* (engines, .nvmrc, requires-python, .tool-versions, go.mod, .env.example)
and reports ✓/✗ per line with a copyable fix for every ✗. It never installs,
switches, or mutates anything without your yes to the specific command.

## Install
```
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install env-doctor@foundry
```

## Recipes
- fresh clone → "env doctor" → the checklist before your first build
- "why won't this run?" → mismatches surface with paired fixes
- CI-only failure → run it inside the container image to diff environments

No hooks, no network, no unasked changes. See [CHANGELOG.md](./CHANGELOG.md).
