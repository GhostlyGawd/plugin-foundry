---
name: adversarial-qa-bounties
title: Adversarial QA Bounties
category: growth
stage: rc
kind: feature
version: null
components: [docs, template, site]
one_liner: Break a published plugin, earn a permanent Hall entry — community red-teaming as a growth loop.
tags: [community, qa, security, ladder]
created: 2026-07-05
updated: 2026-07-06
---

## Pitch
Published claims ("fails open", "never mutates unasked") deserve hostile eyes. A
bounty that pays in permanent credit turns skeptics into contributors and makes
the shelf's honesty *tested* honesty.

## Spec
- CONTRIBUTING.md Lane 3 is the front door (ships alongside this spec).
- Bug template gains a `bounty` checkbox: "this reproduces a break of a claim the
  record makes."
- Confirmed break → fix ships with `found_by: <handle>` in the CHANGELOG entry;
  Hall gains a "Breakers" section ranking confirmed finds; the fixed plugin's
  certificate credits the finder.
- Rules of engagement live in CONTRIBUTING (own machine, no third-party targets,
  findings not harm); out-of-scope reports get a kind decline + journal line.

## Experiment
- Hypothesis: public bounty credit yields ≥1 confirmed adversarial find within 60
  days of the window going live, at zero cash cost.
- Metric: confirmed `bounty` bugs; Baseline: 0; Review-after: 2026-09-15.

### Acceptance checks
1. Lane documented with rules of engagement; SECURITY cross-ref in place.
2. Hall renders a Breakers section only when a confirmed find exists.
3. Fix changelogs carry found_by credit.

## Build log
- i121: build complete — (1) bug template gains the bounty checkbox (claim-at-stake
  framing verbatim from spec); (2) CONTRIBUTING Lane 3 gains the SECURITY.md
  fencing cross-ref and names the Breakers mechanism; (3) collect_hall derives a
  ranked Breakers list from `found_by:` lines in shipped CHANGELOGs — credit is
  substantiated by the artifact, never hand-tallied — and renderHall shows the
  section only when at least one confirmed find exists (empty today, honestly).

## Test log
### Test pass — i122
- tier 1: executable suite (foundry/tests/adversarial-qa-bounties/bounties.test.sh)
  5/5 — lane docs + SECURITY cross-ref, bounty checkbox present, zero-find empty
  state (no phantom breakers on today's window), fixture found_by line surfaces
  as a ranked breaker via collect_hall against an isolated ROOT, window render
  gated on non-empty
- tier 2: n/a (docs/template/site feature)
- tier 3: read the checkbox copy as a reporter — "claim the record makes" framing
  keeps scope to published claims, matching the rules of engagement
- defects: none in product — fixture initially wrote found_by mid-line; the
  collector's dedicated-line convention is the stricter, false-positive-proof
  choice, fixture corrected to match
TEST VERDICT: pass
