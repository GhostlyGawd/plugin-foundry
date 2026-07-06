---
name: pr-gated-publishes
title: PR-Gated Publishes
category: growth
stage: spec
kind: feature
version: null
components: [workflow]
one_liner: Shifts can land as pull requests — a human veto window that costs the human nothing unless they use it.
tags: [governance, trust, veto]
created: 2026-07-05
updated: 2026-07-05
---

# PR-Gated Publishes

Full autonomy is the spectacle; a veto window is the safety valve. The mechanism
already exists (run-shift.yml `mode: pr`) — this experiment decides whether it
becomes the default.

## Pitch
- **Job:** let the operator (and the public) review a shift before it lands, without
  slowing the line when nobody objects.
- **User:** the operator; indirectly, everyone who trusts the marketplace more for it.
- **Components:** the shipped `mode: pr` path in run-shift.yml; this experiment
  governs making it the scheduled default.

## Spec
- Dispatch shifts with `mode: pr` for the trial window; scheduled shifts stay
  `direct` until the verdict.
- Merging a shift-PR = approval; closing = veto (operator leaves a note the next
  auditor must read).
- QA workflow runs on the PR, so vetoes come informed.
### Acceptance checks
1. A `mode: pr` shift produces a branch `shift/<run_id>` and an open PR with the
   shift summary; nothing lands on main until merge.
2. Direct mode remains untouched; tags still push on merge-to-main shifts.
3. Journal + ADR record the trial's start and the verdict.

## Experiment
- **Hypothesis:** a veto window raises trust signals (stars/watchers trend) without
  stalling the line — median PR-to-merge under 24h and zero shifts lost.
- **Metric:** `stars`, `watchers` in METRICS.jsonl across the trial; PR merge
  latency and veto count from the trial's PRs.
- **Baseline:** to be read from the ledger when the trial starts.
- **Review-after:** 10 shift-PRs or 21 days, whichever first.

## Trial log — i144 (growth, interim)
Observed data (operator-directed session PRs, not yet cron `mode: pr` shifts):
- PR #9 (v8 slate): 48 commits / 12 publishes gated behind the operator; merged
  ~3 minutes after ready-for-review; zero vetoes; every gate green pre-merge.
- v9 slate (this PR): same mechanism, second run.
INTERIM VERDICT: directed multi-iteration slates ride PRs from now on (ADR-017) —
the veto window demonstrably costs nothing when the work is clean. The *scheduled*
default stays `direct` until real `mode: pr` cron shifts produce the 10-PR/21-day
data this spec demands; that clock starts with the factory (Gate A). Record stays
at spec until then — the experiment is armed, not finished.
