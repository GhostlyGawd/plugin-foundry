---
name: adversarial-qa-bounties
title: Adversarial QA Bounties
category: growth
stage: spec
kind: feature
version: null
components: [docs, template, site]
one_liner: Break a published plugin, earn a permanent Hall entry — community red-teaming as a growth loop.
tags: [community, qa, security, ladder]
created: 2026-07-05
updated: 2026-07-05
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
