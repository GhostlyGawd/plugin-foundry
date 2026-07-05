---
name: trust-card
title: Trust Card
category: quality
stage: building
kind: feature
version: null
components: [site]
one_liner: A machine-generated footprint block on every plugin certificate - hooks, network, cost, uninstall.
tags: [trust, footprint, certificates]
created: 2026-07-05
updated: 2026-07-05
---

## Pitch
Buyers of automation deserve the blast radius in writing. Everything on the card
derives from the artifact itself, so it cannot drift from the truth.

## Spec
- Certificate block "Trust card": components (from record), hook surface (parsed
  from the plugin hooks.json: event + matcher, or "none"), network heuristic
  (scan plugin files for curl/wget/fetch(/http - report "none detected" or list),
  always-on cost (existing stamp), uninstall line ("/plugin uninstall <name> -
  leaves nothing behind" when no state files are written, else says what).
- Derivation only - no hand-written trust claims allowed inside the block.

## Experiment
- Hypothesis: certificates answer safety questions before they are asked; proxy - fewer is-it-safe issues, field reports cite the card
- Metric: question-labeled issues about safety per month; Baseline: 0; Review-after: 2026-09-05

### Acceptance checks
1. commit-craft card shows "PreToolUse - matcher: Bash"; skills-only plugins show hooks: none.
2. Network heuristic flags a fixture file containing curl, and clears on removal.
3. Block renders only for kind: plugin.

## Build log
- i41: trust_card() derives components, hook surface (parsed hooks.json), network
  heuristic over executable surfaces (labeled as heuristic), always-on cost, and
  the uninstall line; renders only for kind: plugin; block placed above the record
  sections; suite added.
