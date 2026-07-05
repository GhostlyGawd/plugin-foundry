---
name: contributor-cards
title: Contributor Cards
category: growth
stage: published
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

## Test log
### Test pass — i62
- tier 1: pass
- tier 3: fixture suite 5/5 live (prospector yields a card with derived counts +
  since-date, self-contained — no href=http/<image>/url()/@import, certificate
  links appear, empty hall wipes site/card clean); one honest note: the first run
  caught the *test* overclaiming (xmlns URI tripped a naive http scan) — the
  predicate now tests actual external fetches
- defects: 1 in the test, 0 in the artifact; probed: login sanitization
  (path-unsafe chars stripped before filenames)
TEST VERDICT: pass

## Publish log
- i64 (maintainer): generator live in every build; cards appear with the first
  real credit; experiment armed (README-referrer proxy, review 2026-10-05).

## Review log
### Review — i63 (reviewer)
- The card's fine print — "every credit above is a line in an append-only ledger"
  — is the whole product: shareable status backed by receipts.
- Empty-wipes-clean matters more here than anywhere; a stale card for a renamed
  contributor would be a small lie in someone's README.
- QA logging its own test's defect is the culture working; the ledger now shows
  a check that overclaimed and was corrected.
- Sharpest question: can a card inflate? Only if collect_hall does — counts flow
  from the same aggregation the hall page already answers for.
REVIEW: approved
