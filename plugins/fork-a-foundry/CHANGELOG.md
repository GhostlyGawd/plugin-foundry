# Changelog

## 0.2.2 — 2026-07-17
- fix: new foundries now provision a project-scoped `OPENAI_API_KEY`, validate one
  PR-only Codex shift, and remove `STOP` through review; the retired hosted Claude
  OAuth/Anthropic credential path is no longer taught.

## 0.2.1 — 2026-07-17
- feat: one shared source now produces native packages for Claude Code,
  Codex, Gemini CLI, Cursor, and GitHub Copilot.
- feat: bootstrapped foundries now inherit adapter generation, native package
  isolation, and marketplace catalogs for all five hosts.

## 0.2.0 — 2026-07-12
- feat: the fork now inherits the **org-pattern framework** (MASTER.md), not just
  the plugin loop — the bootstrap skill carries over the constitution + guard, the
  agent contract (foundry/agents/), the single-writer orchestrator, the quota
  governor, the trust fence + read/act split, the auth surface, the owner's desk,
  per-agent identity, the state validator, heartbeats, and the merge-blocking evals.
  A fork boots a *governed company*, not an ungoverned loop.

## 0.1.4 — 2026-07-07
- docs: the from-spec bootstrap path now points at OPERATIONS.md §7–8 (governor &
  veto, community & fuel) — the optional layers a hand-built spine tends to
  forget (reviewer nit from i8, v14 P3).

## 0.1.3 — 2026-07-07
- docs: author normalized to "Nightshift Foundry" to match the rest of the
  marketplace, and a standard `## Recipes` section added (skeleton consistency,
  v13 B8).

## 0.1.2 — 2026-07-06
- docs: standard `## Manage` section — update, disable/enable, uninstall,
  and on-disk footprint in one place (v11 #2 README sweep).

## 0.1.1 — 2026-07-06
- docs: README install line bakes the real marketplace slug
  (`GhostlyGawd/plugin-foundry`) instead of a placeholder — works as pasted.

## 0.1.0 — 2026-07-05
- Initial release candidate: `bootstrap` skill (fork or from-spec scaffold).
