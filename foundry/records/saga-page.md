---
name: saga-page
title: The Saga
category: growth
stage: building
kind: feature
version: null
components: [site]
one_liner: An auto-generated timeline of the workshop's own story — ADRs, ships, kills, ceremonies.
tags: [lore, narrative, retention]
created: 2026-07-05
updated: 2026-07-05
---

# The Saga

Lore is retention. The repo already contains the whole story — render it.

## Pitch
- **Job:** give returners and newcomers the plot in one scroll.
- **User:** spectators; press; future forkers.
- **Components:** build.py derives a timeline from DECISIONS.md (ADR titles +
  context first-lines), published ship dates, deprecations, and phase changes —
  site/saga.html, linked from the jump-nav.

## Spec
- Entries only from ADRs and records; no editorializing beyond what the sources
  say; newest first; Naming Ceremony gets a marked slot ("awaiting" until it lands).
### Acceptance checks
1. Every ADR renders as a dated saga entry with its title and one context line.
2. Ships/kills interleave from record `updated` dates.
3. Zero invented milestones.

## Experiment
- **Hypothesis:** the saga deepens sessions — returning uniques and time-on-window
  proxies (repeat data.json fetch patterns are not tracked; use `uniques_14d`
  trend + shipnote issue views) improve post-ship.
- **Metric:** `uniques_14d` in METRICS.jsonl.
- **Baseline:** from first real snapshot.
- **Review-after:** 30 days post-deploy.

## Build log
- i0(v5): generator + page landed with the v5 window; QA fixture pass pending
  before rc.
