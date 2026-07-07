# Changelog

## 0.1.3 — 2026-07-07
- fix: sharpened the `doctor` skill's description with concrete trigger phrases
  ("doctor my plugin", "audit my plugin against the spec", "why won't my hook
  load", "before publishing") — it previously used the vague verb-only wording
  its own rule flags as an auto-invoke risk (v13 A4).
- chore: author normalized to "Nightshift Foundry" to match the rest of the
  marketplace (v13 B8).

## 0.1.2 — 2026-07-06
- docs: standard `## Manage` section — update, disable/enable, uninstall,
  and on-disk footprint in one place (v11 #2 README sweep).
- scaffold: generated READMEs now end with the same `## Manage` section.

## 0.1.1 — 2026-07-06
- docs: README install line bakes the real marketplace slug
  (`GhostlyGawd/plugin-foundry`) instead of a placeholder — works as pasted.

## 0.1.0 — 2026-07-04
- Initial release: `scaffold` and `doctor` skills.
