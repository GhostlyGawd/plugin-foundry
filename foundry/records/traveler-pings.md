---
name: traveler-pings
title: Traveler Pings
category: growth
stage: building
kind: feature
version: null
components: [workflow]
one_liner: When a suggested idea changes stage, the original issue hears about it - suggesters watch their idea move down the line.
tags: [issues, notifications, credit]
created: 2026-07-05
updated: 2026-07-05
---

## Pitch
The cheapest loyalty program in software: tell people their idea is moving.

## Spec
- tools/pings.py: pure diff of record stages (old map vs new map) - for records
  with suggested_in, emit one courteous comment body per stage change; CLI mode
  reads HEAD~1 vs HEAD; DRY_RUN prints, CI mode uses gh issue comment.
- run-shift.yml gains a guarded step (PINGS_ENABLED) after push.
- Max one comment per issue per shift; tone: workshop telegram; links certificate.

## Experiment
- Hypothesis: suggesters return: prospected issues get author reactions or replies after pings
- Metric: author engagement on pinged issues; Baseline: 0; Review-after: 2026-09-15

### Acceptance checks
1. Pure diff unit-tested: created, stage-up, published, no-change, no-issue.
2. One-comment-per-issue-per-shift cap enforced in the emitter.
3. Workflow step is guard-railed and fails soft.

## Build log
- i65: pings.py — pure diff core (created / stage-up / published telegrams,
  per-issue cap, silent on no-issue), git snapshot CLI (HEAD~1 vs HEAD), DRY_RUN
  default, gh only behind --send; run-shift.yml gains a guarded fail-soft step
  after push (PINGS_ENABLED). Unit suite 6/6.
