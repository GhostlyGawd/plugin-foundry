# Changelog

## 0.2.1 — 2026-07-17
- feat: one shared source now produces native packages for Claude Code,
  Codex, Gemini CLI, Cursor, and GitHub Copilot.
- hooks: equivalent session-start maps share the existing read-only check.

## 0.2.0 — 2026-07-07
- feat: `SessionStart` hook (`scripts/session-envcheck.sh`) — a fast, read-only,
  fail-open check that prints a one-line heads-up when a declared runtime version
  (`.nvmrc`/`.node-version`, `.python-version`) clearly drifts from what's
  installed. Silent on a match, when nothing is declared, or with
  `ENV_DOCTOR_SILENT=1`; always exits 0 (never blocks a session). The `envcheck`
  skill remains the deep, comprehensive pass with copyable fixes (v13 A2).

## 0.1.2 — 2026-07-06
- docs: standard `## Manage` section — update, disable/enable, uninstall,
  and on-disk footprint in one place (v11 #2 README sweep).

## 0.1.1 — 2026-07-06
- docs: README install line bakes the real marketplace slug
  (`GhostlyGawd/plugin-foundry`) instead of a placeholder — works as pasted.

## 0.1.0 — 2026-07-05
- Initial release: `envcheck` diagnosis skill (report + consented fixes).
