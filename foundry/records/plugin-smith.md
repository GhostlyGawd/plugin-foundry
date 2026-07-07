---
name: plugin-smith
title: Plugin Smith
category: meta
stage: published
version: 0.1.2
components: [skills]
always_on_tokens: 113
verified: 2026-07-06
one_liner: Scaffolds new Claude Code plugins and health-checks existing ones against the official spec.
tags: [meta, scaffolding, validation, dogfood]
created: 2026-07-04
updated: 2026-07-06
---

# Plugin Smith

The workshop's own first tool: two skills that encode the official plugin layout and
this foundry's quality bar, so every future build starts correct instead of getting
corrected.

## Pitch
- **Job:** make "start a plugin right" and "check a plugin honestly" one invocation each.
- **User:** this loop's builder role, and any human developing plugins in this repo.
- **Components:** two skills — `scaffold` (generate a correct skeleton) and `doctor`
  (audit an existing plugin directory).
- **Why a plugin:** it's the dogfood cornerstone — the factory should run on its own
  products, and this knowledge must be versioned, not tribal.

## Spec
- Name: `plugin-smith` (forever).
- skills/scaffold/SKILL.md — description (verbatim): "Scaffold a new Claude Code
  plugin directory with the official layout. Use when creating a new plugin, starting
  a plugin skeleton, or converting loose commands into a plugin."
- skills/doctor/SKILL.md — description (verbatim): "Audit a Claude Code plugin
  directory against the official schema and this marketplace's quality bar. Use when
  reviewing, debugging, or health-checking a plugin."
- No hooks, no MCP. Token budget: ≤150 always-on.
### Acceptance checks
1. Invoking scaffold with a name + component list yields a tree matching the official
   layout (manifest in .claude-plugin/, components at root, ./-relative paths).
2. Doctor on a plugin with a seeded flaw (e.g. command file missing description, or
   agents/ inside .claude-plugin/) reports each flaw with the fix.
3. Doctor on plugin-smith itself reports clean.

## Build log
- i0: both skills, manifest, README, CHANGELOG written at genesis.

## Test log
- i0: genesis exception — shipped without a full TESTING.md pass; structural tier
  green via tools/validate.py + smoke.sh. Post-publish re-test is P1 in BACKLOG.
TEST VERDICT: pass (structural only — see backlog P1 for the honest re-test)

## Recipes
- "scaffold a plugin called changelog-bot with one skill" → full lawful skeleton
- "doctor my plugin at ./plugins/foo" → structure + manifest + quoting findings
- pair with fork-a-foundry: smith the plugin, then give it a workshop

## Example session
you> scaffold a plugin called changelog-bot with one skill
smith> reading the official plugin docs first (docs-before-invention)...
smith> created plugins/changelog-bot/.claude-plugin/plugin.json
smith> created skills/changelog/SKILL.md — description carries a "Use when" contract
smith> created README.md, CHANGELOG.md
smith> run `claude plugin validate ./plugins/changelog-bot --strict` to confirm

## Review log
REVIEW: approved — genesis self-review; axes: scope 5, prompt 4, thrift 5, hooks n/a,
docs 4, structure 5. The P1 re-test supersedes this the moment it runs.
Published i0 at 0.1.0 — marketplace entry source ./plugins/plugin-smith.
- i182 (maintainer, v11 #2): v0.1.2 — README Manage section (docs sweep). Tag plugin-smith-v0.1.2.
