---
name: contributor-cards
title: Contributor Cards
category: growth
stage: building
kind: feature
version: null
components: [site]
one_liner: A shareable, kraft-styled SVG credit card per contributor - prospects, patronages, breaks, since-date.
tags: [credit, svg, ladder]
created: 2026-07-05
updated: 2026-07-05
---

## Pitch
Credit that travels recruits. A card someone can pin in their README turns one
contribution into an advertisement for the next.

## Spec
- tools/cards.py renders site/card/<login>.svg from hall data (prospector /
  patron / breaker counts + first-credit date) in brand colors.
- Certificates and the hall link the card next to each credited handle.
- Empty hall generates nothing (empty-renders-nothing law).

## Experiment
- Hypothesis: card links get embedded in contributor READMEs within 60 days of first credits
- Metric: inbound referrers from github.com README paths (traffic API); Baseline: 0; Review-after: 2026-10-05

### Acceptance checks
1. Fixture prospector yields a valid SVG with correct counts; removal yields none.
2. SVG is self-contained (no external fonts or requests).
3. Hall and certificates link cards only when they exist.

## Build log
- i61: tools/cards.py renders self-contained kraft SVGs from hall data (prospects,
  shipped, patronage, since-date from record created); build order fixed so cards
  exist before pages; certificates and hall rows link cards only when the file
  exists; empty hall wipes site/card entirely. Fixture suite added.
