---
name: starter-kits
title: Starter Kits
category: growth
stage: rc
kind: feature
version: null
components: [site, docs]
one_liner: Curated bundles with one copy-block — cut choice paralysis for first-time installers.
tags: [onboarding, curation, installs]
created: 2026-07-05
updated: 2026-07-05
---

# Starter Kits

A shelf answers "what exists"; a kit answers "where do I start."

## Pitch
- **Job:** first useful install in under a minute.
- **User:** first-time installers.
- **Components:** foundry/kits.json (Maintainer-curated), Kits section on the
  window with one copyable block per kit; validator keeps kit names honest.

## Spec
- Only published plugins render install lines; unpublished members show as
  "finishing on the line" — kits never oversell.
- Kits stay small (2–4 plugins); Maintainer curates via normal iterations.
### Acceptance checks
1. Kit with mixed-stage members renders installable lines + honest pending note.
2. Validator fails on a kit referencing a nonexistent record.
3. Copy-block contains only real `/plugin install` lines.

## Experiment
- **Hypothesis:** kits lift installs-per-visitor — `clones_14d`/`uniques_14d` ratio
  rises after ship.
- **Metric:** `clones_14d`, `uniques_14d` in METRICS.jsonl.
- **Baseline:** from first real snapshot.
- **Review-after:** 21 days post-deploy.

## Build log
- i0(v5): kits.json seeded (plugin-maker kit), window section, validator law.

## Test log
### Test pass — i0(v5)
- tier 1: pass — validator negative test on an unknown kit member fails as designed
- tier 2: n/a (site feature)
- tier 3: checks 1–3 → mixed-stage kit renders one install line + one pending note;
  copy-block audited
- defects: none found — probed: empty kits array, kit of only-unpublished members
TEST VERDICT: pass
