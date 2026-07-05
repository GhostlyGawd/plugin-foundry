---
name: envcheck
description: Diagnose this project's development environment against what the repo actually requires and report mismatches with fixes. Use when builds fail mysteriously, after cloning a new repo, or the user says check my environment, why won't this run, or env doctor.
---

# Diagnose the environment

1. **Read the repo's own requirements first** — only files that exist, never
   assumptions: `package.json` engines, `.nvmrc`, `.python-version`,
   `pyproject.toml` requires-python, `.tool-versions`, `Gemfile` ruby, `go.mod`
   go line, `.env.example` variable names. Absent file → skip silently.
2. **Measure reality:** matching version commands (`node -v`, `python3 --version`,
   `git --version`, ...), `type -a <tool>` for PATH shadowing, lockfile present but
   dependencies not installed, `.env.example` names unset in the environment.
3. **Report**, one line per finding:
   `✓ node 20.11 (repo wants >=20)` / `✗ python 3.9 (pyproject wants >=3.11)`
4. **Fixes:** for every ✗, one copyable command with a one-line why
   (`nvm install 20`, `pyenv install 3.11`, `npm ci`, `export FOO=...`).
   **Never run an install, version switch, or file mutation yourself unless the
   user says yes to that specific command.** Diagnosis is free; surgery is consented.
5. Nothing to check (no requirement files at all)? Say exactly that and stop —
   don't manufacture findings.
