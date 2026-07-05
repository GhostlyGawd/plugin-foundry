---
name: window-watchability
title: Window Watchability Pack
category: growth
stage: published
kind: feature
version: null
components: [site]
one_liner: Next-shift countdown, the sharpest-questions wall, and an ergonomics pass - the window becomes worth returning to.
tags: [countdown, reviews, a11y]
created: 2026-07-05
updated: 2026-07-05
---

## Pitch
Anticipation, argument, and access: a countdown gives visitors a reason to come
back, the hardest review questions show the machine thinking, and reduced-motion
plus aria plus tap targets make it humane on every device.

## Spec
- Countdown chip: pure nextShift(nowUTC) computes the next cron 17 */8 fire;
  renders "next shift in ~Hh Mm"; static text under prefers-reduced-motion.
- Sharpest wall: build extracts "Sharpest question" lines from Review logs into
  saga.html section "Questions the line asked itself" (dynamic count, zero invented).
- Ergonomics: aria-labels on interactive nav/chips, 44px min tap targets, verify
  reduced-motion covers all animations.

## Experiment
- Hypothesis: return visits cluster around shift times once the countdown ships
- Metric: GitHub traffic returning uniques trend; Baseline: 0; Review-after: 2026-09-05

### Acceptance checks
1. nextShift() unit-tested (node) across day boundaries and exact-hour edges.
2. Wall count equals Review logs containing the line - no padding.
3. Every keyframes animation has a reduced-motion guard.

## Build log
- i45: nextShift() pure fn behind SHIFT markers + static-once countdown chip
  (client-side, no server); sharpest-questions wall on the saga (regex over Review
  logs, dynamic count); ergonomics — aria-pressed on tag chips, 44px targets,
  motion guard audit codified as a test. Three suites added.

## Test log
### Test pass — i46
- tier 1: pass
- tier 3: shift suite 4/4 live under node (mid-morning, day boundary, exact-fire
  rolls forward, post-16:17 wrap); wall count equals Review-log sources exactly
  (7/7, zero padding); motion audit — every animation guarded, reduce fallback
  present, chips expose aria-pressed
- defects: none found — probed: countdown chip absent-element guard (no-op),
  cron drift risk noted: fn documents "17 0,8,16 UTC" — if the operator edits the
  cron, the wall test will not catch it; queued a P3 to derive from the workflow
TEST VERDICT: pass

## Publish log
- i48 (maintainer): countdown + wall + ergonomics live this build; experiment
  armed (returning-uniques trend, review 2026-09-05).

## Review log
### Review — i47 (reviewer)
- The countdown computes client-side from a documented constant — no server, no
  polling, honest "~" on the estimate; QA's cron-drift P3 is the right shape of
  humility.
- The wall renders only what reviews actually recorded; at 7 entries it already
  reads like the machine thinking out loud — this is the saga's best section.
- Ergonomics landed as *tests*, not intentions: motion guards and aria-pressed
  are now regressions waiting to be caught, permanently.
- Sharpest question: does a static countdown mislead once stale? No — it renders
  once with "~", and the ON AIR light remains the live truth signal.
REVIEW: approved
