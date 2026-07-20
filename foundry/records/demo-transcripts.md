---
name: demo-transcripts
title: Demo Transcripts
category: quality
stage: published
kind: feature
version: null
verified: 2026-07-20
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

## Build log
- i49: Example session renders terminal-styled + open with the honesty label;
  SCHEMA documents the section; TESTING gains the CI recording duty (recordings
  replace authored examples, dated); six authored sessions placed — each shows
  only behavior the plugin actually has (consent gates, honest test notes, the
  guard explaining itself). Suite added.

## Test log
### Test pass — i50
- tier 1: pass
- tier 3: suite 2/2 (all six plugin certificates render labeled terminals;
  section-less records render nothing extra); content audit — each transcript
  cross-read against its skill: env-doctor demo shows the consent gate, pr-narrator
  demo shows the honest test-notes clause and the gh y/N prompt, commit-craft demo
  invites the user to trigger the guard; no demo claims an ability the skill lacks
- defects: none found — probed: HTML-escaping of transcript angle brackets (safe)
TEST VERDICT: pass

## Publish log
- i52 (maintainer): sessions live on all plugin certificates; experiment armed
  (field reports referencing examples, review 2026-10-05).

## Review log
### Review — i51 (reviewer)
- The honesty label does double duty: it protects readers today and creates the
  CI obligation that upgrades it tomorrow — a promise with a deadline attached.
- The demos teach the *limits* as much as the features (consent gates, "none" as
  a valid test note); that is exactly the shelf's voice.
- Sharpest question: will an authored demo ever be mistaken for a recording? Not
  while the uppercase label sits between the summary and the terminal — and the
  TESTING duty gives every future recording a date.
REVIEW: approved
