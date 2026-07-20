---
name: scannable-window
title: Scannable Window
category: growth
stage: published
kind: feature
version: null
verified: 2026-07-20
components: [site]
one_liner: A cross-host storefront with native downloads, responsive install guidance, and a shelf readable in one sweep.
tags: [ui, scannability, ia, compatibility, downloads]
created: 2026-07-04
updated: 2026-07-17
---

# Scannable Window

A spectacle nobody can parse is a wall. This pass makes the page legible in one
sweep: where am I, what's alive, what shipped, where do I act.

## Pitch
- **Job:** cut time-to-comprehension for a first-time visitor to seconds.
- **User:** everyone who lands cold from a link.
- **Components:** sticky jump-nav (Shelf · Roadmap · Vote · Commission); a stats
  strip of substantiated numbers (shipped, on the line, community votes, stars);
  section rules with anchor targets; vote badges where relevant.
- **Why now:** the window gained sections (roadmap, request box, vote lane) faster
  than its navigation did.

## Spec
- Nav: anchor links under the strap; sticky on scroll; keyboard-focusable.
- Stats strip: four numbers max, each traceable to data.json (never decorative).
- Reduced-motion and small-screen behavior preserved; no new animation.
- Host picker: one keyboard-readable choice updates guides, cards, kits, and
  deterministic native ZIP links for Codex, Claude Code, Gemini CLI, Cursor,
  and GitHub Copilot.
- Privacy: host choice is in-memory only; no analytics, cookies, storage,
  remote fonts, or third-party scripts.
### Acceptance checks
1. Every nav target scrolls to a labeled section; focus outlines visible.
2. Each stat renders from data.json and shows "—" when its instrument is null.
3. Page remains single-request static + data.json heartbeat; no new dependencies.

## Experiment
- **Hypothesis:** legibility lifts the ladder's first rung — 14-day repo `uniques`
  and returning traffic rise vs. baseline once instruments come online; qualitative
  bar: the Vote/Commission sections receive their first organic use.
- **Metric:** `views_14d`, `uniques_14d` in METRICS.jsonl; first idea/commission
  issue arrivals.
- **Baseline:** unknown — first measurement (nulls until instruments come online).
- **Review-after:** 14 days after first public deploy.

## Build log
- i0: nav, stats strip, anchors, vote badges — shipped at genesis with community-voting.
- 2026-07-17: rewrote the Claude-only journey as a five-host storefront;
  added digest-indexed downloads and responsive host-native install guidance.

## Test log
### Test pass — i0
- tier 1: pass — build.py green; no leftover template tokens
- tier 2: unavailable — verified rendering from file:// with embedded DATA
- tier 3: checks 1–3 → anchors land, null-stat renders "—", no new deps
- defects: none found — probed: reduced-motion path, 360px viewport, empty lanes
TEST VERDICT: pass

## Review log
REVIEW: approved — genesis self-review; bundled ship with community-voting noted
(GROWTH.md one-variable rule): each experiment names its own metric to stay separable.
Published i0. Verdict pending experiment review.

### Test pass — 2026-07-17
- tier 1: pass — generator and storefront JavaScript parse green
- tier 2: pass — desktop and 390px browser checks; no horizontal overflow
- tier 3: pass — five host controls, 50 package links, storage-free selection,
  search/filter behavior, and mobile anchors verified
- defects: one Windows-path escape and one sticky-header anchor offset found and fixed
TEST VERDICT: pass
