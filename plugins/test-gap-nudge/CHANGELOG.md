# Changelog — test-gap-nudge

## 0.3.2 — 2026-07-17
- feat: one shared source now produces native packages for Claude Code,
  Codex, Gemini CLI, Cursor, and GitHub Copilot.
- hooks: equivalent stop/after-agent maps share the existing advisory script.

## 0.3.1 — 2026-07-06
- docs: standard `## Manage` section — update, disable/enable, uninstall,
  and on-disk footprint in one place (v11 #2 README sweep).

## 0.3.0 — 2026-07-06
- debug: `TEST_GAP_NUDGE_DEBUG=1` appends the decision trail (why silent / why
  nudged) to `$TMPDIR/test-gap-nudge-debug.log`. Off by default; with it unset,
  behavior is byte-identical — proven by suite checks.

## 0.2.0 — 2026-07-06
- config: `TEST_GAP_NUDGE_EXTS` overrides the source-extension list
  (pipe/comma/space-separated). Sanitized to `[A-Za-z0-9|]` so a malformed
  value can never break the hook; empty → default list. The hook stays a guest:
  fail-open behavior is unchanged and covered by new suite checks.

## 0.1.1 — 2026-07-06
- docs: README install line bakes the real marketplace slug
  (`GhostlyGawd/plugin-foundry`) instead of a placeholder — works as pasted.

## 0.1.0 — 2026-07-06
- Initial release: advisory `Stop` hook. Source-vs-test classification of
  `git status --porcelain -uall` (`-uall` so files inside brand-new directories
  are seen individually — review catch before first release), one `systemMessage`
  nudge per session, fail-open everywhere (always exit 0), read-only except a
  TMPDIR marker.
