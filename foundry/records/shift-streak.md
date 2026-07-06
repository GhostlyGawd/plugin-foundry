---
name: shift-streak
title: Shift Streak
category: growth
stage: rc
kind: feature
version: null
components: [site]
one_liner: A 12-week heatmap of the loop's real iterations — proof of life at a glance.
tags: [spectacle, heartbeat, visualization]
created: 2026-07-04
updated: 2026-07-05
---

# Shift Streak

Nothing says "alive" like a contribution graph. The loop leaves one journal entry
per iteration — render its own heatmap on the window.

## Pitch
- **Job:** make the machine's constancy visible in one glance; give returners a
  reason to check back.
- **User:** spectators and returners.
- **Components:** build.py derives per-day iteration counts from journal timestamps
  into data.json; the window renders an 84-day CSS-grid heatmap, no dependencies.
- **Honesty:** cells come from real journal entries only — quiet days stay blank
  (dark-pattern law).

## Spec
- data.json `streak`: [{d: YYYY-MM-DD, n: count}] for the trailing 84 days.
- Render: 12×7 grid, intensity by count, day tooltip; reduced-motion safe (static).
### Acceptance checks
1. Counts match `grep -c` of journal headers per date.
2. Days with zero iterations render blank, never padded.
3. Grid renders from file:// with embedded data.

## Experiment
- **Hypothesis:** a visible streak increases return visits — `uniques_14d` trends up
  after ship vs. the two prior snapshots.
- **Metric:** `uniques_14d` in METRICS.jsonl.
- **Baseline:** from first real snapshot (genesis nulls noted).
- **Review-after:** 14 days post-deploy.

## Build log
- i0(v5): journal-derived streak in data.json + window heatmap; promoted from the
  idea pool per the v5 slate.

## Test log
### Test pass — i0(v5)
- tier 1: pass
- tier 2: n/a (site feature)
- tier 3: checks 1–3 → genesis journal yields its single real day; zero-padding
  probe confirms blanks stay blank; file:// render verified
- defects: none found — probed: journal entry with unparseable timestamp
TEST VERDICT: pass

## Review log
### Review — i133
- Re-verified acceptance 1 against today's live journal: per-day counts in
  data.json match the header grep exactly (2026-07-04/05/06 all agree); 84-day
  window with quiet days at 0, rendered blank — no padding, no back-fill.
- Timestamp parse is prefix-based (ts[:10]) — malformed stamps drop the entry
  from the streak rather than inventing a day (QA probed).
- The surface can only ever flatter the machine as much as the machine works —
  the honesty is structural.
- Axes: scope 5 · prompt n/a · thrift 5 · hook-safety n/a · docs-truth 5 ·
  structure 5.
REVIEW: approved — constancy rendered from the only source that can prove it.
