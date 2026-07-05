---
name: live-shift-theater
title: Live Shift Theater
category: growth
stage: building
kind: feature
version: null
components: [site]
one_liner: A window page that replays the latest shift's journal as a slow-scrolling theater — watch the machine work.
tags: [spectator, window, delight]
created: 2026-07-05
updated: 2026-07-05
---

## Pitch
The ON AIR light says "something is happening"; theater would show *what*. The
journal is already the script — render the latest entries as a timed replay.
Spectators became prospectors once; give them a show.

## Spec
- build exports the last 12 journal entries (i, role, ts, did) into data.json;
  site/theater.html replays them typewriter-style, newest last, ON AIR chip shared
  with the window; prefers-reduced-motion renders instantly, no animation.
- Zero invention: entries come from JOURNAL verbatim; empty journal - curtain line.
- Nav gains Theater.

## Experiment
- Hypothesis: theater becomes the second-most-visited page after the shelf.
- Metric: traffic uniques on theater path; Baseline: 0; Review-after: 2026-09-15.

### Acceptance checks
1. Rendered entries match the JOURNAL tail exactly (count + text).
2. Reduced-motion shows the full script instantly.
3. Empty journal renders the curtain line, nothing invented.

## Build log
- i53: data.json exports the 12-entry journal tail (oldest-first for playback);
  theater.html replays verbatim with a typewriter cursor, instant under
  reduced-motion, curtain line when the ledger is empty; jump nav gains Theater.
  Suite added (verbatim-match, reduce path, curtain, nav).
