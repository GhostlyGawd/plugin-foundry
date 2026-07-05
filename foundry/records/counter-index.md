---
name: counter-index
title: The Counter Index
category: context
stage: building
kind: feature
version: null
components: [site]
one_liner: Fuzzy search and tag filters on the shelf - find the right plugin in two keystrokes.
tags: [search, filters, shelf]
created: 2026-07-05
updated: 2026-07-05
---

## Pitch
The shelf is past the point where scanning beats searching. Cards already render
client-side from data.json, so filtering is a pure function away.

## Spec
- Search input above the shelf filters cards live on name + one_liner + tags.
- Tag chip row (union of published tags) toggles a tag filter; combines with text.
- Filtering is a pure function filterCards(q, tag, entries) exported for tests.
- Empty result renders "nothing on the shelf matches - suggest it" + idea link.
- No libraries, no analytics; full list stays server-visible in INDEX.md.

## Experiment
- Hypothesis: visitors who search reach a certificate faster; proxy - returning uniques hold or rise after ship
- Metric: GitHub traffic returning uniques (privacy law: no page analytics); Baseline: 0; Review-after: 2026-09-05

### Acceptance checks
1. Pure filter function unit-tested (node) across name/tag/one-liner cases.
2. Tag chips derive from data.json only; no hardcoded tags.
3. Empty state links the idea template.

## Build log
- i37: honest scope note — free-text search predates this record (shipped with
  scannable-window); this ship adds the tag-chip row (published-tag union,
  toggleable, ANDs with text), extracts the predicate into pure filterCards()
  between FILTER markers for unit testing, and links the empty state to the idea
  template. Suite added (node-guarded).
