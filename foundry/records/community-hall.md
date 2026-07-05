---
name: community-hall
title: Hall of Prospectors & Patrons
category: growth
stage: building
kind: feature
version: null
components: [site]
one_liner: Real contributor recognition — who suggested what shipped, who fueled what got built.
tags: [recognition, community, ladder]
created: 2026-07-05
updated: 2026-07-05
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
