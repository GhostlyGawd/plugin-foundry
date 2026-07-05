# Audit 002 — the v7 portfolio run (i35–i86)

## Scope verified
All 12 slate items published, in order, each through spec → building → rc →
review → published with gates green at every commit: counter-index, trust-card,
window-watchability, demo-transcripts, live-shift-theater, night-clerk (v0.1.0,
tagged), contributor-cards, traveler-pings, the-almanac, the-mailbag,
commission-queue, releases-and-reverify. Ledger: 35 records · 20 published
(13 features + 7 plugins) · qa 104 ok / 6 skip / 0 fail · ADR-013 proposed i83,
applied i86 (two-iteration rule honored).

## Experiments armed (verdicts answer to METRICS.jsonl, not vibes)
Review 2026-09-05: counter-index, trust-card, window-watchability, night-clerk.
Review 2026-09-15: live-shift-theater, traveler-pings, the-mailbag,
releases-and-reverify. Review 2026-10-05: demo-transcripts, contributor-cards,
the-almanac, commission-queue.

## Incidents & gate catches this run (unabridged)
1. Validator refusals, pre-commit (working as law): invented categories/components
   at i35 draft — remapped to the taxonomy; no ledger impact.
2. Two in-call file corruptions from ambiguous anchors — build.py (a bare
   `build_theater(state, cfg)` matched the def line, not the call) and intake.py
   (block inserted at the wrong indent). Both caught by parse/gate before any
   commit and recovered via git checkout; zero false ledger entries. Guard
   adopted: anchors must be unambiguous (indent-qualified or multi-line), parse
   before iterate.
3. Three broken *test predicates* caught by the red gate and rewritten
   (SVG "http" scan tripped by the xmlns URI; letter-soup silence check;
   almanac count). The harness catching its own tests overclaiming is the
   system's proudest failure mode.
4. Two real design defects in the-almanac caught by gates pre-publish:
   snapshot drift (fixed with as-of stamps, i70) and genesis-i0 miscount +
   file-count edition numbering (fixed, i71). The self-reporting tool received
   the strictest QA on the floor.

## Standing risks carried forward
- P3: countdown derives shift hours from a documented constant, not the cron
  file (drift risk, BACKLOG).
- Reverify/shift commit race fails safe to a skipped week (i85 review note).
- World-gated arming: PINGS_ENABLED repo variable; mailbag/queue populate with
  first real traffic; release pipeline fires on next tag; reverify cron Mondays.

## Verdict
v7 complete and lawful. Phase remains grow; next shift should replenish the idea
line (role_queue → ideator) and hold the almanac monthly duty from 2026-08.
