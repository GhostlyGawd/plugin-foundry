---
name: verified-by-foundry
title: Verified by the Foundry
category: growth
stage: published
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

## Test log
### Test pass — i171 (qa)
- tier 1: validate + build green; suite executable.
- tier 3: acceptance checks 1–4 as an executable suite (12 checks): shelf 8/8
  DOCTOR: OK; hostile fixture names all seven laws individually; action.yml
  proven composite with doctor reference and plugin-dir default (yaml check
  self-skips where pyyaml is absent and runs in CI); registry proven empty→
  nothing and fixture-entry→window-data, section ships hidden.
- defects: none found — probed: doctor against a plugin dir with no manifest
  (fails with the manifest law, not a traceback); action path traversal
  (github.action_path/../../../tools/doctor.py resolves inside the action
  checkout by construction).
TEST VERDICT: pass

## Review log
### Review — i172 (reviewer)
- The doctor's teeth are real: every law it enforces is the same table
  validate.py enforces on this shelf (single import, no copy), and the suite
  asserts each violation is NAMED — a diagnosis, not a verdict.
- Registry law holds structurally: entries are maintainer-curated JSON, the
  section renders nothing while empty, and the inline _law note travels with
  the file.
- **Required before approval (applied and verified in-pass):** a "verified"
  badge for a trust product must state its limits or it lies by implication.
  The doctor proves structure, not intent — a spec-perfect plugin can still
  carry a hostile skill body. Honest-limits copy now on all three surfaces:
  README ("a floor, not a guarantee"), window section footer, action
  description ("Proves structure, not intent"). Runner python3 requirement
  documented in the action header.
- Sharpest question: does listing external repos on the window endorse them?
  No — the entry states exactly what happened (doctor green, date, public run
  link) and now states what that does NOT mean, in the same breath.
REVIEW: approved

## Publish log
- i173 (maintainer): published — the action is live at
  GhostlyGawd/plugin-foundry/.github/actions/foundry-doctor@main the moment
  this lands on main; README paste-block is the storefront; registry opens
  empty by law. Experiment armed (registry entries + views_14d, review
  2026-09-06). kind:feature — no marketplace entry, no version tag.

## Maintenance log
- i211 (builder, v12 4.2): verified listings now mint embeddable SVG badges
  ("verified by the foundry | doctor green · <date>", honest-limits in the
  tooltip), regenerated from scratch each build so a delisted repo's badge
  dies with its listing; paste-ready markdown rendered beside each entry on
  the window. Suite +2 checks (empty→none; fixture→SVG with date + limits).
