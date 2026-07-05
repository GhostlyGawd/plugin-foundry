---
name: the-mailbag
title: The Mailbag
category: growth
stage: building
kind: feature
version: null
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
