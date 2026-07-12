# PROGRAM — MASTER.md execution ledger (ADR-026 adoption · ADR-031 mandate)

Single place where every MASTER.md §14 line item is **accounted for**. Updated every
program iteration. Statuses: **DONE** (built+tested, evidence cited) · **PARTIAL**
(in progress, what remains named) · **QUEUED** (not started) · **DESK** (built to the
repo's edge; one operator click remains — desk item filed) · **OPERATOR** (inherently
the operator's action; kit prepared) · **DEFERRED** (per MASTER.md verdict; tracked,
not lost) · **DORMANT** (built; runtime waits on the CI token / STOP removal).

Mandate (ADR-031): operator directive 2026-07-12 — full merge authority granted;
build every line item end to end, 100% accounted for. Outward actions under the
operator's identity (launch posts, third-party account signups) are prepared and
desk-queued, never performed autonomously — constitution floor.

## Stage 0 — the minimum safe, story-bearing core

| Item | Verdict | Status | Evidence |
|---|---|---|---|
| P0.1 agent contract & manifest | BUILD | **DONE** (i219) | charter/AGENTS.md · foundry/agents/schema.json · loader+registry in tools/lib.py · build.py gate · foundry/tests/_tools/agents.test.sh (9 cases) |
| P0.5 constitution + guard | BUILD | **DONE** (i220) | charter/CONSTITUTION.md · tools/guard.py (allow/desk/block, fails closed) · tools/desk.py + state/DESK.jsonl (minimal desk) · ADR-027 · 13-case suite |
| P0.7 chief-of-staff orchestrator | BUILD | **DONE** (i225) | tools/orchestrator.py (collect→precedence→guard→gates→attributed commits; conflicts defer+re-queue; desk holds/approvals/rejections; red gates revert byte-for-byte) · orchestrate.yml (shift concurrency group, mode:pr parity) · active NOW (deterministic, no token needed) · 9-case suite |
| P0.6 quota governor v2 | BUILD | **DONE** (i222) | tools/quota.py (168h pressure, low→high shed, product never on pressure, ≥1.0 kill switch → desk, dollar path absolute) · run-shift wiring · ADR-028 · 15-case suite |
| AUTH-1 auth abstraction | BUILD | **DONE** (i223) | tools/auth.py (api > subscription > local-login > loud CI fail) · probe classifies auth failures, loop.sh halts on FIRST · migration triggers in auth.py + OPERATIONS §9 · single-surface lint · 10-case suite |
| P0.2 trust fencing + read/act split | BUY+WRAP | **DONE** (i224) | tools/fence.py wrap/scan (envelope uncloseable from inside; FENCE_BACKEND seam falls back to builtin floor) · intake ported · unfenced-ingestion CI lint in validate_state · read/act split live via hard rule 2 + guard · 11-case suite. LLM Guard/Lakera upgrade = desk item at Stage 2 |
| P0.3 per-agent commit identity | BUILD | **DONE** (i221) | identities.json · tools/commit.py (author + Agent: trailer) · validate.py trailer law (HEAD, fails on untrailed agent commits) |
| P0.4 state validator | BUILD | **DONE** (i221) | tools/validate_state.py (STATE/BUDGET/METRICS/DESK/votes/verified/reports/kits/alarms/network/registry/identities/heartbeats) · gates.yml step · orchestrator pre-commit at P0.7 |
| P0.9 heartbeats / liveness | CHEAP | **DONE** (i221) | tools/heartbeat.py beat/check (×1.5 grace, dormant exempt) · heartbeats.json · ops-guard liveness job (alarms, never fails) |

## Stage 1 — proof artifacts

| Item | Verdict | Status | Evidence |
|---|---|---|---|
| GAP-A quality number | BUILD | **DONE** (i226) | build_quality() in build.py — 10 shipped · 86% first-try (QA+review, bounces disqualify) · 5 bounces shown · 226 iterations · ledger shifts/spend · hero stat cell · site/quality.json shields endpoint · 3-case suite |
| GAP-A2 live dashboard | BUILD | **DONE** (i227) | qstrip running counter in "Under the hood" (quality + latest ship, all substantiated) · hero already carries the number (i226) — ADR-025 funnel preserved · Chromium render check: strip live, zero page errors |
| GAP-A3 proof artifact (shift replay) | BUILD | **DONE** (i228) | tools/replay.py → foundry/assets/replay.svg (7-frame SMIL loop of the real i89–i93 starter-kits arc; the GATE BLOCKS frame quotes the actual bounce) · labeled REPLAY + record citation · deterministic · embedded on the site, README next (A4) · 6-case suite w/ record-drift guard |
| GAP-A4 README first screen + org chart | BY HAND | **DONE** (i229) | hand-written: hook → replay embed → proof counter + badges (quality.json endpoint) → 2-command install → 1-command fork → org-chart mermaid → refreshed layout/truth sections. Fork command verified against marketplace.json |
| GAP-B auto-publish to registries | BUILD | **DONE** (i230) | passive indexing live (valid marketplace.json since genesis) · tools/publish.py → foundry/SUBMISSIONS.md (prefilled intake links + copy for awesome-claude-code, Anthropic community form, generic blurbs) · desk item d-0001 queued for the operator click · tool provably offline · 5-case suite |

## Stage 2 — table-stakes integrations

| Item | Verdict | Status | Evidence |
|---|---|---|---|
| P3.2 dependency bumping + GAP-D cooldowns | BUY | **DONE** (i233) | .github/dependabot.yml (native, GitHub Actions, 5-day cooldown, weekly grouping) · renovate.json (5-day minimumReleaseAge, no automerge) · socket.yml (malware/install-scripts/typosquat block) · app installs → desk d-0002 · 4-case config-validity suite |
| P3.5 community PR review | BUY | **DONE** (i234) | .coderabbit.yaml bound to the foundry's laws (Version law, hook safety, two-iteration ADR rule, growth-honesty) · app install → desk d-0003 · validity suite |
| P5.2 agent evals (merge-blocking) | BUY | **DONE** (i232) | tools/evals.py + 25 golden cases (guard law + fence detection) merge-blocking in gates.yml · proven able to go red (poison-fixture test) · promptfoo.yaml config-ready for red-team/spec-drift/reviewer (API-armed) · ADR-030 · 4-case meta-suite |
| P5.1 factory brain (memory) | BUY | **DONE** (i235) | tools/memory.py — dedup-on-write local store (near-duplicate refused, --force override), deterministic recall, MEMORY_BACKEND seam (Mem0/Zep, falls back to local floor) · 5 real lessons seeded from this program · 8-case suite |
| P4.3 visual regression + narrator | BUY | **DONE** (i236) | tools/vishot.py — narrate (deterministic vision-narration from data.json, committed) + shoot (best-effort Playwright capture, degrades cleanly) · deploy-site capture step · argos.config.json + desk d-0005 for hosted diffing · 6-case suite. STAGE 2 COMPLETE |
| P0.8 owner's desk (ranking in-house) | SPLIT | **DONE** (i231) | ranking law (kind strictly dominates, age within kind) + dedup in desk.py · `queue`/`sync` → ONE pinned ops-desk issue (degrades ledger-only) · site/desk.html public card · orchestrate.yml syncs post-run · approvals land only via the orchestrator (i225) · ADR-029 · 6-case suite. G4 closed |
| P2.1 issue triage (Dosu) | BUY | **DONE** (i234) | .dosu.yaml triage-only (auto-answer OFF — night-clerk stays deferred), untrusted-data, routing mirrors intake + labels · app install → desk d-0004 · validity suite |
| P4.4 night-clerk responder | DEFER | **DEFERRED** | per MASTER.md — risky pre-launch, most ToS-sensitive; revisit post-launch |

## Stage 3 — launch (concentrated window)

| Item | Verdict | Status | Evidence |
|---|---|---|---|
| Show HN / Reddit / X posts | OPERATOR | **DONE** (i237) | foundry/LAUNCH.md — Show HN copy, tailored Reddit posts, X thread, all substantiated · desk d-0006 (operator go) · honesty suite pins the numbers to the badge |
| awesome-claude-code + Anthropic marketplace submissions | OPERATOR | **DONE** (i237) | prefilled intake links in SUBMISSIONS.md (d-0001) + LAUNCH.md; submissions only, never third-party PRs |
| Newsletters / YouTube / evergreens (T+1–2wk) | OPERATOR | **DONE** (i237) | newsletter list + 3 evergreen post drafts + T+ calendar in LAUNCH.md. STAGE 3 COMPLETE |

## Stage 4 — build the rest in public

| Item | Verdict | Status | Evidence |
|---|---|---|---|
| P1.4 dogfood report card | HALO | **DONE** (i238) | tools/dogfood.py — grades genuine use (construction mentions excluded), shows not-yet honestly, auto-regraded in build · site card with per-plugin evidence chips · 4-case suite |
| P1.1 per-shift operator briefing | HALO | **DONE** (i240) | tools/briefing.py (<30s read: last move, quality number, top-3 ranked desk items, alarms) · briefing agent (read_only/low) · deterministic |
| P1.2 ask-the-factory | HALO | **DONE** (i241) | tools/ask.py — sourced retrieval over JOURNAL/DECISIONS/records (every answer cites its source; admits when history has none) · ask agent (ingests_untrusted, fenced, read_only) |
| P4.2 shipnotes weekly + social variant | HALO | **DONE** (i240) | shipnote.py --social (one substantiated post, weekly regardless of volume); weekly regression intact |
| P5.4 self-authored postmortems | HALO | **DONE** (i239) | postmortem agent (proposes/high/event) + prompt · reviews/postmortems/pm-001 (the REAL token incident, blameless, cites AUTH-1) · RUNBOOK.md with the operator procedure · pm↔m-001 memory loop · 6-case suite |
| P5.5 quarterly state-of-the-company | HALO | **DONE** (i240) | tools/quarterly.py — real metric deltas from METRICS.jsonl, honest failures (bounces + postmortems), 3-5 recs landed+deduped on the desk · quarterly agent · re-launch moment |
| P2.2 steer-by-issue | HALO | **DONE** (i242) | tools/steer.py — fenced classify: normal→backlog, rule-touching→desk (never a silent law edit), injection→held for red-team · steer agent (ingests_untrusted, fenced, proposes) |
| P2.5 naming ceremony assistant | HALO | **DONE** (i242) | tools/naming.py — collision check (exact, near/separator, reserved, malformed) before a slug is forever · naming agent · company already named (ADR-011) so scope = plugin names |
| P1.5 ecosystem scout | HALO | **DONE** (i241) | scout agent (ingests_untrusted, fenced:true, read_only — read/act split) + prompt routing fetched text through fence.py |
| P1.3 failed-shift diagnostician | STAKES | **DONE** (i241) | tools/diagnose.py — classifies auth/quota/budget/gate-red/disk with a next step + ops-alarm, honest 'unknown' when no signature; reuses the auth classifier · diagnostician agent |
| P3.1 spec-drift auditor | BUILD | QUEUED | |
| P3.3 tripwire auditor | BUILD | QUEUED | |
| P3.4 commission red-team | BUILD | QUEUED | |
| GAP-C multi-harness portability | BUILD | QUEUED | exporter; published plugins untouched (no Version-law churn) |
| GAP-E durable execution / resume | DOC | QUEUED | journal-as-checkpoint documentation path (MASTER.md's own option) |
| fork-a-foundry inherits the framework | BUILD | QUEUED | Version law: semver + CHANGELOG same iteration |

## Deferred — tracked, not lost (MASTER.md verdicts)

| Item | Why |
|---|---|
| P2.3 backlog grooming | low visible value |
| P2.4 auto-drafted ADRs | not load-bearing early |
| P3.6 deprecation/migration drafter | no users to migrate yet |
| P4.1 README/starter-kit generator | launch README is hand-written (GAP-A4) |
| P5.3 champion-challenger prompt A/B | overlaps evals; auto-promotion premature |
| GAP-F agent identity/auth at scale | roadmap note |
| P4.4 night-clerk responder | see Stage 2 row |

## Program-level definition of done (§14) — verified at close-out

- [ ] No workflow other than the orchestrator (P0.7) and run-shift writes to main
- [ ] Every untrusted input path fenced; CI lint proves it
- [ ] Every human decision reaches exactly one place — the desk; nothing requiring approval auto-merges
- [ ] Guard + constitution block schema edits, record deletions, self-governing edits, third-party PRs; each desk-routed
- [ ] Quota governor v2 protects the product loop under rate-limit pressure
- [ ] Every agent has an identity, a heartbeat, and (risky ones) an eval fixture
- [ ] The quality number is live and public
- [ ] ADRs 026–030 filed (+031 mandate)
- [ ] fork-a-foundry inherits the whole framework
