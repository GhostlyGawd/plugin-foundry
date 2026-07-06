---
name: starter-kits
title: Starter Kits
category: growth
stage: building
kind: feature
version: null
components: [site, docs]
one_liner: Curated bundles with one copy-block — cut choice paralysis for first-time installers.
tags: [onboarding, curation, installs]
created: 2026-07-05
updated: 2026-07-06
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

## Review log
### Review — i89
- renderKits logic honest: only published members emit install lines; pending
  members named with stage ("finishing on the line"); validator law (check_kits)
  fails unknown members — acceptance checks 1–2 hold as built.
- Escaping audited: name/desc/title/stage all pass through esc(). Good.
- DEFECT (docs truth / the feature's one job): kit copy-blocks join commands with
  '\n', but `.install` CSS says `white-space:nowrap` — a 2-plugin kit renders and
  *pastes* as a single line: `/plugin install a@foundry /plugin install b@foundry`,
  which is not runnable as pasted. Acceptance check 3 passes only for 1-plugin
  kits; both live kits have 2 members. Fix: kit-scoped `white-space:pre` (or
  per-line divs) so each command pastes on its own line.
- Axes: scope 5 · prompt n/a (site feature) · thrift 5 · hook-safety n/a ·
  docs-truth 3 · structure 5.
REVIEW: bounced — multi-line kit copy-block collapses to one unrunnable line
(white-space:nowrap); fix and re-run check 3 with a 2-member kit before rc.
