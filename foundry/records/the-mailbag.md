---
name: the-mailbag
title: The Mailbag
category: growth
stage: published
kind: feature
version: null
verified: 2026-07-06
components: [workflow,docs,template]
one_liner: question-labeled issues get answered inside Monday shipnotes - office hours, kept by a machine.
tags: [shipnotes, questions, community]
created: 2026-07-05
updated: 2026-07-05
---

## Pitch
Every unanswered question is churn. Fold answers into the artifact people already
read: the Monday shipnote.

## Spec
- shipnote.py: fetch open issues labeled question (gh api; absent - skip with a
  logged line); render a Mailbag section - question title + link + the answer.
- Answer authorship is a LOOP duty: the growth shift drafts answers from repo
  evidence before shipnote assembly; unanswered stay listed as "on the desk".
- Issue template question.yml added; CONTRIBUTING points at it.

## Experiment
- Hypothesis: questions get asked because they get answered: at least 3 question issues in the first 60 days, all answered by the next shipnote
- Metric: question issues opened + answered-by-next-shipnote rate; Baseline: 0; Review-after: 2026-09-15

### Acceptance checks
1. shipnote dry-run without gh prints the skip line and still builds.
2. Mailbag section renders only when question issues exist.
3. question.yml lints; CONTRIBUTING links it.

## Build log
- i75: shipnote gains a Mailbag section (gh-gated, fail-open with a stderr skip
  line so the note always builds); question.yml template; CONTRIBUTING gains
  Lane 0 — Ask; GROWTH carries the evidence-only answering duty. Suite added.

## Test log
### Test pass — i76
- tier 1: pass
- tier 3: suite 4/4 — live PATH-stripped dry-run proved the fail-open skip (note
  builds, stderr says why); question.yml yaml-lints; Lane 0 routed; duty on the
  books; also verified the Mailbag renders nothing when zero questions exist
  (empty-renders-nothing holds even inside a text artifact)
- defects: none found — probed: malformed gh JSON (caught, treated as zero
  questions), label with no open issues (silent)
TEST VERDICT: pass

## Publish log
- i78 (maintainer): mechanism live in the Monday shipnote pipeline; first Mailbag
  renders with the first question; experiment armed (asked+answered rate, review
  2026-09-15).

## Review log
### Review — i77 (reviewer)
- Evidence-only answering is the load-bearing clause; a mailbag that speculates
  would launder guesses through the shipnote's credibility. GROWTH says the quiet
  part: unanswerable-yet is an allowed answer.
- Fail-open with a stderr note is exactly right for a garnish feature — the
  shipnote's core cargo never waits on gh.
- Sharpest question: who audits the answers? The same thread they land in —
  in-thread answers are publicly falsifiable next to the question, unlike a
  private FAQ.
REVIEW: approved
