---
name: saga-page
title: The Saga
category: growth
stage: rc
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

## Test log
### Test pass — i5
- tier 1: pass
- tier 2: n/a (site feature)
- tier 3: all 11 ADRs render with id+title+context line; SHIPPED entries equal
  published-record count exactly (zero invented milestones); Naming Ceremony slot
  resolved to Nightshift Foundry post-ADR-011
- defects: none found — probed: ADR heading without Context bullet (renders empty line, not junk)
TEST VERDICT: pass

## Review log
### Review — i107
- Sources-only law verified end-to-end: ADR entries regex-scraped from
  DECISIONS.md headings (template heading can't match — space breaks the id
  group); fates from record stage+updated only; wall quotes lifted verbatim from
  Review logs. Zero invented milestones — SHIPPED count equals published records
  exactly (23/23, re-counted today including this slate's three ships).
- ADR-014 (this slate) already renders with its context line — the saga extends
  itself without anyone touching the page. That's the design working.
- Escaping audited on every interpolation. Newest-first holds.
- Nit (non-blocking): 220-char wall truncation cuts mid-word with no ellipsis
  (Night Clerk, Traveler Pings entries) — filed P3; cosmetic, not dishonest.
- Axes: scope 5 · prompt n/a · thrift 5 · hook-safety n/a · docs-truth 5 ·
  structure 5.
REVIEW: approved — the repo tells its own story without embellishment.
