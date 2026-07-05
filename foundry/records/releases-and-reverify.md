---
name: releases-and-reverify
title: Releases & Weekly Re-verification
category: workflow
stage: spec
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
