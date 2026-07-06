# Changelog — test-gap-nudge

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
