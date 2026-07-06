---
name: verified-by-foundry
title: Verified by the Foundry
category: growth
stage: idea
version: null
kind: feature
components: [workflow, site, docs]
one_liner: The foundry's verification machinery pointed outward - any Claude Code plugin repo can run the doctor in CI and earn a listed, dated badge.
tags: [trust, ecosystem, verification]
created: 2026-07-06
updated: 2026-07-06
---

# Verified by the Foundry

The foundry already owns the only verification machinery in the Claude Code
plugin ecosystem: structural laws hard-coded from the official spec
(tools/validate.py), weekly re-verification (ADR-013), token-cost measurement,
a shields endpoint. All of it points inward at 8 plugins.

## Pitch
- **Job:** let any third-party plugin repo prove — continuously, in its own CI —
  that its plugin passes the same structural laws the foundry holds itself to,
  and show for it a badge that a stranger can trust.
- **User:** plugin authors who want a credibility signal; installers deciding
  whether a random plugin repo is safe to add.
- **Components:** a standalone `tools/doctor.py` (single-plugin structural
  checker, no foundry-repo assumptions), a composite GitHub Action
  (`.github/actions/foundry-doctor/`) any repo can `uses:`, a
  `foundry/verified.json` registry (renders nothing until it has a first name,
  hall law), and a window section listing verified externals with dates.
- **Why the foundry and no one else:** the laws are already written, tested
  (foundry/tests/_tools/), and enforced in anger on a real shelf. Competitors
  would have to adopt the whole law book to copy the badge.
