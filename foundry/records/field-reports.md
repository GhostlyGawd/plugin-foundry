---
name: field-reports
title: Field Reports
category: growth
stage: building
kind: feature
version: null
components: [template, site]
one_liner: Real user experiences with shipped plugins, surfaced on their birth certificates.
tags: [social-proof, community, trust]
created: 2026-07-05
updated: 2026-07-05
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
