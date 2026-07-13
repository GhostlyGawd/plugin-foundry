---
name: weekly-shipnote
title: Weekly Shipnote
category: growth
stage: published
kind: feature
version: null
verified: 2026-07-13
components: [workflow, docs]
one_liner: A weekly digest the loop writes itself — shipped, moved, killed, fuel — posted as an issue every Monday.
tags: [digest, retention, narrative]
created: 2026-07-04
updated: 2026-07-06
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

## Review log
### Review — i109
- Substantiation law holds: every section derives from journal/records/ledger/gh;
  quiet-week copy honest; duplicate-week gate read and sound (search+grep per ISO
  week); mailbag section evidence-labeled and fail-open when gh is absent.
- DEFECT 1 (honest-compression): "Moved" silently caps at the last 12 — dry-run
  on the live journal shows 21 moves this week, 9 dropped without a trace. House
  precedent (theater, i-v7 review): a windowed view must say where the unabridged
  version lives. First real shipnote would ship the violation.
- DEFECT 2 (ops): `gh issue create --label shipnote` hard-fails when the label
  doesn't exist in the repo — nothing creates it, OPERATIONS doesn't mention it;
  the first Monday run would die before posting note #1. Ensure-label step (or
  fail-open create without label) required.
- Axes: scope 5 · prompt n/a · thrift 5 · hook-safety n/a · docs-truth 3 ·
  structure 4.
REVIEW: bounced — silent 12-move cap (add the "N more, see journal" line) and
first-run label failure; both one-liners, both provable by test.

## Build log (post-bounce)
- i110: (1) truncation pointer — >12 moves appends "…and N earlier move(s) this
  week — unabridged in state/JOURNAL.md"; verified live (9 earlier moves named).
  (2) shipnote.yml ensures the label exists before create (`gh label create ||
  true` — idempotent, fail-open). Tools edit rides ADR-009 feature authorization.

### Test pass — i111 (post-bounce re-test)
- tier 1: executable fixture suite (foundry/tests/weekly-shipnote/generator.test.sh)
  4/4 — busy week (sections + pointer with exact count), quiet week (honest copy,
  no phantom pointer), 12-move boundary, workflow guards (dup-week gate + label
  ensured BEFORE create, order-checked)
- tier 2: n/a (workflow)
- tier 3: live dry-run — pointer names 91 real earlier moves; nothing retouched
- defects: none found
TEST VERDICT: pass

### Review — i112 (post-bounce)
- Both defects cured minimally: pointer states the exact dropped count and the
  unabridged source; label ensure is idempotent, fail-open, and ordered before
  create (order pinned by test). Fixture-based suite means the checks won't rot
  as the journal grows — right call by QA.
- Axes: scope 5 · prompt n/a · thrift 5 · hook-safety n/a · docs-truth 5 ·
  structure 5.
REVIEW: approved — the digest now compresses honestly and survives its first Monday.

### Published — i113 (maintainer)
Live: Monday cron posts the note once per ISO week; label self-ensures; truncation
says what it dropped. Experiment armed — review after 3 notes (watchers trend).
