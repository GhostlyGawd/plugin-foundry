---
name: counter-index
title: The Counter Index
category: context
stage: published
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

## Test log
### Test pass — i38
- tier 1: pass
- tier 3: node unit suite 5/5 on the extracted pure function (no-filter, text over
  one_liner+tags, tag chip, text AND tag, no-match); chips provably derive from
  data (flatMap over entry tags in the built window — zero hardcoded tags);
  empty state carries the idea-template link in the built page
- defects: none found — probed: tag toggle-off (second click clears), entries
  missing tags array (guarded with ||[])
TEST VERDICT: pass

## Publish log
- i40 (maintainer): live on the window this build; experiment armed (returning-
  uniques proxy, review 2026-09-05).

## Review log
### Review — i39 (reviewer)
- Scope honesty is the standout: the record credits scannable-window for the text
  search instead of re-claiming it — the ledger stays trustworthy.
- The pure-function extraction turns UI behavior into a tested contract; markers
  make the test read the *shipped* code, not a copy.
- AND semantics between text and tag are the right default (narrowing, never
  surprising); toggle-off on second tap matches chip conventions.
- Sharpest question: can a tag chip appear for an unpublished record and dead-end
  a filter? No — chip union is published-only; filtered non-published cards still
  match by tag if present, which is a feature (watch it move down the line).
REVIEW: approved
