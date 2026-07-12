# BACKLOG

Priorities: **P0** = drop everything · P1 = important · P2 = normal · `blocked:` needs
diagnosis. Check items off, don't delete. Max 3 new items per iteration.

## Master program (MASTER.md — operator-directed, ADR-026, i218)
The reconciled org-pattern program: Stage 0 safe core → proof artifacts →
integrate table-stakes → launch → build in public. MASTER.md §14 is the full
task list and single source of truth; items enter here ≤3 per iteration, in §10
order, honoring §14 dependencies. Stage 0 tools/ work is pre-authorized by
ADR-026 (two-iteration rule); ADR-027–030 land with their items.
- [x] P0 (builder) MASTER P0.1 — agent contract & manifest: charter/AGENTS.md
      (contract prose + four hard rules), `agent.json` JSON Schema →
      foundry/agents/schema.json, loader + registry generator in tools/lib.py →
      foundry/agents/registry.json. Acceptance: a sample manifest loads and
      validates; any hard-rule violation is rejected. (MASTER.md §14; ADR-026)
      DONE i219: loader + 4 hard rules live in lib.py, build.py gates on them,
      first manifest = foundry-loop (grandfathered, dormant), 9-case suite green.
      Program ledger opened at state/PROGRAM.md; mandate + rulings at ADR-031.
- [x] P0 (builder) MASTER P0.5 — constitution + guard: charter/CONSTITUTION.md
      (never-do list + human-ratification list + the public "we don't spam
      maintainers" clause) and tools/guard.py (allow / block-with-reason on a
      proposed changeset). Depends: P0.1. File ADR-027. Acceptance: simulated
      schema-edit and record-deletion changesets block; a within-limits doc
      change passes. (MASTER.md §14)
      DONE i220: 4 articles ratified; guard allow/desk/block fails closed;
      desk primitive (desk.py + DESK.jsonl, dedup) live; 13-case suite green.
- [x] P1 (builder) MASTER P0.3+P0.4+P0.9 — the cheap trio (one §14 Stage 0
      bullet): per-agent commit identity, shared-state validator, heartbeats.
      DONE i221: identities.json + commit.py + validate.py trailer law;
      validate_state.py in gates.yml; heartbeat.py + ops-guard liveness job;
      15-case suite (untrailed agent commit fails, malformed state caught
      pointedly, stale/never-beaten agents named, dormant exempt).
- [x] P0 (builder) MASTER P0.6 — quota governor v2 (ADR-028). DONE i222:
      quota.py pressure model + tier shedding (product never sheds on
      pressure; ≥1.0 kill switch desk-pauses), dollar path absolute,
      run-shift wired, decisions ledgered; 15-case suite green.
- [x] P1 (builder) MASTER AUTH-1 — auth abstraction: one swappable auth surface
      (no agent reads the token env var directly), token-expiry/rejection
      detection with a loud failure (the exact silence behind the 2026-07-07
      re-pause), document the four hard migration triggers. Acceptance:
      OAuth→API switch requires no agent changes. (MASTER.md §14)
      DONE i223: auth.py check/probe; loop.sh halts LOUD on first auth failure
      (alarm + remedy); OPERATIONS §9; lint proves the surface is single.
- [x] P0 (builder) MASTER P0.2 — trust fencing + read/act split. DONE i224:
      fence.py wrap (envelope, marker-collision-proof, sha256 provenance) +
      scan (9 attack shapes incl. third-party-PR lure + Agent-trailer spoof;
      FENCE_BACKEND swappable, falls back closed); intake.py ported to the
      seam; validate_state lint fails unfenced ingests_untrusted prompts;
      11-case suite green.
- [x] P0 (builder) MASTER P0.7 — chief-of-staff orchestrator, the keystone.
      DONE i225: single-writer landing pipeline live and ACTIVE (deterministic
      python — runs while the loop is token-paused); conflicts resolve by
      precedence with loser re-queue; guard/desk/gate vetoes honored; every
      landing attributed per-agent (P0.3); orchestrate.yml shares the shift
      concurrency group (no race with run-shift); 9-case suite green.
      STAGE 0 COMPLETE.
- [x] P0 (growth) MASTER GAP-A — the quality number (highest-priority gap).
      DONE i226: definition pinned (shipped = published kind:plugin; first-try
      = clean pass through QA AND review — REVIEW: bounced disqualifies;
      bounces displayed, never hidden), computed from records/journal/ledger
      only, on the hero stat row + site/quality.json badge endpoint. The
      honest number: 10 shipped · 86% first-try · 5 bounces · 226 iterations.

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
- [x] P3 (builder) fork-a-foundry polish: from-spec path links OPERATIONS §7–8 (reviewer nit, i8).
      DONE i216 (v14) — from-spec path links §7–8; fork-a-foundry v0.1.4.
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
- [x] P1 Walk session-recap through spec (hooks + skill combo — good hook-safety exercise).
      DONE — published, now at v0.1.2 (see foundry/records/session-recap.md; hygiene i207).
- [x] P1 Post-publish re-test of plugin-smith (it shipped at genesis without a QA pass
      of record — hold it to the same bar; Version law applies to any fixes).
      DONE — executable suite exists (foundry/tests/plugin-smith/), weekly re-verified, verified: stamp current (hygiene i207).
- [x] P2 Per-plugin detail pages on the catalog — already exist: 38 birth
      certificates at site/p/<name>.html (build_pages); stale item, closed i140.
- [x] P2 CONTRIBUTING.md for humans proposing plugin ideas.
      DONE — CONTRIBUTING.md exists with Lanes 0–4 (hygiene i207).
- [x] P1 Go-live (human-assisted): fill foundry/site-config.json, push to GitHub,
      enable Pages (Actions source), add ANTHROPIC_API_KEY secret — per OPERATIONS.md.
      DONE i196 (ADR-020): Pages enabled via dispatch, window LIVE at the pages_url; only the Claude secret remains (hygiene i207).
- [x] P1 (designer) First Theme of the Month via ADR once in grow phase.
      DONE i216 (v14, ADR-024): July 2026 = "Repo hygiene"; set in STATE.theme,
      banners the window. Community-vote path dormant until traffic (ADR-023).
- [x] P2 (growth) Spec shift-streak — OBE: specced, built, and published in the
      v8 slate (i134); baseline arms at go-live. Closed i140.
- [x] P2 (growth) Spec weekly-shipnote — OBE: published i113 with fixture suite.
      Closed i140.
- [ ] P2 (operator, optional) Wire GoatCounter per OPERATIONS.md § 6 for real pageviews.
- [x] P1 (operator) Genesis ceremony unblock (v12 4.1, ADR-021 — blessing on
      record): create ONE empty public repo (suggested name: dawnshift-forge);
      a session then seeds it per fork-a-foundry and registers the first
      sister. Attempted i212: create_repository → 403, no session or workflow
      token can create repos. Everything downstream is built and waiting
      (network strip, family tree, Lane 4 verification, badges).
      DONE i214: operator created GhostlyGawd/test; parent seeded it whole
      (protocol, charter, tools, workflows, one idea record, reciprocal network
      entry), child's own gates ran green pre-push, Lane 4 duty verified
      (LOOP.md + records present), registered as the first sister.

## v7 slate — SHIPPED ✓ (audit-002)
All 12 published i35–i86; experiments armed with dated reviews. World-gated
arming: PINGS_ENABLED, first question/commission, next tag, Monday cron.

## Roadmap phase gates (ROADMAP.md — Auditor verifies, nobody else checks boxes)
- [ ] GATE A — window live 14d, ledger arming, 6 experiment baselines [GATED: operator+world]
- [ ] GATE B — ≥8 shipped, ≥2 public verdicts, first bug survived well [GATED: world]
- [ ] GATE C — ≥3 community ships, 1st paid commission, ≥1 sponsored shift [GATED: community]

- [x] P3 (builder) countdown: derive shift hours from run-shift.yml cron instead
      of the documented constant (drift risk noted at i46).
      DONE i216 (v14, ADR-024): build.py parses the cron → SHIFT_MIN/SHIFT_HOURS.
- [x] P3 (designer) saga wall ellipsis — DONE i145 (word-boundary clip()).
- [x] P3 (designer) field-report cap link — DONE i145 ("all N reports →" when >8).
- [x] P2 (qa) Suite backfill: executable tests for the v5/v7 features that
      published on manual probes (audit-003 finding #3) — one suite per pass.
      DONE — v9 slate #10 (audit-004: 13/13 built); every published record now requires an executable suite at rc+ (validator law) (hygiene i207).
- [x] P3 (builder) qa.sh: warn on non-executable *.test.sh files instead of
      silent skip (sharp edge, audit-004; tools/ change — ADR first).
      DONE i161 (v10 #7, ADR-018): went further than warn — per-file FAIL.

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

## v13 slate — SHIPPED ✓ (ADR-022/023, directed PR)
All 14 built as one directed PR (i215). Shelf-truth: A1 pr-narrator relabel ·
A2 env-doctor SessionStart hook (v0.2.0) · A3 commit-craft type parity (v0.3.2) ·
A4 plugin-smith doctor description (v0.1.3). Depth: B5 session-recap hooks
(v0.2.0) · B6 synergies · B7 night-clerk catalog regen (v0.2.5) · B8 author +
README parity (fork-a-foundry v0.1.3, dep-bump-brief v0.1.1, pr-narrator v0.1.3).
Gates: C9 sitemap content-dated · C10 worker idempotency + cap + parse-in-try ·
C11 intake/metrics truncation · C12 restamp guard + parser dedup · C13 qa.yml
tools/**. Honest-zero: D14 dormant experiments (ADR-023). qa 248 ok · 0 fail.

## v14 — SHIPPED ✓ (ADR-024, directed PR) — the buildable line, finished
i216: tenth plugin **todo-ledger** walked idea → published (108 tok, suite 9/9);
first **Theme of the Month** (July = "Repo hygiene"); **bug** build.py mkdirs
site/; **P3s** countdown derives shift hours from cron + fork-a-foundry from-spec
→ OPERATIONS §7–8. qa 257 ok · 0 fail. **What remains is gated, not buildable by
the line:** commission tiers + GoatCounter (operator); pr-gated CRON default and
roadmap gates A/B/C (world/community). The line has nothing left it can build alone.

## v0.7 window redesign — SHIPPED ✓ (ADR-025, operator-directed PR)
i217 (designer): the living window **reimagined for the first-time visitor**.
Nightshift Foundry brand **evolved, not replaced** — kept name, `foundry` slug,
kraft palette, every honesty law, all telemetry/provenance machinery. New:
friendly sans typography (mono only for code/telemetry) + ember CTA; a
conversion-funnel IA (plain-language hero defining Claude Code + plugins →
30-second primer + before/after → 3-step install → shelf grouped by category with
benefit-led cards → kits → trust section → telemetry demoted to "Under the hood"
→ vote → commission + install); `categories` added to data.json; stat row shows
only substantiated numbers. All test-pinned machinery ported verbatim; qa 257 ok ·
0 fail; official --strict green; zero horizontal overflow 320/402/1440px.
- [ ] P3 (designer) Reshoot foundry/assets/og-image.png for the new v0.7 hero
      (the social card still shows the old window).

## Bugs (published plugins — installed users first; see LOOP.md priority 3)
- [x] P3 (builder) build.py assumes site/ exists (crashes on a fresh checkout
      without it — found by the firstborn at genesis, i214); mkdir it in main().
      DONE i216 (v14): main() mkdirs site/ first; verified from a bare copy.
Populated by `tools/intake.py` from issues labeled `bug`.
Format: `- [ ] B#<issue> <plugin> — <summary>`
- (none yet)

## Commissions (paid — outrank standing work; see LOOP.md priority 3)
Populated automatically by `tools/intake.py` from GitHub issues labeled `commission`.
Format: `- [ ] C#<issue> (<author>) <title> — <summary>`
- (none yet)

## Experiments — DORMANT until traffic (v13 D14, ADR-023)
METRICS.jsonl still reads 0 stars / null traffic / 0 votes: none of these can earn
an honest verdict yet, so they are **dormant**, not overdue. Each review clock
starts at first real traffic (Gate A: window live with non-null metrics), NOT the
calendar dates below (kept as the intended *cadence*, re-anchored on that day). No
dormant experiment counts toward the extend-twice-kill rule or the calibration
tripwire (charter/GROWTH.md).
- [ ] token-cost-badges — dormant → review +14d from first traffic (clones/uniques ratio)
- [ ] idea-credit-loop — dormant → +21d from first traffic (suggester spread + repeat rate)
- [ ] fuel-gauge — dormant → review once watchers > 0 (sponsored-shift credits)
- [ ] weekly-shipnote — dormant → review after 3 notes with a live audience (watchers trend)
- [ ] shift-streak — dormant → +14d from first traffic (uniques_14d trend)
- [ ] starter-kits — dormant → +21d from first traffic (clones per unique)
- [ ] community-voting — dormant → +14d from first public traffic (open_ideas, idea_votes_total)
- [ ] scannable-window — dormant → +14d from first public traffic (views_14d, uniques_14d)

## Hunting grounds (Ideator's sources — Maintainer prunes)
- Dogfood friction: this repo's own journal — every "I wished Claude Code would…" is a pitch.
- Repetition mining: any prompt a developer types twice a week is a skill; any check
  they run before committing is a hook.
- Event mining: walk the official hooks event table — each event is a category of
  plugin nobody built yet.
- Gap mining: what do teams keep in CLAUDE.md that should be a versioned, shareable plugin?
- Companion mining: popular CLIs and services without a good MCP/LSP bridge.

## Idea inbox (humans drop raw pitches here; Ideator formalizes)
- [x] I#4 (GhostlyGawd) Idea: dep-bump-brief — plain-language briefs for dependency-bump PRs
      FORMALIZED and PUBLISHED v0.1.0 (i199–i203, v12 1.2).
- [x] I#5 (GhostlyGawd) Idea: todo-ledger — TODO/FIXME debt as a dated, ranked report
      FORMALIZED and PUBLISHED v0.1.0 (i216, v14) — the tenth plugin, first
      exhibit of July's "Repo hygiene" theme.
- [x] I#6 (GhostlyGawd) Idea: cross-foundry-exchange — sister workshops trade their best ideas
      FORMALIZED — record at stage spec (i178).
