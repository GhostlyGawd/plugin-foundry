---
name: traveler-pings
title: Traveler Pings
category: growth
stage: published
kind: feature
version: null
verified: 2026-07-06
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

## Test log
### Test pass — i66
- tier 1: pass
- tier 3: unit suite 6/6 (created / stage-up / published telegrams, no-issue
  silence by key-set assertion, per-issue cap, no-change no-noise); live dry-run
  against real HEAD~1 → clean "nothing moved for a suggester" (no records carry
  suggested_in yet — correct silence); workflow lints, step guarded + fail-soft
- defects: none in the artifact; the suite's first silence predicate was letter
  soup and got rewritten — logged for the pattern file
TEST VERDICT: pass

## Publish log
- i68 (maintainer): mechanism live; arms when the operator sets PINGS_ENABLED in
  repo variables; experiment armed (suggester re-engagement, review 2026-09-15).

## Review log
### Review — i67 (reviewer)
- The comment body tells the reader *how it was sent* ("by the shift that did the
  work") — provenance in the notification itself, on brand.
- Per-issue cap and fail-soft are the difference between a courtesy and a spam
  bot; the guard means the operator arms it deliberately, never by surprise.
- Sharpest question: what if a suggester's record is killed? diff() only speaks
  on stage *changes it can name kindly* — shelved/killed records still ping with
  the honest stage word, and the certificate explains the memo. Acceptable; the
  kill memo is part of the deal suggesters sign up for.
REVIEW: approved
