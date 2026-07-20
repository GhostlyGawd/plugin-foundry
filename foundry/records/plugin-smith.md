---
name: plugin-smith
title: Plugin Smith
category: meta
stage: published
version: 0.1.4
components: [skills]
always_on_tokens: 137
verified: 2026-07-20
one_liner: Scaffolds portable coding-agent plugins and audits their host-native packages.
tags: [meta, scaffolding, validation, dogfood]
created: 2026-07-04
updated: 2026-07-17
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
- skills/scaffold/SKILL.md — creates shared behavior and separate native packages
  for Claude Code, Codex, Gemini CLI, Cursor, and GitHub Copilot.
- skills/doctor/SKILL.md — detects target hosts, audits their schemas and root
  variables, and blocks cross-host hook collisions or undocumented risky behavior.
- No hooks, no MCP. Token budget: ≤150 always-on.
### Acceptance checks
1. Invoking scaffold with a name + component list yields one shared component tree
   and a native manifest/package plan for each requested host.
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
- v13 A4+B8: v0.1.3 — sharpened the `doctor` skill description with concrete
  trigger phrases (it failed the very "couldn't tell Claude *when* to fire" bar
  it enforces); normalized author to "Nightshift Foundry" to match the shelf.
  Tag plugin-smith-v0.1.3.
