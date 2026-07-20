---
name: commission-queue
title: The Commission Queue
category: growth
stage: published
kind: feature
version: null
verified: 2026-07-20
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

## Build log
- i79: intake gains sanitize_title (title line only, fences/backticks/brackets
  stripped, 80-char cap) + a state/commissions.json ledger that rides the intake
  commit; build renders site/queue.html — status derives from the line (queued /
  on the line / delivered with paper-trail link), empty renders the open counter;
  nav gains Queue. Fixture suite added.

## Test log
### Test pass — i80
- tier 1: pass
- tier 3: suite 7/7 live — sanitizer provably drops body prose, fences, backticks
  and injected instructions (kept only the cleaned title line), truncates at 80,
  honest placeholder for empty titles; fixture ledger rendered a delivered row
  with its paper-trail link and a queued row; teardown restored the real state
  (open counter) and the nav link held
- defects: none found — probed: malformed commissions.json (load_json default []
  keeps the page up), commission number as int vs string (normalized both sides)
TEST VERDICT: pass

## Publish log
- i82 (maintainer): queue live at /queue.html with the counter open; first
  commission populates it via intake; experiment armed (status-request comments
  per commission, review 2026-10-05).

## Review log
### Review — i81 (reviewer)
- Sanitization at *intake*, not at render, is the right layer: patron prose never
  enters the repo's derived state at all, so no future renderer can leak it.
- Status derived from the line means the queue cannot be edited into optimism —
  a commission reads "delivered" only when a published record claims its number.
- The no-amounts rule keeps the board a status window, not a revenue billboard;
  that is the dark-pattern ban doing quiet work.
- Sharpest question: can two records claim one commission? by_comm keeps the
  last — flagged as acceptable now (one-commission-one-record is the intake
  contract), worth a validator rule if co-delivery ever becomes real.
REVIEW: approved
