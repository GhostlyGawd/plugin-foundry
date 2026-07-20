---
name: field-reports
title: Field Reports
category: growth
stage: published
kind: feature
version: null
verified: 2026-07-20
components: [template, site]
one_liner: Real user experiences with shipped plugins, surfaced on their birth certificates.
tags: [social-proof, community, trust]
created: 2026-07-05
updated: 2026-07-06
---

# Field Reports

Qualitative, attributed, un-gameable social proof — the opposite of star ratings.

## Pitch
- **Job:** let installers hear from the field before installing.
- **User:** installers; reporters who want their experience to count.
- **Components:** field-report issue template; metrics.py collects them into
  foundry/reports.json; provenance pages list titles + links (UNTRUSTED bodies stay
  on GitHub per SECURITY.md).

## Spec
- Pages render report title, author, link — never the body inline.
- Reports on a plugin appear on its certificate under "From the field".
### Acceptance checks
1. Fixture reports.json renders titled links on the right certificate.
2. Plugins with none render nothing (no empty-state begging).
3. No report body text is ever inlined into the window.

## Experiment
- **Hypothesis:** field-visible plugins convert better — clones ratio rises for
  reported plugins vs. unreported over the window.
- **Metric:** `field_reports` count + `clones_14d` in METRICS.jsonl.
- **Baseline:** 0 reports (genesis).
- **Review-after:** 30 days post-deploy.

## Build log
- i0(v5): template + collection pipeline landed; certificate rendering is the
  remaining build step (QA pass follows).

## Test log
### Test pass — i3
- tier 1: pass — validate/build green with fixture and after restore
- tier 2: n/a (site feature)
- tier 3: fixture reports.json (2 reports) → "From the field" rendered on
  plugin-smith certificate with titles+authors+links only (no bodies inlined);
  fork-a-foundry certificate untouched; empty-state restore renders nothing
- defects: none found — probed: report on unknown plugin key (ignored cleanly)
TEST VERDICT: pass

## Review log
### Review — i125
- SECURITY posture is the feature: titles/authors/links only, bodies stay on
  GitHub — re-read the render path, nothing inlines report prose. Empty state
  renders nothing (no begging). Unknown-plugin keys ignored (QA probed).
- Cap check ([:8] per certificate): unlike the shipnote's week-one cap (i109
  bounce), this cannot fire until one plugin accumulates 9 reports — today the
  file is `{}`. Nit filed with the saga nit class, not a bounce: add an
  "all N reports →" label-search link when the cap engages.
- Suite gap noted (manual fixture QA at i3, no executable suite) — carried to the
  closing audit with the systemic v5/v7 pattern, consistent with saga-page (i107).
- Axes: scope 5 · prompt n/a · thrift 5 · hook-safety n/a · docs-truth 5 ·
  structure 5.
REVIEW: approved — un-gameable social proof, honestly empty until the field speaks.

### Published — i126 (maintainer)
Live: certificates carry "From the field" when reports exist, "file a field
report" link always. Experiment armed — review 30 days post-deploy.

### Test pass — i147 (suite backfill, audit-003 #3)
- executable suite landed: fixture report renders title/author/link on the right
  certificate; hostile body (script tag + injection text) NEVER reaches the
  window; unreported plugins render nothing; fixture restored + rebuilt in a
  finally block so the suite can't dirty the site
TEST VERDICT: pass
