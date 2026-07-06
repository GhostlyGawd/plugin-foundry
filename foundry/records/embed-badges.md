---
name: embed-badges
title: Embeds & Badges
category: growth
stage: building
kind: feature
version: null
components: [site, docs]
one_liner: A shields-style status badge and an embeddable ticker — put the living machine on your own site.
tags: [distribution, virality]
created: 2026-07-05
updated: 2026-07-06
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

## Review log
### Review — i114
- badge.json: real values at build time (25 shipped · i113), shields endpoint
  fields exact, post-ceremony label from STATE. Good.
- embed.html: script-free, real reel only, reduced-motion honored, escapes
  audited, pages_url baked from config. Good.
- DEFECT (docs truth, check 3): README's snippet still prints literal
  `<pages_url>` placeholders — but pages_url IS set now (site-config filled at
  go-live prep, i-ops). "Works as pasted" is the acceptance check and it fails
  today: a visitor pasting the badge line gets a 404 to the literal string. The
  i7 test predates the config landing; the world moved, the doc didn't.
- Axes: scope 5 · prompt n/a · thrift 5 · hook-safety n/a · docs-truth 3 ·
  structure 5.
REVIEW: bounced — bake the real pages_url into the README snippet (and prefer
deriving it from site-config so it can't drift again).
