---
name: fork-a-foundry
title: Fork a Foundry
category: meta
stage: published
kind: plugin
version: 0.1.4
components: [skills]
always_on_tokens: 90
verified: 2026-07-06
one_liner: One skill that bootstraps your own self-running plugin workshop — the factory, shipping itself.
tags: [meta, bootstrap, viral, dogfood]
created: 2026-07-05
updated: 2026-07-07
---

# Fork a Foundry

The most useful thing the workshop can ship is the workshop. One skill stands up the
whole architecture — protocol, roles, gates, laws — and won't finish until the new
loop runs a green iteration.

## Pitch
- **Job:** anyone with Claude Code gets their own autonomous plugin factory in
  minutes.
- **User:** developers who watched the window and thought "I want one."
- **Components:** a single `bootstrap` skill (fork path + from-spec scaffold).
- **Why a plugin:** it's the strongest possible dogfood — and the most honest growth
  feature, since every fork is a person who trusted the machine enough to run it.

## Spec
- Name: `fork-a-foundry` (forever).
- skills/bootstrap/SKILL.md — description (verbatim): "Bootstrap a new self-running
  foundry — a loop-driven Claude Code plugin workshop and marketplace — in a fresh
  directory. Use when someone wants their own autonomous plugin factory, a fork of
  this workshop, or a loop-run marketplace."
- Must offer fork vs. scaffold; must carry the load-bearing laws verbatim; must not
  finish before the new repo passes its own gates; must remind about containers and
  the Naming Ceremony. No hooks, no network beyond the user-pointed clone.
### Acceptance checks
1. Skill body names both paths and refuses to finish without a green `./loop.sh`-able
   state (validate + build + qa).
2. The load-bearing laws (one-commit discipline, untrusted patron text,
   two-iteration rule, naming ceremony, tripwires) appear verbatim-or-equivalent.
3. `foundry/tests/fork-a-foundry` harness green; official `--strict` validate green
   in CI.

## Build log
- i0(v4): manifest, bootstrap skill, README, CHANGELOG, executable test suite.

## Test log
### Test pass — i0(v4)
- tier 1: pass — validate.py + qa.sh green (see harness)
- tier 2: unavailable locally — official --strict validate runs in the QA workflow
- tier 3: checks 1–2 executed via foundry/tests/fork-a-foundry/structure.test.sh
- defects: none found — probed: law-coverage greps, missing-sandbox-reminder case
TEST VERDICT: pass

## Recipes
- "fork this foundry into ~/my-workshop" → the whole loop, laws carried
- "bootstrap a fresh foundry from spec in ./new" → from-spec path, ceremony pending
- first run after forking: `bash loop.sh 3` and watch the journal fill

## Example session
you> fork this foundry into ~/my-workshop
bootstrap> copying LOOP.md, charter/, tools/, loop.sh — laws travel with the code
bootstrap> your workshop has NO name yet: the Naming Ceremony is yours to hold
bootstrap> first run: cd ~/my-workshop && bash loop.sh 3
bootstrap> gates must pass in the new repo before I call this done... green.

## Publish log
- i9 (maintainer): marketplace entry (source ./plugins/fork-a-foundry), version
  0.1.0 synced, CHANGELOG dated, release tag fork-a-foundry-v0.1.0 laid. First
  artifact through the complete v4/v5 gate chain with zero genesis exceptions.

## Review log
### Review — i8 (reviewer)
- QUALITY bar walked line-by-line: invoke contract present; both paths (fork /
  from-spec) named with the fork path recommended; the five load-bearing laws
  carried verbatim-or-equivalent (one-commit, untrusted patron text, two-iteration
  rule, tripwires, naming handoff); finish condition demands the new repo pass its
  own gates before the skill may stop; container reminder present.
- Hooks: none shipped, none referenced — matches README's claim. Token thrift:
  ~90 tok est always-on, well under budget.
- Sharpest question asked: does the skill teach forks to keep OUR name? No — it
  explicitly hands the new system its own Naming Ceremony.
- Nit (non-blocking, journaled): from-spec path could link OPERATIONS.md § 7–8
  once forks stabilize; queue as P3 polish.
REVIEW: approved
- i182 (maintainer, v11 #2): v0.1.2 — README Manage section (docs sweep). Tag fork-a-foundry-v0.1.2.

## Maintenance log
- i214 (maintainer, v12 4.1): the first real fork exists — GhostlyGawd/test,
  seeded whole by the genesis ceremony (ADR-021) and registered on the
  network. The record's promise ("the loop that built this one, in a box")
  is now backed by a birth, not a fixture. No artifact change; no bump.
- v13 B8: v0.1.2 → v0.1.3 — author normalized to "Nightshift Foundry" (matched
  the shelf) and a standard `## Recipes` section added. Docs-only; Tag
  fork-a-foundry-v0.1.3.
- v14 P3 (ADR-024): v0.1.4 — the from-spec bootstrap path now points at
  OPERATIONS.md §7–8 (governor & veto, community & fuel), the optional layers a
  hand-built spine forgets (reviewer nit from i8). Docs-only; Tag fork-a-foundry-v0.1.4.
