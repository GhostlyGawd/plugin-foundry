---
name: commission-tiers
title: Commission Tiers
category: growth
stage: spec
kind: feature
version: null
components: [worker, docs]
one_liner: A pricing experiment — standard, rush, and named-sponsor commissions.
tags: [pricing, patrons, experiment]
created: 2026-07-05
updated: 2026-07-05
---

# Commission Tiers

One price fits nobody. Test whether patrons value speed and recognition.

## Pitch
- **Job:** let patrons choose priority level and public credit; fund more shifts.
- **User:** patrons; the fuel gauge.
- **Components:** two additional Stripe Payment Links (rush ~3×, sponsor ~5× with
  opt-in `patron` naming); worker maps link → label (`commission-rush`,
  `commission-sponsor`); intake orders the Commissions lane rush-first; window
  copy updated with the same honest terms.

## Spec
- Rush = front of the commission lane, not a guarantee; sponsor = rush + named
  credit on the shipped card and shipnote (opt-in text field).
- Refund posture per tier stated on each payment link (operator-owned).
### Acceptance checks
1. Worker labels issues by tier from the originating payment link.
2. Intake orders rush/sponsor ahead of standard within the lane.
3. Named credit renders only from an explicit opt-in field.

## Experiment
- **Hypothesis:** tiers raise commission revenue per month ≥2× without raising the
  shelf rate — patrons self-select honestly when terms are honest.
- **Metric:** open_commissions mix + Stripe revenue (operator-reported into the
  review) + shelf rate of commissioned records.
- **Baseline:** single-tier revenue over the prior 30 days.
- **Review-after:** 45 days after the operator wires the tier links.
