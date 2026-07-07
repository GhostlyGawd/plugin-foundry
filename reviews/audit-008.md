# Audit 008 — the v13 slate (IMPROVEMENTS v13 A1–D14, i215)

Auditor pass closing v13 (ADR-022/023) — the first slate built as a single
directed PR rather than N loop shifts. Directed: "Build all in order."

## Outcome: 14 built, 0 blocked

- **Lane A — shelf-truth:** pr-narrator relabeled to the truth (ships a skill,
  not an agent); env-doctor's SessionStart hook built (v0.2.0), resolving its
  "claimed [hooks], shipped a skill" contradiction toward value; commit-craft
  skill honours `COMMIT_CRAFT_TYPES` (v0.3.2); plugin-smith `doctor` description
  sharpened to concrete triggers (v0.1.3) — it had been failing the very bar it
  enforces.
- **Lane B — depth:** session-recap gained Stop-nudge + SessionStart-recall
  hooks (v0.2.0), making its `[skills, hooks]` record true; two cross-plugin
  synergies wired; night-clerk catalog regenerated once (v0.2.5), correcting the
  two mislabels at the discovery surface; author names normalized and README
  parity closed (fork-a-foundry v0.1.3, dep-bump-brief v0.1.1, pr-narrator v0.1.3).
- **Lane C — the gates:** sitemap.xml is content-dated (gates.yml no longer
  cries wolf); the commission worker survives its first dollar (idempotency,
  body cap, JSON.parse moved into the try); intake/metrics no longer silently
  truncate; restamp guards a nameless record; four more tools route through
  `lib.parse_front_matter` (one parser, one truth); qa.yml runs on `tools/**`.
- **Lane D — honest-zero:** the dormant-experiment rubric (ADR-023) parks
  pre-traffic experiments instead of marching them toward a kill they can't avoid.

## Lawfulness

- Version law: 8 published plugins bumped, each with plugin.json + record +
  CHANGELOG in sync (validator green); tags to be cut via release dispatch
  post-merge (TAGS-PENDING stays empty by design, ADR-020 path).
- Two-iteration rule: ADR-022 landed in the first commit; the `tools/` and
  `.github/workflows/` changes (C9/C11/C12/C13) landed in a later commit with
  that ADR as the prior-iteration record. charter/GROWTH.md's rubric change is
  covered by ADR-023.
- Three self-contradicting records surfaced while building — none papered over:
  pr-narrator/env-doctor/session-recap each claimed a component they didn't
  ship; each resolved to the truth (relabel) or to the value (build the hook).
- Append-only respected: JOURNAL, DECISIONS (ADR-022/023), this review, and the
  records' logs were appended, never rewritten. The one edit to a just-added
  line (ADR-022's header → `(i214, directed)`) was a format fix so the saga
  parser renders it, not a substance rewrite.

## Test posture at close

qa: 248 ok · 1 skip · 0 fail (up from 244 pre-slate — two new hook suites,
env-doctor 6 + session-recap 8). validate + build green; official `--strict`
smoke passes both new hooks.json; `node --check` on the worker. The tripwire
held: QA caught four real regressions mid-build (weekly-shipnote fixture missing
lib.py, a stale trust-card "skills-only" example after session-recap gained a
hook, the ADR-022 header format, the catalog self-version drift) — all fixed at
the source, not by loosening the test.

## Operator actions outstanding (unchanged)

1. The Claude secret (the only Gate A blocker).
2. Optional: budget var, GoatCounter, FUNDING handle.

## Verdict

v13: 14/14 built lawfully as a directed PR. The shelf no longer lies, the
flagship gate no longer cries wolf, the money path is hardened before the first
dollar, and the growth ledger is honest about a traffic count of zero.
