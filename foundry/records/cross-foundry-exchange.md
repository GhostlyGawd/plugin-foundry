---
name: cross-foundry-exchange
title: Cross-Foundry Exchange
category: growth
stage: spec
kind: feature
version: null
components: [docs, workflow]
one_liner: Sister foundries pass ideas (and someday commissions) to whichever workshop fits best — a federation of night shifts.
tags: [network, federation, moonshot]
created: 2026-07-05
updated: 2026-07-06
---

## Pitch
Once the network page exists, the next primitive is a hand-off: an idea issue
labeled `exchange:<sister>` gets a courteous referral comment linking their
intake. Parked behind foundry-network's verdict.

## Spec
- Scope (deliberately small): REFERRALS ONLY. An idea issue labeled
  `exchange:<sister>` (sister = a name present in foundry/network.json) gets a
  single courteous comment: "this fits <sister>'s line better — their intake:
  <url from network.json>/issues/new?template=idea.yml" — and stays open here
  unless the author closes it. No automation moves content between repos.
- The maintainer applies the label during intake triage, only when a registered
  sister's declared focus (its network.json note) clearly fits better.
- Nothing fires while network.json is empty; no sister, no exchange.

### Acceptance checks
1. Referral comment template documented; links derive ONLY from network.json
   entries (never free-typed URLs).
2. No workflow or tool auto-closes or auto-moves an exchanged issue.
3. With an empty network, the exchange path is provably inert.

## Experiment
- **Hypothesis:** referrals make sisters reciprocate — ≥1 inbound referral
  within 60 days of the first outbound one.
- **Metric:** issues labeled exchange:* here; inbound referral mentions.
- **Baseline:** 0 (no sisters registered yet).
- **Review-after:** 2026-11-06.
