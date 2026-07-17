# Changelog

## 0.2.1 — 2026-07-17
- feat: one shared source now produces native packages for Claude Code,
  Codex, Gemini CLI, Cursor, and GitHub Copilot.
- hooks: equivalent start and stop/after-agent maps share the existing scripts.

## 0.2.0 — 2026-07-07
- feat: two read-only, fail-open hooks make the plugin match its own promise
  ("writes a recap when a session ends and recalls it when the next starts"),
  which until now was skill-only (v13 B5):
  - `Stop` (`scripts/recap-nudge.sh`) — suggests a recap once per session when
    there's uncommitted work and none was written today; silent otherwise.
  - `SessionStart` (`scripts/recap-recall.sh`) — surfaces the last handoff's
    title so you resume where you left off; silent when no `SESSION-RECAP.md`.
  Both exit 0 always; silence with `SESSION_RECAP_SILENT=1`.
- docs: recap now notes source-changed-without-tests under Open questions — the
  signal test-gap-nudge raises, captured in the handoff (v13 B6 synergy).

## 0.1.2 — 2026-07-06
- docs: standard `## Manage` section — update, disable/enable, uninstall,
  and on-disk footprint in one place (v11 #2 README sweep).

## 0.1.1 — 2026-07-06
- docs: README install line bakes the real marketplace slug
  (`GhostlyGawd/plugin-foundry`) instead of a placeholder — works as pasted.

## 0.1.0 — 2026-07-05
- Initial release: append-only dated `recap` skill.
