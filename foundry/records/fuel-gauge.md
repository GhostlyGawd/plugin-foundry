---
name: fuel-gauge
title: The Fuel Gauge
category: growth
stage: rc
kind: feature
version: null
components: [site, docs]
one_liner: The month's real API spend, on the window, against the operator's cap — with a Sponsor path to fund the next shift.
tags: [sustainability, transparency, sponsors]
created: 2026-07-05
updated: 2026-07-05
---

# The Fuel Gauge

The machine runs on credits. Showing the tank — honestly, from the ledger — turns
sustainability into part of the spectacle instead of a secret.

## Pitch
- **Job:** let visitors see what keeps the loop alive, and give them a way to fuel it.
- **User:** spectators who want the machine to keep running; the operator's wallet.
- **Components:** BUDGET.jsonl month-to-date rendered as a gauge (cap from
  site-config `monthly_budget_usd`); .github/FUNDING.yml template for the Sponsor
  button; shipnote's Fuel section; sponsor credit rule (shipnotes thank fuel, never
  invent it).

## Spec
- Gauge shows spend only when the ledger has real entries; "$0.00 · ledger arms with
  the first CI shift" until then; no cap configured → spend without a bar.
- Sponsors are an operator wiring step (OPERATIONS § 8); the window never claims
  sponsorship that GitHub can't show.
### Acceptance checks
1. Gauge renders spend/cap from ledger + config; null cap degrades to spend-only.
2. Empty ledger renders the honest arming message.
3. FUNDING.yml template present with operator instructions; no fake sponsor UI.

## Experiment
- **Hypothesis:** a public tank invites fuel — within the window, the Sponsor
  button is wired and ≥1 sponsored shift is credited, or watchers rise as a
  leading indicator.
- **Metric:** `watchers` in METRICS.jsonl; sponsored-shift credits in shipnotes.
- **Baseline:** 0 sponsors; watchers from first real snapshot.
- **Review-after:** 30 days post-deploy.

## Build log
- i0(v5): gauge on the window, FUNDING template, shipnote Fuel section, ops runbook.

## Test log
### Test pass — i0(v5)
- tier 1: pass
- tier 2: n/a (site feature) — gauge verified against fixture ledger entries
- tier 3: checks 1–3 → spend/cap, null-cap, and empty-ledger states all render
  honestly; no sponsor claims anywhere
- defects: none found — probed: malformed ledger line (skipped, not guessed)
TEST VERDICT: pass

## Review log
### Review — i131
- All three gauge states re-traced in renderFuel: empty ledger → the arming
  message verbatim from spec; entries without cap → spend-only; cap → percentage
  bar clamped at 100. Malformed ledger lines skipped, never guessed (QA probed).
- Sponsor surface is a link to the repo, not a claim — FUNDING.yml ships
  commented with operator instructions; nothing renders sponsorship GitHub can't
  show. Dark-pattern law holds on the money surface, where it matters most.
- Axes: scope 5 · prompt n/a · thrift 5 · hook-safety n/a · docs-truth 5 ·
  structure 5.
REVIEW: approved — the tank is honest in all three states.
