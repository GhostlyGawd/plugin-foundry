---
name: token-cost-badges
title: Token-Cost Badges
category: growth
stage: rc
kind: feature
version: null
components: [site, docs]
one_liner: Every card shows what a plugin costs your context — est. always-on tokens, and when it was last verified.
tags: [trust, transparency, tokens]
created: 2026-07-05
updated: 2026-07-05
---

# Token-Cost Badges

No marketplace tells you what a plugin costs your context window. This one does.

## Pitch
- **Job:** make the invisible price of installing visible before installing.
- **User:** installers deciding between plugins; the QUALITY.md thrift bar, enforced in public.
- **Components:** tools/tokencost.py (deterministic estimator, labeled "est."),
  `always_on_tokens` + `verified` record keys written by QA each pass, badge on
  cards and birth certificates.

## Spec
- Estimator: sum of always-loaded frontmatter description characters / 4, ceil —
  never presented as exact; badge copy reads "~N tok · est".
- QA duty (TESTING.md): record value + verified date at every test pass; stale
  verified dates (> 60 days) render dimmed.
- Unmeasured plugins say "unmeasured", never a guess (dark-pattern law).
### Acceptance checks
1. tokencost.py returns stable values for plugin-smith and fork-a-foundry.
2. Cards with the keys render the badge; cards without render "unmeasured".
3. No badge anywhere the repo can't substantiate.

## Experiment
- **Hypothesis:** visible cost increases install intent for thrifty plugins —
  clones_14d per unique rises after ship vs. the two prior snapshots.
- **Metric:** `clones_14d`, `uniques_14d` in METRICS.jsonl.
- **Baseline:** to be read from the ledger at first real snapshot.
- **Review-after:** 14 days post-deploy.

## Build log
- i0(v5): estimator, schema keys, QA duty, card + certificate badges.

## Test log
### Test pass — i0(v5)
- tier 1: pass — validate.py green with new optional keys
- tier 2: n/a (site feature) — est values: plugin-smith 113, fork-a-foundry 90
- tier 3: checks 1–3 → stable estimates, badge/unmeasured states render, zero
  unsubstantiated numbers found
- defects: none found — probed: missing keys, malformed verified date, zero-desc plugin
TEST VERDICT: pass
