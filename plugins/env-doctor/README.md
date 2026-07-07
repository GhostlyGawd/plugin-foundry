# Env Doctor

One skill, `envcheck`: compares your machine against what the repo *actually
declares* (engines, .nvmrc, requires-python, .tool-versions, go.mod, .env.example)
and reports ✓/✗ per line with a copyable fix for every ✗. It never installs,
switches, or mutates anything without your yes to the specific command.

Plus a `SessionStart` hook that catches you early: on a fresh session it does a
fast, read-only check of the declared runtime versions (`.nvmrc`/`.node-version`,
`.python-version`) and prints a single heads-up line only when one clearly drifts
from what's installed — then get the full picture with `envcheck` ("env doctor").

## Install
```
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install env-doctor@foundry
```

## Recipes
- fresh clone → "env doctor" → the checklist before your first build
- "why won't this run?" → mismatches surface with paired fixes
- CI-only failure → run it inside the container image to diff environments

One read-only `SessionStart` hook, no network, no unasked changes. See
[CHANGELOG.md](./CHANGELOG.md).

## Manage

- **Update:** `/plugin marketplace update`, then `claude plugin update env-doctor`
- **Disable / re-enable:** `claude plugin disable env-doctor` / `claude plugin enable env-doctor` (or the `/plugin` menu — no uninstall needed)
- **Silence just the session-start heads-up** (keep the `envcheck` skill): set `ENV_DOCTOR_SILENT=1` in your environment. `ENV_DOCTOR_DEBUG=1` writes the hook's decision trail to `${TMPDIR}/env-doctor-debug.log`.
- **Uninstall:** `claude plugin uninstall env-doctor` — removes everything the plugin added
