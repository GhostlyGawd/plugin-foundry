---
name: releases-and-reverify
title: Releases & Weekly Re-verification
category: workflow
stage: rc
kind: feature
version: null
components: [workflow]
one_liner: Tags become GitHub Releases with real notes; a weekly cron re-runs every published suite and re-stamps freshness.
tags: [releases, cron, freshness]
created: 2026-07-05
updated: 2026-07-05
---

## Pitch
Install bases deserve a changelog push channel and proof the shelf still passes -
freshness as a standing promise, not a launch-day claim.

## Spec
- release-on-tag.yml: on tag push *-v*, tools/relnotes.py extracts the matching
  CHANGELOG section - gh release create (fails soft, alarms on repeat).
- qa.yml gains a weekly cron; a guarded step re-runs suites for all published and
  re-stamps verified: (and tested_with when the CLI is present) - metadata-only
  writes, exempt from the version-bump law (documented in charter/QUALITY.md).
- Re-verify failures open an ops-alarm issue naming the plugin.

## Experiment
- Hypothesis: stale-shelf risk goes observable: every published record verified within 7 days at all times
- Metric: max age of verified stamps across published; Baseline: 0; Review-after: 2026-09-15

### Acceptance checks
1. relnotes.py unit: extracts exactly the 0.1.0 section from commit-craft changelog.
2. Both workflows lint; re-verify step is guarded and fails soft to an alarm.
3. QUALITY documents the metadata exemption precisely.

## Build log
- i83: relnotes.py (exact-section extraction, refuses absent versions);
  release-on-tag.yml (notes from the changelog, ops-alarm on failure);
  qa.yml gains the Monday cron + a schedule-guarded reverify job (restamp.py:
  pure parse/stamp helpers unit-tested, main is CI-only to avoid qa recursion,
  stamps withheld from red suites, stale shelf raises an alarm). ADR-013
  proposed for the metadata exemption — applies no earlier than i85; the cron
  first fires Monday, after the ADR window closes. Two suites added.

## Test log
### Test pass — i84
- tier 1: pass
- tier 3: suites 13/13 live — relnotes extracts the exact section with proven
  exclusion of neighbors, refuses absent versions at both API and CLI levels
  (a release with no notes does not happen); both workflows lint; cron, schedule
  guard and dual ops-alarms asserted; restamp helpers unit-tested (red suites
  withhold stamps, insert-vs-refresh both covered) without invoking main —
  the qa-recursion trap was designed out, not patched around
- defects: none found — probed: prerelease-style versions in extract (word
  boundary holds), CHANGELOG with the version mentioned in prose only (heading
  regex ignores it)
TEST VERDICT: pass
