---
name: token-cost-badges
title: Token-Cost Badges
category: growth
stage: published
kind: feature
version: null
verified: 2026-07-13
components: [site, docs]
one_liner: Every card shows what a plugin costs your context — est. always-on tokens, and when it was last verified.
tags: [trust, transparency, tokens]
created: 2026-07-05
updated: 2026-07-06
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

## Review log
### Review — i94
- Estimator honest and stable: chars/4 ceil over always-loaded frontmatter only;
  re-ran plugin-smith (113) and fork-a-foundry (90) — matches the Test log.
  All 7 published plugins carry always_on_tokens + verified. "est." labeling
  everywhere the number appears (cards, certificates, INDEX). Zero-desc edge
  renders "unmeasured" (0 is falsy) — more honest than "~0 tok"; acceptable.
- DEFECT (docs truth / the feature's own trust promise): spec says stale
  `verified` dates (> 60 days) render dimmed. No such logic exists in build.py —
  a ✓ stamp looks equally fresh at 6 days and 6 months. Weekly re-verify masks
  this only while CI runs; if the factory pauses, every badge quietly overstates
  freshness — precisely what this feature exists to prevent. Unlogged deviation,
  load-bearing clause.
- Axes: scope 5 · prompt n/a · thrift 5 · hook-safety n/a · docs-truth 3 ·
  structure 5.
REVIEW: bounced — implement the >60-day dimmed state (or amend the spec with a
justification that survives a stopped factory); add an executable check.

## Build log (post-bounce)
- i95: stale state built client-side in badge(): verified > 60 days → chip dims
  (.chip.tok.stale, opacity .5) and the title says why. Client-side deliberately —
  a build-time check would itself freeze if the factory stopped, which is the exact
  failure the reviewer named. Certificates already print the literal verified date
  in the meta line (self-dating, reader can judge), so the card badge — a bare ✓ —
  was the only misleading surface. Under ADR-009 feature authorization.

### Test pass — i96 (post-bounce re-test)
- tier 1: executable suite landed (foundry/tests/token-cost-badges/badges.test.sh)
  3/3: estimator determinism across all 7 published plugins, badge-number
  substantiation vs records (both type-normalized), stale-dimming regression
  pinned at the 60-day threshold
- tier 2: n/a (site feature)
- tier 3: title copy explains WHY a chip is dim ("verification older than 60
  days") — honest degradation, not decoration
- defects: none in product — one test-harness type mismatch (data.json strings vs
  record ints) fixed in the test itself
TEST VERDICT: pass

### Review — i97 (post-bounce)
- i94 defect cured the right way: client-side check means the dimming keeps
  working precisely when the factory stops — the failure mode that motivated the
  bounce. Threshold and copy pinned by an executable regression.
- Certificates print the literal verified date (self-dating); the bare-✓ card was
  the misleading surface and is the one fixed. Scope judgment sound.
- Axes: scope 5 · prompt n/a · thrift 5 · hook-safety n/a · docs-truth 5 ·
  structure 5.
REVIEW: approved — spec and shipped artifact now agree; staleness degrades honestly.

### Published — i98 (maintainer)
Live: every card shows its context price or says "unmeasured"; stale verifications
dim honestly. Experiment armed — review 14 days post-deploy (clones per unique vs
prior snapshots).
