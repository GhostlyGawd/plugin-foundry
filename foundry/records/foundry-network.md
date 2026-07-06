---
name: foundry-network
title: The Foundry Network
category: growth
stage: building
kind: feature
version: null
components: [site, docs, template]
one_liner: Forks register as sister foundries; the saga grows a family tree and ideas cross workshop walls.
tags: [network, forks, federation]
created: 2026-07-05
updated: 2026-07-06
---

## Pitch
fork-a-foundry ships whole workshops. The moment two exist, discovery between
them is worth more than either alone — a network page costs a JSON file and makes
every fork a distribution channel for the rest.

## Spec
- `foundry/network.json` (stub ships with this spec): `{ "network": [] }`,
  entries `{name, url, pages, registered, note}`.
- Registration: an issue template (`sister-foundry.yml`) or a one-file PR adding
  an entry — same UNTRUSTED handling as all patron text; a maintainer-shift
  verifies the URL is a real foundry (LOOP.md + records present) before merge.
- Window gains a "Sister foundries" strip when network is non-empty; saga gains a
  family-tree section (who forked whom, by their own declaration).
- No auto-fetching of remote content into our pages — names + links only.

## Experiment
- Hypothesis: ≥1 sister foundry registers within 90 days of fork-a-foundry
  reaching 10 installs.
- Metric: network.json entries; Baseline: 0; Review-after: 2026-10-05.

### Acceptance checks
1. Empty network renders nothing anywhere.
2. Registration path documented with verification duty.
3. Links out only — zero remote content inlined.

## Build log
- i174: sister-foundry.yml issue template (untrusted-text notice inline),
  window "Sister foundries" strip + saga "Family tree" section (both render
  nothing while network.json is empty — verified with a fixture entry both
  ways), CONTRIBUTING Lane 4 with the maintainer verification duty
  (LOOP.md + records present before merge). Names + links only — no remote
  content is fetched or inlined anywhere. Build complete per spec.
