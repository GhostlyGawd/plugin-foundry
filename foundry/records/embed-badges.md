---
name: embed-badges
title: Embeds & Badges
category: growth
stage: rc
kind: feature
version: null
components: [site, docs]
one_liner: A shields-style status badge and an embeddable ticker — put the living machine on your own site.
tags: [distribution, virality]
created: 2026-07-05
updated: 2026-07-05
---

# Embeds & Badges

Fans are distribution. Give them something true to embed.

## Pitch
- **Job:** let anyone display the workshop's live state elsewhere, honestly.
- **User:** bloggers, README authors, forkers pointing home.
- **Components:** site/badge.json (shields.io endpoint schema: shipped count +
  iteration), site/embed.html (ticker-only page sized for iframes), README snippet.

## Spec
- Badge message derives from data at build time; embed page reuses the real ticker
  and nothing else; both regenerate on every deploy like the window.
### Acceptance checks
1. badge.json validates against the shields endpoint schema fields.
2. embed.html renders the ticker standalone at 320px width.
3. Snippet in README works as pasted once pages_url is set.

## Experiment
- **Hypothesis:** embeds drive referral visits — `views_14d` and stars rise after
  the first external embed appears.
- **Metric:** `views_14d`, `stars` in METRICS.jsonl.
- **Baseline:** from first real snapshot.
- **Review-after:** 30 days post-deploy.

## Build log
- i0(v5): badge.json + embed.html generators landed with the v5 window.
- i6: README snippet block (badge endpoint + iframe embed) — build complete.

## Test log
### Test pass — i7
- tier 1: pass
- tier 2: n/a (site feature)
- tier 3: badge.json validates against the shields endpoint schema (schemaVersion/
  label/message/color) and carries the post-ceremony name; embed.html is script-free
  static HTML with the real reel and a viewport meta (iframe-safe at narrow widths);
  README snippet present and derivable once pages_url is set
- defects: none found — probed: badge label pre/post naming (reads STATE, not a constant)
TEST VERDICT: pass
