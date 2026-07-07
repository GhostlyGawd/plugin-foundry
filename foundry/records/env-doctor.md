---
name: env-doctor
title: Env Doctor
category: quality
stage: published
version: 0.2.0
always_on_tokens: 130
verified: 2026-07-06
components: [skills, hooks]
one_liner: Checks the toolchain against the project's declared versions at session start and warns early.
tags: [environment, onboarding, hooks]
created: 2026-07-04
updated: 2026-07-07
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

## Build log
- i21: manifest, `envcheck` skill (requirements-first, ✓/✗ report, paired copyable
  fixes, consent law, honest empty state), README with recipes, CHANGELOG, suite.

## Test log
### Test pass — i22
- tier 1: pass; smoke: CLI absent locally, official --strict runs in CI (logged)
- tier 2: unavailable locally — always-on cost: 110 tok (est., stamped)
- tier 3: suite 6/6 — requirements-first, PATH shadowing, consent law, honest empty
  state, invoke contract, manifest; acceptance checks 1–3 traced
- defects: none found — probed: repo with zero requirement files (explicit stop),
  fix vocabulary audited (installs/exports only, nothing destructive)
TEST VERDICT: pass

## Recipes
- fresh clone → "env doctor" → the checklist before your first build
- "why won't this run?" → mismatches surface with paired copyable fixes
- CI-only failure → run inside the container image to diff environments

## Example session
you> why won't this run?
envcheck> reading what the repo declares: package.json engines, .nvmrc found
envcheck> ✓ git 2.43 · ✓ node 20.11 (repo wants >=20) · ✗ python 3.9 (pyproject wants >=3.11)
envcheck> fix (copyable, not run): pyenv install 3.11 && pyenv local 3.11
envcheck> say the word and I run exactly that command — nothing else.

## Publish log
- i24 (maintainer): marketplace entry, version synced, CHANGELOG dated, tag
  env-doctor-v0.1.0.

## Review log
### Review — i23 (reviewer)
- The consent law is the artifact: diagnosis free, surgery consented, per-command.
- Requirements sourced from the repo's own files with silent-skip on absence — no
  manufactured findings, and the empty state says so in words.
- Sharpest question: could a suggested "fix" be destructive-by-default? Audited the
  vocabulary — installs and exports only, no rm/overwrite class commands.
REVIEW: approved
- i182 (maintainer, v11 #2): v0.1.2 — README Manage section (docs sweep). Tag env-doctor-v0.1.2.

## Maintenance log
- v13 A2 (feature, v0.1.2 → v0.2.0): shipped the `SessionStart` hook the Pitch
  and catalog always promised. Ground truth found while building: the front
  matter said `components: [hooks]` but the plugin only ever shipped the
  `envcheck` skill (see Spec/Build log) — so this record was doubly wrong (it
  claimed a hook it lacked). Now it genuinely carries both: `components:
  [skills, hooks]`, and the "at session start" one-liner is finally true. The
  hook (`scripts/session-envcheck.sh`) is a fast, read-only, fail-open tripwire
  on `.nvmrc`/`.node-version` and `.python-version` drift — silent on match /
  no declaration / `ENV_DOCTOR_SILENT=1`, always exit 0. The `envcheck` skill
  stays the deep pass. Regression suite: `foundry/tests/env-doctor/session-hook.test.sh`
  (6 checks: mismatch warns · match silent · nothing-declared silent · opt-out ·
  garbage stdin exit 0 · structural). CHANGELOG + tag env-doctor-v0.2.0.
### Test pass — v13 A2 (qa)
- tier 1: hook suite 6/6 + structure suite 7/7 (14 ok · 0 fail via tools/qa.sh)
- tier 3: SessionStart event valid, matcher-free, quoted ${CLAUDE_PLUGIN_ROOT},
  executable shebang script; read-only (version reads only, 4s timeouts);
  fail-open verified on garbage/empty stdin and python subprocess failure.
- defects: none found — probed false-positive risk (only clear major or
  declared-minor-behind mismatches warn) and nag risk (SessionStart fires once).
TEST VERDICT: pass
### Review — v13 A2 (reviewer)
- Hook-safety bar met: no matcher (`.*` impossible), quoted root, exit 0 always,
  no mutations or network, opt-out + debug env vars documented in README.
- Honest scope: the fast hook covers node/python only; the README and CHANGELOG
  say so and point to the full skill — no overclaim. Version law satisfied
  (minor bump for a new component + CHANGELOG + tag).
REVIEW: approved
