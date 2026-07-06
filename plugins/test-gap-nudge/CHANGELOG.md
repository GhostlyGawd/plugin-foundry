# Changelog — test-gap-nudge

## 0.1.0 — 2026-07-06
- Initial release: advisory `Stop` hook. Source-vs-test classification of
  `git status --porcelain -uall` (`-uall` so files inside brand-new directories
  are seen individually — review catch before first release), one `systemMessage`
  nudge per session, fail-open everywhere (always exit 0), read-only except a
  TMPDIR marker.
