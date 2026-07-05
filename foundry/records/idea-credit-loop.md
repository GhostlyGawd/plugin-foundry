---
name: idea-credit-loop
title: Idea-Credit Loop
category: growth
stage: rc
kind: feature
version: null
components: [site, docs]
one_liner: Community suggestions carry their prospector's name from issue to card to birth certificate — with a thank-you at every milestone.
tags: [community, recognition, retention]
created: 2026-07-05
updated: 2026-07-05
---

# Idea-Credit Loop

Recognition is the cheapest honest retention lever that exists. Close the loop:
suggest → formalized → credited → thanked → shipped.

## Pitch
- **Job:** make suggesting feel like contributing, because it is.
- **User:** voters and suggesters climbing the ladder.
- **Components:** `prospected_by` + `suggested_in` record keys; Ideator credit duty
  (ROLES.md); "prospected by @x (#N)" on cards and certificates; milestone comments
  on the source issue.

## Spec
- Credit is set only from real issue authorship; opt-in `patron` naming for
  commissions; nothing rendered without a record field behind it.
- Card line links the source issue; certificate carries it in the meta row.
### Acceptance checks
1. A record with the keys renders credit on card + certificate with a working link.
2. Records without the keys render nothing (no placeholder flattery).
3. ROLES/LOOP name the duty explicitly, including the shelf-outcome comment.

## Experiment
- **Hypothesis:** visible credit lifts repeat participation — distinct suggesters
  and per-suggester repeat rate rise across the review window.
- **Metric:** `open_ideas` authorship spread (from votes.json) and formalized-idea
  count in the journal.
- **Baseline:** 0 community-sourced records (genesis).
- **Review-after:** 21 days post-deploy.

## Build log
- i0(v5): schema keys, role + protocol duties, card and certificate rendering.

## Test log
### Test pass — i0(v5)
- tier 1: pass — validator tolerant of optional keys
- tier 2: n/a (site feature)
- tier 3: checks 1–3 → fixture record rendered credit + link; absent keys rendered
  nothing; duties present in ROLES.md and LOOP.md
- defects: none found — probed: missing suggested_in with present prospected_by
TEST VERDICT: pass
