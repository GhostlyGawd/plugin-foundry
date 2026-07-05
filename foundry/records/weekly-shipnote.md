---
name: weekly-shipnote
title: Weekly Shipnote
category: growth
stage: rc
kind: feature
version: null
components: [workflow, docs]
one_liner: A weekly digest the loop writes itself — shipped, moved, killed, fuel — posted as an issue every Monday.
tags: [digest, retention, narrative]
created: 2026-07-04
updated: 2026-07-05
---

# Weekly Shipnote

Ticker lines are for the floor; returners want the week's story.

## Pitch
- **Job:** a subscribable narrative artifact (watch the repo → get the note) that
  compresses seven days of journal into honest sections.
- **User:** returners and anyone deciding whether to star/watch.
- **Components:** tools/shipnote.py (writes only what journal/records substantiate)
  + shipnote.yml (Monday cron, idempotent per ISO week, posts a `shipnote` issue).

## Spec
- Sections: Shipped (with install lines), Moved on the line, Killed or shelved,
  Fuel (ledger month-to-date). No forward promises the backlog can't substantiate.
- Idempotence: one note per ISO week, ever.
### Acceptance checks
1. shipnote.py on the live journal produces all applicable sections with real data.
2. Empty weeks render honest "quiet week" copy, not filler.
3. Workflow refuses a duplicate week.

## Experiment
- **Hypothesis:** a digest converts visitors to watchers — `watchers` rises in the
  two snapshots after each note vs. before.
- **Metric:** `watchers` in METRICS.jsonl.
- **Baseline:** from first real snapshot.
- **Review-after:** after 3 shipnotes.

## Build log
- i0(v5): generator + weekly workflow landed; promoted from the idea pool per the
  v5 slate.

## Test log
### Test pass — i0(v5)
- tier 1: pass — shipnote.yml parses; script stdlib-only
- tier 2: n/a (workflow) — duplicate-week guard verified by reading the gh search gate
- tier 3: check 1 executed live (30-day run produced Shipped + Moved + Fuel from
  real journal/ledger); check 2 via empty-window dry run
- defects: none found — probed: malformed journal timestamp (skipped cleanly)
TEST VERDICT: pass
