# Changelog

## 0.3.3 — 2026-07-17
- feat: one shared source now produces native packages for Claude Code,
  Codex, Gemini CLI, Cursor, and GitHub Copilot.
- hooks: equivalent pre-tool hook maps share the existing fail-open guard.

## 0.3.2 — 2026-07-07
- fix: the `commit` skill now honours `COMMIT_CRAFT_TYPES` too — it drafts using
  the same allowed-type list the guard hook enforces, so a customized type set no
  longer produces messages the guard rejects (config parity, v13 A3).
- chore: guard debug log uses timezone-aware UTC (drops the deprecated
  `datetime.utcnow()`); no behavior change, debug-only.

## 0.3.1 — 2026-07-06
- docs: standard `## Manage` section — update, disable/enable, uninstall,
  and on-disk footprint in one place (v11 #2 README sweep).

## 0.3.0 — 2026-07-06
- debug: `COMMIT_CRAFT_DEBUG=1` appends the guard's decision trail (pass reason
  or BLOCK + enforced type list) to `$TMPDIR/commit-craft-debug.log`. Off by
  default; behavior unchanged when unset.

## 0.2.0 — 2026-07-06
- config: `COMMIT_CRAFT_TYPES` replaces the guard's allowed type list
  (pipe/comma/space-separated). Tokens are restricted to lowercase letters —
  regex injection is structurally impossible — and an empty/malformed value
  falls back to the default list. Fail-open behavior unchanged; the block
  message now names the list it enforced.

## 0.1.1 — 2026-07-06
- docs: README install line bakes the real marketplace slug
  (`GhostlyGawd/plugin-foundry`) instead of a placeholder — works as pasted.

## 0.1.0 — 2026-07-05
- Initial release: `commit` skill + fail-open conventional-commit guard hook.
