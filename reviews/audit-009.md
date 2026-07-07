# Audit 009 — v14: finish the buildable line (i216)

Auditor pass closing v14 (ADR-024) — a directed PR that built everything the
line could still build without operator/world/community gating. Directed: "Build
all until fully complete."

## Outcome: buildable set complete, gated set honestly left open

- **Tenth plugin — todo-ledger**, walked idea → published in one directed pass:
  a `ledger` skill (grep TODO/FIXME/HACK/XXX → git-blame age + author → oldest-
  first ledger with a worst-offenders summary and copyable file:line refs).
  Read-only by default; dated report opt-in. Suite 9/9, official `--strict`, 108
  always-on tokens. The shelf is now ten plugins.
- **First Theme of the Month** (BRAND.md): July 2026 = "Repo hygiene", set by the
  designer via ADR-024. The three-candidate community vote is dormant until the
  window has traffic (ADR-023) — honest, not skipped. todo-ledger is the theme's
  first exhibit.
- **Bug fix** (bug lane): `build.py` mkdirs `site/` before writing into it — the
  crash the firstborn hit on a bare checkout. Verified by building in a copy with
  `site/` removed.
- **P3s:** the window countdown derives `(minute, hours)` from run-shift.yml's
  cron at build time instead of a hardcoded constant (drift fix); fork-a-foundry's
  from-spec bootstrap path links OPERATIONS §7–8 (v0.1.4).

## Lawfulness

- Version law: todo-ledger 0.1.0 (new, three-place sync + marketplace entry);
  night-clerk 0.2.6 and fork-a-foundry 0.1.4 bumped with CHANGELOGs. The catalog
  regeneration folded both shelf changes into the single night-clerk 0.2.6 bump
  (one directed iteration = one bump), avoiding a 0.2.6/0.2.7 stutter.
- Two-iteration rule: ADR-024 landed first; the `tools/` changes (build.py mkdir
  + countdown derivation) landed in a later commit with that ADR as the prior
  record.
- Nothing published without an executable `TEST VERDICT: pass` and a
  `REVIEW: approved` in the record — todo-ledger's record carries both, with the
  review scoring all six axes and probing the dating-honesty clause.
- Append-only respected: JOURNAL (i216), DECISIONS (ADR-024), this review, and
  every record log were appended, not rewritten.

## Test posture at close

qa: 257 ok · 1 skip · 0 fail (up from 248 — todo-ledger's 9-check suite).
validate (36 published) + build green; official `--strict` passes todo-ledger;
build-from-bare-checkout verified for the mkdir fix. The tripwire held: no QA
pass this batch found zero defects by luck — the new suite exercises real
behavior (git-grep fallback, blame honesty, read-only default).

## What remains open (gated, by construction)

- **Operator:** commission tiers wiring, GoatCounter.
- **World/community:** pr-gated-publishes CRON default (needs 10 mode:pr shifts),
  roadmap gates A (window live 14d + baselines), B (verdicts + first bug), C
  (community ships + first paid commission).

None of these can be closed by the line alone — they need a human, real traffic,
or real users. The buildable backlog is empty.

## Verdict

v14: the line built everything it could and stopped honestly at the gates it
can't cross. Ten plugins on the shelf, a theme on the window, a bug the firstborn
found now fixed, and a backlog whose only open items are someone else's to close.
