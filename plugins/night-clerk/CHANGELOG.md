# Changelog

## 0.2.6 — 2026-07-07
- catalog snapshot: todo-ledger 0.1.0 joins the shelf (tenth plugin) — the front
  desk can now recommend the tech-debt ledger; also picks up fork-a-foundry 0.1.4.

## 0.2.5 — 2026-07-07
- catalog snapshot regenerated (v13 B7): corrects two entries the shelf had been
  misdescribing — pr-narrator is a **skill**, not a "subagent" (tags `agents` →
  `skills`), and env-doctor now genuinely runs **at session start** (v0.2.0 hook)
  so its "at session start" line and `hooks` tag are finally accurate. Also picks
  up commit-craft 0.3.2, plugin-smith 0.1.3, session-recap 0.2.0, dep-bump-brief
  0.1.1, fork-a-foundry 0.1.3.
- clerk: for "newest/most recent" asks, the skill now says plainly the bundled
  snapshot is point-in-time and points at `/plugin marketplace update` + the live
  window for anything shipped since (decay honesty).

## 0.2.4 — 2026-07-07
- catalog snapshot: dep-bump-brief 0.1.0 joins the shelf (nine plugins)

## 0.2.3 — 2026-07-06
- docs: standard `## Manage` section — update, disable/enable, uninstall,
  and on-disk footprint in one place (v11 #2 README sweep).

## 0.2.2 — 2026-07-06
- catalog snapshot refreshed: shelf versions 0.3.0 for commit-craft and
  test-gap-nudge (debug trails)

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
