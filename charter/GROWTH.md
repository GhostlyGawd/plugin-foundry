# GROWTH — The Engagement Doctrine

Engagement is a product this workshop builds, on the same line, at the same bar —
plus one law plugins don't have: **every engagement feature is an experiment**, and
experiments answer to data, not to the iteration that shipped them.

## What we optimize (and what we never touch)
Optimize **earned attention** up the ladder:

```
visitor → returner → voter → suggester → patron → installer
```

Real signals only: return traffic, votes on idea issues, free suggestions,
commissions, stars/watchers, installs-proxy (clones + marketplace adds we can see).

**Banned, permanently (dark-pattern law):** fabricated or inflated counters, fake
scarcity or urgency, simulated activity (the ticker shows only true journal lines,
ever), attention traps (autoplay, infinite feeds, nagging), and any metric shown to
users that the repo can't substantiate. The spectacle is compelling *because it is
real*; faking it destroys the only asset. Violations are red-build severity.

## The experiment protocol (kind: feature records)
- **At spec**, the `## Experiment` section must state: Hypothesis (behavior change
  expected), Metric (from METRICS.jsonl or votes.json), Baseline (current value or
  "unknown — first measurement"), and Review-after (a date or N shifts, default 14
  days).
- One variable at a time where feasible; if features must bundle, say which metric
  belongs to which.
- **At review time** (growth role; overdue reviews are P1): append `## Verdict` with
  the data observed and rule `VERDICT: keep | kill | extend — {reason}`.
  - keep → stays published; learning noted.
  - kill → stage `deprecated`, feature reverted, learning noted — the graveyard of
    experiments teaches exactly like the plugin shelf does.
  - extend → new review date; extending twice without movement = kill.
- **Small-sample honesty:** with thin traffic, most deltas are noise. "Insufficient
  data" is a legitimate finding; torturing noise into a win is not. When in doubt,
  extend once, then kill.

## Instruments
- `tools/metrics.py` (runs every shift): snapshot → `state/METRICS.jsonl`
  (append-only growth ledger) and vote counts → `foundry/votes.json`.
- Sources: GitHub API (stars, watchers, forks, 14-day repo traffic, 👍 reactions on
  open `idea` issues, open commissions) and, optionally, a privacy-respecting page
  counter (GoatCounter) if the operator wires it — no cookies, no tracking pixels,
  nothing that needs a consent banner. Absent instruments record `null`, never a guess.

## Calibration
If the last 4 experiment verdicts are all `keep`, measurement has gone soft — audit
becomes P0 (same logic as the QA rubber-stamp tripwire). The Auditor's monthly read
includes: verdict mix, ladder movement, and whether any shipped feature lacks an
open or closed experiment (orphan features get one retroactively or get killed).

## The Almanac (monthly duty)
First shift of each month, the growth role runs `python3 tools/almanac.py` and
commits the edition. Numbers come from JOURNAL, records, DECISIONS, BUDGET.jsonl
and the live gates; a missing ledger is named, never estimated around.
