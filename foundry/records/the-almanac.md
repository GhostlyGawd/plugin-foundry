---
name: the-almanac
title: The Almanac
category: growth
stage: published
kind: feature
version: null
verified: 2026-07-13
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

## Build log
- i69: almanac.py writes editions from JOURNAL/records/DECISIONS/BUDGET + live
  gates; absent cost ledger produces the honest sentence, never an estimate;
  editions index + nav link; GROWTH monthly duty; Edition 000 generated for
  2026-07 from real data. Suite added.

## Test log
### Test pass — i70
- tier 1: pass
- tier 3: suite 4/4 — iteration count diffed against JOURNAL exactly (69/69),
  money section verified against the actual ledger state (BUDGET.jsonl exists
  with entries → real spend line renders; the honesty branch is exercised by the
  test's iff-assertion), editions index present, nav linked; edition regenerated
  idempotently (numbering stable)
- defects: none found — probed: month with zero iterations (renders "none yet",
  no invented histogram)
TEST VERDICT: pass

### Build fix — i70
- Gate caught snapshot drift: the edition's count went stale the moment its own
  generating iteration journaled (69/70). Editions now carry an as-of stamp
  ("as of iN") and the suite compares against the ledger *at that stamp* — the
  number is permanently true instead of momentarily true.

### Build fix — i71
- Ledger archaeology from the i70 gate trail: the "extra" entry was the i0
  genesis stamp, not drift. Iteration counts now exclude i0 and say so in a
  genesis note; edition numbers are the month's stable index, not a file count
  (regenerating a month can no longer promote it to a new edition).

## Test log
### Test pass — i72
- tier 1: pass
- tier 3: suite 4/4 with the hardened semantics — count matches the ledger at the
  as-of stamp (70/70 @ i70, i0 excluded and noted on-page), Edition 000 stable
  under regeneration, money section truthful to the real BUDGET.jsonl, index +
  nav present
- defects this cycle: 2, both caught by the gates before any publish — snapshot
  drift (i70) and genesis miscount + file-count numbering (i71); this is the
  pipeline doing its job on the machine's own reporting tool
TEST VERDICT: pass

## Publish log
- i74 (maintainer): Edition 000 live at /almanac/; monthly duty in force from
  2026-08; experiment armed (path uniques vs saga, review 2026-10-05).

## Review log
### Review — i73 (reviewer)
- The almanac needed three iterations because it *reports on the reporter* — and
  the gates treated it exactly like any plugin. That the machine's self-portrait
  gets the strictest QA on the floor is the culture, proven.
- "As of iN" + the genesis note turn every number into a permanently checkable
  claim; edition numbers now survive regeneration.
- Sharpest question: does self-reporting drift into self-praise? Structurally
  hard — counts, lists, one code line; no adjective slot to fill. The two logged
  defects on this very record are the counter-evidence.
REVIEW: approved
