---
name: community-hall
title: Hall of Prospectors & Patrons
category: growth
stage: published
kind: feature
version: null
components: [site]
one_liner: Real contributor recognition — who suggested what shipped, who fueled what got built.
tags: [recognition, community, ladder]
created: 2026-07-05
updated: 2026-07-06
---

# Hall of Prospectors & Patrons

The ladder's top rungs deserve a wall. Counts come from records only.

## Pitch
- **Job:** durable recognition for the people who shape the shelf.
- **User:** suggesters and patrons; visitors gauging whether participation matters.
- **Components:** window section derived from `prospected_by` and opt-in `patron`
  fields across records — the section renders only once it has a first name.

## Spec
- Prospectors ranked by shipped suggestions, then formalized; patrons listed only
  with explicit opt-in; empty hall renders nothing (no manufactured community).
### Acceptance checks
1. Fixture records populate ranked prospectors with issue links.
2. Zero-data state renders no section at all.
3. No name appears without a record field behind it.

## Experiment
- **Hypothesis:** a visible hall lifts repeat suggestions per suggester.
- **Metric:** authorship spread in votes.json + formalized counts in the journal.
- **Baseline:** empty hall (genesis).
- **Review-after:** 30 days after first entry appears.

## Build log
- i0(v5): derivation + conditional section landed with the v5 window; QA pass with
  fixtures is the remaining gate before rc.

## Test log
### Test pass — i4
- tier 1: pass
- tier 2: n/a (site feature)
- tier 3: fixture prospected_by/suggested_in on a record → hall ranks
  @fixture-prospector, certificate meta shows "prospected by @fixture-prospector
  (#42)"; fixture removed → hall data empty and section hidden (renders nothing)
- defects: none found — probed: prospected_by without suggested_in (credit renders, no link)
TEST VERDICT: pass

## Review log
### Review — i127
- Derivation re-read post-i121 (the hall gained the Breakers list from
  adversarial-qa-bounties): all three lists remain artifact-substantiated —
  prospectors/patrons from record fields, breakers from shipped changelogs; the
  hide-when-empty condition covers all three, so the no-manufactured-community
  law still holds exactly.
- Ranking honest (shipped desc, then formalized, then login — no recency bias to
  game); patrons opt-in only; QA's i4 fixture pass covered credit-without-link.
- Axes: scope 5 · prompt n/a · thrift 5 · hook-safety n/a · docs-truth 5 ·
  structure 5.
REVIEW: approved — recognition that can't be bought or faked, hidden until earned.


### Published — i128 (maintainer)
Live (hidden, correctly, until the first name). Experiment clock starts at first
entry per the record.
