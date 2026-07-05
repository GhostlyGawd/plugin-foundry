---
name: window-watchability
title: Window Watchability Pack
category: growth
stage: spec
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
