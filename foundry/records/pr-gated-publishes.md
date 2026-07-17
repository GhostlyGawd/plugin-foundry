---
name: pr-gated-publishes
title: PR-Gated Publishes
category: growth
stage: published
kind: feature
version: null
components: [workflow]
one_liner: Every automated content change lands as a pull request behind required gates and a human veto window.
tags: [governance, trust, veto]
created: 2026-07-05
updated: 2026-07-17
---

# PR-Gated Publishes

Full autonomy is the spectacle; a veto window is the safety valve. The trial
graduated into the repository's permanent landing policy on 2026-07-17.

## Pitch
- **Job:** let the operator (and the public) review a shift before it lands, without
  slowing the line when nobody objects.
- **User:** the operator; indirectly, everyone who trusts the marketplace more for it.
- **Components:** shift, demo, orchestrator, and weekly re-verification workflows;
  the `main` ruleset; Gates and CodeQL.

## Spec
- Every automated content mutation pushes a purpose-named branch and opens a PR;
  no workflow pushes commits to `main`.
- Merging an automation PR = approval; closing = veto (operator leaves a note the next
  auditor must read).
- Gates and CodeQL run on every PR, and the `main` ruleset requires them.
### Acceptance checks
1. A shift produces a branch `shift/<run_id>` and an open PR with the
   shift summary; nothing lands on main until merge.
2. Orchestrator and weekly re-verification jobs also open PRs; no bare main push remains.
3. The active main ruleset requires pull requests plus green Gates and CodeQL checks.

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
the veto window demonstrably costs nothing when the work is clean.

## Publish log — 2026-07-17

The safety boundary is now universal rather than experimental: hosted Codex shifts,
demo recording, orchestrated agent batches, and weekly verification stamps only
propose PRs. Repository rules require a PR and green Gates + CodeQL before `main`
can move. Release-tag publishing remains a separate, immutable-tag operation.

## Build log

- The orchestrator's `direct` dispatch choice was removed; every batch starts a
  run-scoped branch and opens a pull request.
- Weekly re-verification now proposes changed stamps from a run-scoped branch.
- The hosted Codex shift and demo workflows were already split into read-only model
  jobs and keyless PR landing jobs.

## Test log

- Workflow-security checks assert that orchestrator and re-verification paths contain
  PR creation and no bare `git push` to the checked-out branch.
- Build, validation, state validation, golden evals, adapter drift, and workflow YAML
  checks pass locally; required Gates and CodeQL enforce the same boundary on the PR.

TEST VERDICT: pass

## Review log

- PR-only automation makes the repository ruleset enforceable without silently
  breaking a scheduled writer.
- Tag and release operations remain deliberately separate: tags are immutable release
  pointers and do not bypass review for branch content.
- Write-capable jobs still use scoped GitHub tokens, but they can only propose branches;
  they cannot satisfy the required checks by writing around the review boundary.

REVIEW: approved
