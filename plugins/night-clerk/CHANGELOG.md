# Changelog

## 0.2.1 — 2026-07-06
- catalog snapshot refreshed: shelf versions 0.2.0 for commit-craft and
  test-gap-nudge (config knobs) — whats-new answers stay true

## 0.2.0 — 2026-07-06
- new skill `whats-new`: compares installed foundry plugin versions (via
  `claude plugin list`) against the bundled catalog and hands you the exact
  `claude plugin update <name>` lines — the shelf finally tells you when it moved
- catalog snapshot now carries each plugin's shelf `version`

## 0.1.2 — 2026-07-06
- catalog snapshot: solo-dev kit added (env-doctor + test-gap-nudge +
  session-recap) — the clerk can now bundle the one-person-repo workflow

## 0.1.1 — 2026-07-06
- catalog snapshot regenerated: all 8 published plugins (test-gap-nudge was
  missing — the front desk was a day behind the shelf)
- catalog gains `kits`: the clerk can now offer curated bundles, published
  members only; SKILL step 2 teaches the behavior
- docs: README install line bakes the real marketplace slug

## 0.1.0 — 2026-07-05
- Initial release: `clerk` recommendation skill + bundled catalog snapshot.
