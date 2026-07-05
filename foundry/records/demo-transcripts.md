---
name: demo-transcripts
title: Demo Transcripts
category: quality
stage: spec
kind: feature
version: null
components: [site,docs]
one_liner: Certificates show the plugin working - a terminal-styled example session, honestly labeled until CI records the real thing.
tags: [demos, certificates, show-dont-tell]
created: 2026-07-05
updated: 2026-07-05
---

## Pitch
Install decisions want evidence, not adjectives. The record gains an optional
Example session that renders as a terminal on the certificate.

## Spec
- SCHEMA: optional record section "## Example session" - fenced transcript.
- Certificate renders it terminal-styled, open by default, with the honest label
  "authored example - a CI-recorded transcript replaces this" until QA swaps in a
  recorded one (TESTING gains the recording duty for CI shifts).
- Ship authored examples for all six published plugins now.

## Experiment
- Hypothesis: certificates with sessions convert lookers to installers better; proxy - field reports reference the examples
- Metric: field reports mentioning the example per quarter; Baseline: 0; Review-after: 2026-10-05

### Acceptance checks
1. All six published plugin certificates render a terminal block with the label.
2. Records without the section render nothing extra.
3. TESTING documents the CI recording duty.
