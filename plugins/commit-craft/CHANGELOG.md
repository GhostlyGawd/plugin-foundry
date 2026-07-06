# Changelog

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
