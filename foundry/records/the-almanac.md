---
name: the-almanac
title: The Almanac
category: growth
stage: spec
kind: feature
version: null
components: [site]
one_liner: A monthly, auto-generated state-of-the-shift: ships, kill rate, cost per ship, the best defect the gates caught.
tags: [retrospective, accountability, content]
created: 2026-07-05
updated: 2026-07-05
---

## Pitch
Public accountability as content: a page the machine writes about itself from the
ledger, every month, no adjectives it cannot back.

## Spec
- tools/almanac.py reads JOURNAL (iterations, role histogram), records (ships and
  kills this month), DECISIONS delta, BUDGET.jsonl (absent - says "no ledger yet"),
  qa summary - writes site/almanac/<YYYY-MM>.html + an editions index; nav link.
- GROWTH.md gains the monthly duty (first shift of the month).
- Edition 000 "Bootstrap" generates now from real data.

## Experiment
- Hypothesis: editions get read: almanac pages accrue uniques comparable to the saga
- Metric: traffic uniques on almanac paths; Baseline: 0; Review-after: 2026-10-05

### Acceptance checks
1. Edition 000 counts match the ledger (iterations, ships) exactly.
2. Missing budget data produces the honest line, not zeros presented as fact.
3. Editions index renders; nav links it.
