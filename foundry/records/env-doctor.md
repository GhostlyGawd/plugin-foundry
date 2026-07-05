---
name: env-doctor
title: Env Doctor
category: quality
stage: spec
version: null
components: [hooks]
one_liner: Checks the toolchain against the project's declared versions at session start and warns early.
tags: [environment, onboarding, hooks]
created: 2026-07-04
updated: 2026-07-04
---

# Env Doctor

Half of "it doesn't work" is a version mismatch discovered twenty minutes in.

## Pitch
- **Job:** surface toolchain drift in the first second of a session.
- **User:** teams with .tool-versions/.nvmrc/pinned runtimes.
- **Components:** one SessionStart command hook running a read-only script that
  compares installed versions to declared ones and prints warnings.
- **Why a plugin:** SessionStart is exactly what hooks exist for; read-only by
  design, so a good showcase of the safety bar.

## Spec
- Name: `env-doctor` (forever). One skill, `envcheck`, description (verbatim):
  "Diagnose this project's development environment against what the repo actually
  requires and report mismatches with fixes. Use when builds fail mysteriously,
  after cloning a new repo, or the user says check my environment, why won't this
  run, or env doctor."
- Behavior: read the repo's own requirements first (package.json engines, .nvmrc,
  .python-version / pyproject requires-python, .tool-versions, Gemfile ruby, go.mod
  go line — whichever exist), then compare against installed versions, check PATH
  shadowing (`type -a`), missing lockfile installs, and unset vars named in
  .env.example. Output: REPORT (✓/✗ per line) then FIXES as copyable commands.
  NEVER runs an install or mutation without the user saying yes to the specific
  command.
### Acceptance checks
1. Requirements come from repo files, not assumptions; absent files skip silently.
2. Every ✗ pairs with a copyable fix; no fix auto-runs.
3. PATH shadowing check present (`type -a`).
