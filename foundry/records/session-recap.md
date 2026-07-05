---
name: session-recap
title: Session Recap
category: context
stage: rc
version: null
always_on_tokens: 93
verified: 2026-07-05
components: [skills, hooks]
one_liner: Writes a structured recap when a session ends and recalls it when the next one starts.
tags: [memory, sessions, continuity]
created: 2026-07-04
updated: 2026-07-04
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

## Review log
### Review — i18 (reviewer)
- The skill's spine is the honesty clause: evidence (git + actual conversation
  decisions) before prose, and APPEND-only so handoffs are a ledger, not a wiki.
- Checkboxes written "for a stranger" — matches the handoff job precisely.
- No hooks, no background writes, one file touched, archive is an offer.
- Sharpest question: can it fabricate a change log with no git repo present? No —
  status/diff steps precede writing; absent evidence yields absent claims.
REVIEW: approved
