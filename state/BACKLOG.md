# BACKLOG

Priorities: **P0** = drop everything · P1 = important · P2 = normal · `blocked:` needs
diagnosis. Check items off, don't delete. Max 3 new items per iteration.

## Bootstrap (in order; role in parentheses — walks commit-craft spec → published)
- [x] B1 (auditor) Run `python3 tools/validate.py && python3 tools/build.py` and
      `bash tools/smoke.sh`; confirm green; journal baseline: records per stage,
      plugins on disk, marketplace entries.
- [x] B2 (builder) Build commit-craft component 1: the `commit` skill
      (skills/commit/SKILL.md) exactly per its spec's verbatim description; scaffold
      via plugin-smith's scaffold skill; plugin.json; advance record spec → building
      with Build log entry.
- [x] B3 (builder) Build commit-craft component 2: the message-guard hook
      (hooks/hooks.json + scripts/check-commit-msg.sh, executable, shebang, quoted
      "${CLAUDE_PLUGIN_ROOT}"); README.md + CHANGELOG.md (0.1.0 – Unreleased);
      Build log entry.
- [x] B4 (qa) Full three-tier test pass per charter/TESTING.md against the spec's
      acceptance checks; Test log; advance building → rc, or bounce with reasons.
- [x] B5 (reviewer) Line-by-line review (prompt craft, hook safety, token thrift,
      docs truth); QUALITY axis scores; `REVIEW: approved` or bounce; Review log.
- [x] B6 (maintainer) Publish commit-craft: marketplace.json entry
      (source ./plugins/commit-craft), version 0.1.0 in plugin.json + record,
      CHANGELOG dated, README install line verified; advance rc → published.
- [x] B7 (designer) **Naming Ceremony** per charter/BRAND.md — marketplace + repo
      name, ASCII wordmark, brand v1, ADR; update STATE.json, marketplace.json name,
      README, catalog copy, every install snippet.
- [x] B8 (designer) Apply brand v1 to the catalog (template changes need a
      prior-iteration ADR; copy/palette-in-place fine now).
- [x] B9 (ideator) Replenish the line: 3–5 new idea records, deduped against records
      + shelf, drawn from § Hunting grounds and journaled dogfood friction.
- [x] B10 (auditor) Audit #1 → reviews/audit-001.md: QA rigor, version-law
      compliance, token budgets. If sound: phase → "grow", refill role_queue, ADR.

## Grow (worked after bootstrap)
- [x] P1 Review + publish fork-a-foundry — DONE i8/i9, tag fork-a-foundry-v0.1.0.
- [ ] P3 (builder) fork-a-foundry polish: from-spec path links OPERATIONS §7–8 (reviewer nit, i8).
- [x] P1 (growth) Run the pr-gated-publishes trial — interim verdict i144/ADR-017:
      directed slates ride PRs (proven, PR #9); cron default deferred to real
      mode:pr shift data once the factory is live.
- [ ] P2 (growth) pr-gated-publishes: rule on the CRON default after 10 mode:pr
      shifts or 21 days of a live factory (spec terms; successor to the i144
      interim verdict).
- [x] P1 (qa) QA fixture passes for the four building-stage v5 features
      (field-reports, community-hall, saga-page, embed-badges) → rc, then review
      → publish. DONE — all four published in the v8 slate (i107–i128).
- [ ] P2 (operator+growth) Wire commission tiers per foundry/records/commission-tiers.md,
      then start its 45-day pricing experiment.
- [ ] P1 Walk session-recap through spec (hooks + skill combo — good hook-safety exercise).
- [ ] P1 Post-publish re-test of plugin-smith (it shipped at genesis without a QA pass
      of record — hold it to the same bar; Version law applies to any fixes).
- [x] P2 Per-plugin detail pages on the catalog — already exist: 38 birth
      certificates at site/p/<name>.html (build_pages); stale item, closed i140.
- [ ] P2 CONTRIBUTING.md for humans proposing plugin ideas.
- [ ] P1 Go-live (human-assisted): fill foundry/site-config.json, push to GitHub,
      enable Pages (Actions source), add ANTHROPIC_API_KEY secret — per OPERATIONS.md.
- [ ] P1 (designer) First Theme of the Month via ADR once in grow phase.
- [x] P2 (growth) Spec shift-streak — OBE: specced, built, and published in the
      v8 slate (i134); baseline arms at go-live. Closed i140.
- [x] P2 (growth) Spec weekly-shipnote — OBE: published i113 with fixture suite.
      Closed i140.
- [ ] P2 (operator, optional) Wire GoatCounter per OPERATIONS.md § 6 for real pageviews.

## v7 slate — SHIPPED ✓ (audit-002)
All 12 published i35–i86; experiments armed with dated reviews. World-gated
arming: PINGS_ENABLED, first question/commission, next tag, Monday cron.

## Roadmap phase gates (ROADMAP.md — Auditor verifies, nobody else checks boxes)
- [ ] GATE A — window live 14d, ledger arming, 6 experiment baselines [GATED: operator+world]
- [ ] GATE B — ≥8 shipped, ≥2 public verdicts, first bug survived well [GATED: world]
- [ ] GATE C — ≥3 community ships, 1st paid commission, ≥1 sponsored shift [GATED: community]

- [ ] P3 (builder) countdown: derive shift hours from run-shift.yml cron instead
      of the documented constant (drift risk noted at i46).
- [x] P3 (designer) saga wall ellipsis — DONE i145 (word-boundary clip()).
- [x] P3 (designer) field-report cap link — DONE i145 ("all N reports →" when >8).
- [ ] P2 (qa) Suite backfill: executable tests for the v5/v7 features that
      published on manual probes (audit-003 finding #3) — one suite per pass.

## v8 slate (ADR-014 — operator-directed; role_queue seeded for it)
- [x] P1 (line) Publish-or-bounce the ten rc features: reviewer+maintainer pairs in
      ADR-014 order; genuine reviews, tripwire stands. DONE i89–i134: 10/10
      published, 4 bounced first (starter-kits, token-cost-badges,
      weekly-shipnote, embed-badges) and fixed with pinned regressions.
- [x] P1 (builder) Walk test-gap-nudge idea → published — DONE i99–i106, tag
      test-gap-nudge-v0.1.0 (bounced once at review; -uall fix + regression).
- [x] P2 (growth) Seed mailbag FAQ + vote board with clearly foundry-authored
      content (growth-honesty law: no simulated activity) and ADR the intake.py
      idea-label path; builder applies it next iteration.

## Bugs (published plugins — installed users first; see LOOP.md priority 3)
Populated by `tools/intake.py` from issues labeled `bug`.
Format: `- [ ] B#<issue> <plugin> — <summary>`
- (none yet)

## Commissions (paid — outrank standing work; see LOOP.md priority 3)
Populated automatically by `tools/intake.py` from GitHub issues labeled `commission`.
Format: `- [ ] C#<issue> (<author>) <title> — <summary>`
- (none yet)

## Experiments open (growth reviews these when review-after passes — overdue = P1)
- [ ] token-cost-badges — review 2026-07-19 (clones/uniques ratio vs. prior snapshots)
- [ ] idea-credit-loop — review 2026-07-26 (suggester spread + repeat rate)
- [ ] fuel-gauge — review 2026-08-04 (watchers; sponsored-shift credits)
- [ ] weekly-shipnote — review after 3 notes (watchers trend)
- [ ] shift-streak — review 2026-07-19 (uniques_14d trend)
- [ ] starter-kits — review 2026-07-26 (clones per unique)
- community-voting — review 14 days after first public deploy (metric: open_ideas, idea_votes_total)
- scannable-window — review 14 days after first public deploy (metric: views_14d, uniques_14d)

## Hunting grounds (Ideator's sources — Maintainer prunes)
- Dogfood friction: this repo's own journal — every "I wished Claude Code would…" is a pitch.
- Repetition mining: any prompt a developer types twice a week is a skill; any check
  they run before committing is a hook.
- Event mining: walk the official hooks event table — each event is a category of
  plugin nobody built yet.
- Gap mining: what do teams keep in CLAUDE.md that should be a versioned, shareable plugin?
- Companion mining: popular CLIs and services without a good MCP/LSP bridge.

## Idea inbox (humans drop raw pitches here; Ideator formalizes)
- (empty)
