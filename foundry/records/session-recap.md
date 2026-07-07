---
name: session-recap
title: Session Recap
category: context
stage: published
version: 0.2.0
always_on_tokens: 93
verified: 2026-07-06
components: [skills, hooks]
one_liner: Writes a structured recap when a session ends and recalls it when the next one starts.
tags: [memory, sessions, continuity]
created: 2026-07-04
updated: 2026-07-07
---

# Session Recap

Context evaporates between sessions; yesterday's decisions get re-derived today.

## Pitch
- **Job:** continuity across sessions without hand-written notes.
- **User:** anyone running multi-day work in one repo.
- **Components:** a Stop/SessionEnd hook appending a dated recap stub to a project
  log file, plus a `recall` skill that reads and summarizes recent entries on demand.
- **Why a plugin:** it's an event (hook) + a retrieval prompt (skill) — a natural
  bundle; also a clean exercise of hook-safety law (writes one project-local file,
  documented loudly).

## Spec
- Name: `session-recap` (forever). One skill, `recap`, description (verbatim):
  "Write a durable handoff recap of this working session into SESSION-RECAP.md.
  Use when ending a session, handing work to someone else, or the user says recap
  this session, write a handoff, or where did we leave off."
- Behavior: read the session's evidence (git status, git diff --stat, recent
  conversation decisions), then APPEND a dated section to SESSION-RECAP.md with:
  What changed · Decisions made · Open questions · Next steps (checkboxed). Never
  overwrite prior recaps; create the file if absent; no hooks, no network.
### Acceptance checks
1. Skill appends (never truncates) and dates each section.
2. Reads git evidence before writing — no invented changes.
3. Next steps render as actionable checkboxes.

## Build log
- i16: manifest, `recap` skill (evidence-first, append-only, checkboxed next
  steps, archive offer past ~10 sections), README with recipes, CHANGELOG,
  executable test suite.

## Test log
### Test pass — i17
- tier 1: pass; smoke: CLI absent locally, official --strict runs in CI (logged)
- tier 2: unavailable locally — always-on cost: 93 tok (est., stamped)
- tier 3: suite 5/5 — append-only law, evidence-before-prose, checkboxed steps,
  invoke contract, manifest; acceptance checks 1–3 traced through the skill text
- defects: none found — probed: missing-file case (create-if-missing present),
  archive behavior is offer-only (no unasked file moves)
TEST VERDICT: pass

## Recipes
- "recap this session" → dated section appended to SESSION-RECAP.md
- "where did we leave off?" → latest section read back before starting
- "hand this off to Sam" → next steps written for a stranger

## Example session
you> recap this session
recap> evidence: git status, diff --stat, 3 decisions from this conversation
recap> appended "## 2026-07-05 14:30 — intake hardening" to SESSION-RECAP.md
recap> next steps written for a stranger:
recap> - [ ] wire PINGS_ENABLED in repo settings
recap> - [ ] re-run the adversarial pass on commission #12

## Publish log
- i19 (maintainer): marketplace entry, version synced, CHANGELOG dated, tag
  session-recap-v0.1.0.

## Review log
### Review — i18 (reviewer)
- The skill's spine is the honesty clause: evidence (git + actual conversation
  decisions) before prose, and APPEND-only so handoffs are a ledger, not a wiki.
- Checkboxes written "for a stranger" — matches the handoff job precisely.
- No hooks, no background writes, one file touched, archive is an offer.
- Sharpest question: can it fabricate a change log with no git repo present? No —
  status/diff steps precede writing; absent evidence yields absent claims.
REVIEW: approved
- i182 (maintainer, v11 #2): v0.1.2 — README Manage section (docs sweep). Tag session-recap-v0.1.2.

## Maintenance log
- v13 B5+B6 (feature, v0.1.2 → v0.2.0): the record carried `components:
  [skills, hooks]` and a one-liner promising "when a session ends … the next
  one starts", but the plugin shipped skill-only (the Spec even said "no
  hooks"). Rather than the originally-pitched stub-writing hook (which would
  write a file unasked — against hook-safety law), shipped two **read-only,
  fail-open** hooks: a `Stop` nudge (`scripts/recap-nudge.sh`) that suggests a
  recap once per session when there's uncommitted work and none written today,
  and a `SessionStart` recall (`scripts/recap-recall.sh`) that surfaces the
  last handoff's title. `components` is now true; the one-liner is true. B6
  synergy: the `recap` skill now files source-changed-without-tests (the
  test-gap-nudge signal) under Open questions. Suite:
  `foundry/tests/session-recap/hooks.test.sh` (8 checks). Tag session-recap-v0.2.0.
### Test pass — v13 B5 (qa)
- tier 1: hooks suite 8/8 + skill suite 6/6 (15 ok · 0 fail via tools/qa.sh);
  official validate --strict passes the two-hook manifest.
- tier 3: SessionStart + Stop events valid, matcher-free, quoted roots,
  executable shebang scripts; read-only (git status + file reads only);
  fail-open verified on clean tree / recapped-today / no-file / garbage stdin /
  opt-out; once-per-session marker honored.
- defects: none found — probed double-nudge (marker), post-recap silence
  (today's date match), and recall with multiple sections (newest wins).
TEST VERDICT: pass
### Review — v13 B5 (reviewer)
- Hook-safety bar met: no file writes (the pitch's stub-writer was correctly
  dropped as unasked-write), exit 0 always, opt-out + debug documented.
- The two hooks finally make a self-contradicting record honest without
  overclaiming — nudge suggests, never writes; recall reads, never mutates.
REVIEW: approved
