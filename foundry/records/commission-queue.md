---
name: commission-queue
title: The Commission Queue
category: growth
stage: spec
kind: feature
version: null
components: [site,worker]
one_liner: A sanitized public status board for commissions - patrons watch progress without asking.
tags: [commissions, transparency, queue]
created: 2026-07-05
updated: 2026-07-05
---

## Pitch
Paying strangers deserve a window of their own. Titles only (patron text stays
fenced and untrusted), status derived from the line.

## Spec
- intake.py additionally maintains state/commissions.json: issue, title
  (sanitized: title line only, truncated, no body), status queued|building|
  delivered, opened; status flips when a commission-born record moves stages.
- build renders site/queue.html: empty - "The counter is open" + commission link;
  otherwise rows with status chips. Nav gains Queue.
- No amounts, no handles unless the patron opted into credit.

## Experiment
- Hypothesis: patrons stop asking for status: zero any-update comments on commission issues after ship
- Metric: status-request comments per commission; Baseline: 0; Review-after: 2026-10-05

### Acceptance checks
1. Fixture commissions.json renders rows; empty renders the open-counter line.
2. Sanitizer provably drops body text and fences.
3. Nav links Queue on index.
