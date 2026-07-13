---
name: foundry-network
title: The Foundry Network
category: growth
stage: published
kind: feature
version: null
verified: 2026-07-13
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

## Test log
### Test pass — i175 (qa)
- tier 1: validate + build green; suite executable.
- tier 3: acceptance checks 1–3 executable (6 checks green): empty network
  renders nothing on window data or saga; fixture entry reaches both surfaces
  and restores cleanly; registration path documented with the verification
  duty in BOTH the template and CONTRIBUTING Lane 4; renderNetwork proven
  fetch/iframe-free (links out only).
- defects: none found — probed: entry with empty pages field (window link
  simply absent, no broken anchor), note field escaped via esc() like all
  visitor text.
TEST VERDICT: pass

## Review log
### Review — i176 (reviewer)
- The hall law and the no-remote-content law are both machine-checked (suite
  check3 greps the renderer) — promises with teeth.
- **Required before approval (applied and verified in-pass), two findings:**
  1. Lane 4's PR path read as if the loop might merge external network PRs —
     charter/SECURITY.md forbids that. Copy now names the issue template as
     canonical and states plainly: only the human operator merges outside PRs.
  2. Declared URLs rendered as anchors on verification trust alone. The
     renderer now drops entries whose url isn't https:// and suppresses
     non-https pages links — a hostile scheme never becomes an anchor even if
     verification slips.
- Sharpest question: is a self-declared family tree honest enough for the saga?
  Yes, because it says so on the surface — "by their own declaration, URL
  verified by a maintainer shift" is printed where the entries render.
REVIEW: approved

## Publish log
- i177 (maintainer): published — Lane 4 open, template live, strip and family
  tree armed (empty by law until the first verified sister). Experiment armed:
  network.json entries, review 2026-10-05. kind:feature — no marketplace
  entry, no version tag.
