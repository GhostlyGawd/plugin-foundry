---
name: community-voting
title: Community Voting
category: growth
stage: published
kind: feature
version: null
components: [template, workflow, site]
one_liner: Free plugin suggestions via GitHub issues, prioritized by 👍 reactions, surfaced live on the window.
tags: [voting, community, ladder]
created: 2026-07-04
updated: 2026-07-04
---

# Community Voting

Visitors need a lever between lurking and paying. GitHub already has one: issues and
reactions. This feature wires it end to end — suggest free, vote with 👍, watch the
loop formalize the winners.

## Pitch
- **Job:** a zero-cost participation rung on the engagement ladder
  (visitor → **voter → suggester** → patron).
- **User:** anyone who wants a plugin but not enough to pay for priority.
- **Components:** `idea` issue template; metrics.py reads 👍 counts into
  foundry/votes.json each shift; the window renders a Vote lane with live counts and
  one-tap links; the Ideator/growth roles read votes when formalizing.
- **Why native GitHub:** votes are public, un-fakeable by us, spam-resistant
  (GitHub accounts), and free — the honest substrate the dark-pattern law demands.

## Spec
- `.github/ISSUE_TEMPLATE/idea.yml`: one required textarea, label `idea`, copy that
  explains votes vs. paid commissions.
- `tools/metrics.py`: open `idea` issues → `{number: {title, votes, url}}` sorted by
  votes desc → `foundry/votes.json`; totals into the METRICS ledger.
- Site: `#vote` section listing top open ideas with counts, "vote →" links to the
  issue, and a "Suggest an idea — free" button to the template; roadmap copy states
  the rule: votes order the pool, commissions skip the queue.
### Acceptance checks
1. votes.json with seeded fixture data renders a correctly ordered Vote lane.
2. Empty votes.json renders the suggest CTA with an honest "no open ideas yet" state.
3. No vote count appears anywhere the repo can't substantiate (dark-pattern law).

## Experiment
- **Hypothesis:** giving a free lever converts passive visitors into participants —
  within the review window, ≥5 distinct idea issues or ≥15 total 👍 votes appear.
- **Metric:** `open_ideas` and `idea_votes_total` in state/METRICS.jsonl.
- **Baseline:** 0 / 0 (genesis).
- **Review-after:** 14 days after the site's first public deploy (growth role: P1
  when overdue).

## Build log
- i0: template, metrics votes pipeline, Vote lane, suggest CTA — shipped at genesis.

## Test log
### Test pass — i0
- tier 1: pass — validate.py + build.py green; template YAML parses
- tier 2: unavailable — no live repo at genesis; fixture votes.json exercised the lane
- tier 3: checks 1–3 run against fixtures → ordered lane, honest empty state, no
  unsubstantiated numbers found
- defects: none found — probed: empty file, missing file, tie votes, 100-issue fixture
TEST VERDICT: pass

## Review log
REVIEW: approved — genesis self-review; the P0-on-keep-streak tripwire and the open
experiment supersede this the moment real data lands.
Published i0. Verdict pending experiment review.
