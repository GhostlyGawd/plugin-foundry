---
name: verified-by-foundry
title: Verified by the Foundry
category: growth
stage: building
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

## Spec
- `tools/doctor.py <plugin-dir>`: standalone structural checker for ONE plugin
  directory, importable nowhere-else assumptions (no records, no marketplace):
  manifest exists/parses, kebab-case name, semver version (if present), only
  plugin.json inside .claude-plugin/, `./`-relative manifest paths, skill/
  command/agent frontmatter completeness, hook events/types against the
  verified spec tables (imported from validate.py — one law book), no `.*`
  matchers, quoted `"${CLAUDE_PLUGIN_ROOT}"`, executable scripts with shebangs.
  Exit 0 with "DOCTOR: OK" or exit 1 listing every violation. Stdlib only.
- `.github/actions/foundry-doctor/action.yml`: composite Action; input
  `plugin-dir` (default `.`); runs the doctor from the checked-out action repo
  against the caller's checkout. README section documents one paste-block:
  `uses: GhostlyGawd/plugin-foundry/.github/actions/foundry-doctor@main`.
- `foundry/verified.json`: registry of externally verified repos
  (`{"repo", "plugin_dir", "verified", "run_url"}`); entries added by the
  maintainer from a passing public Actions run link (substantiated-numbers law:
  no run link, no entry). Renders nothing until it has a first name.
- Window: "Verified externals" section on the index, only when registry is
  non-empty; each entry shows repo, date, and links to the run.

### Acceptance checks
1. doctor.py passes every shipped plugin on this shelf (8/8 OK).
2. doctor.py fails a broken fixture with the specific law named (bad hook
   event, `.*` matcher, unquoted root, lost exec bit — each detected).
3. action.yml is valid YAML, composite, references the doctor relative to the
   action path, and defaults plugin-dir to `.`.
4. verified.json with zero entries renders no window section; with a fixture
   entry, the section appears with repo + date + run link.

## Experiment
- **Hypothesis:** outward verification becomes the foundry's top referral
  source — external repos carrying the badge/action link back, measurable as
  `views_14d` referrers and registry growth.
- **Metric:** entries in foundry/verified.json; `views_14d` in METRICS.jsonl.
- **Baseline:** 0 external repos; views null until the window is live.
- **Review-after:** 2026-09-06 (60 days — outward adoption is slow).

## Build log
- i170: tools/doctor.py (standalone one-plugin checker, law tables imported
  from validate.py), .github/actions/foundry-doctor/action.yml (composite,
  plugin-dir input, runs the doctor from the action checkout),
  foundry/verified.json (empty registry + law note), window "Verified
  externals" section (hall law: hidden while empty), README paste-block.
  Live probes: 8/8 shelf plugins DOCTOR: OK; 8-violation fixture named every
  law; registry plumbing verified empty and with a fixture entry. Build
  complete — all spec components exist.
