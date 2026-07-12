# DURABILITY — how the loop survives interruption (MASTER GAP-E, ADR-031)

MASTER GAP-E: *"a long autonomous loop needs to survive interruption — integrate
Inngest/Temporal **or** document journal-as-checkpoint."* This foundry already has
the durable-execution property by construction. This documents it, and names where
a heavier engine would slot in if the model ever outgrows it.

## The repo IS the state; git IS the checkpoint

There is no in-memory workflow state to lose. Everything the next iteration needs
is on disk, and every iteration ends in a single commit:

- **`state/STATE.json`** — the iteration counter and role queue. The resume point.
- **`state/JOURNAL.md`** — append-only; the last entry is where work stopped.
- **`state/DESK.jsonl`, `state/BUDGET.jsonl`, `state/METRICS.jsonl`** — append-only
  ledgers; a partial write is caught by `validate_state.py`, not silently trusted.
- **`git`** — the checkpoint boundary. One iteration = one commit (LOOP.md rule 1).

## What an interruption costs

A crash, a killed container, a lost token — the blast radius is **at most one
uncommitted iteration**, because:

1. `loop.sh` commits at the end of each pass; an interrupted pass leaves an
   uncommitted working tree that `git` discards or a human inspects — it never
   half-lands.
2. The belt-and-suspenders check in `loop.sh` re-runs `validate.py` after every
   pass and **halts on red**, so a corrupt state never rolls into the next pass.
3. On restart, the loop reads `STATE.json` + the journal tail and continues from
   the exact iteration number — no replay, no duplicate work, because the work
   product (the commit) is idempotent per iteration.

This is the journal-as-checkpoint pattern: the durable log (JOURNAL + git) is the
source of truth, and resume is "read the log, continue." The single-writer
orchestrator (P0.7) preserves it — one writer means one linear log to resume from,
never a partial multi-writer merge.

## Where Inngest / Temporal would slot in

The journal-as-checkpoint model is sufficient while writes are single-threaded and
each iteration is short (minutes). A heavier durable-execution engine earns its
place only if the model changes:

- **Long-running single steps** (an iteration that spans hours) → a step engine to
  checkpoint *within* an iteration, not just between them.
- **Cross-repo fan-out** (the network of forked foundries coordinating) → Temporal
  workflows for cross-process orchestration.
- **Exactly-once external side effects** (payments, third-party posts) → an engine's
  idempotency keys. Today those are all desk-gated and operator-executed, so the
  human is the durability boundary.

The seam is `loop.sh` + the orchestrator: both already resume from the repo, so
swapping the *driver* for a durable engine is a harness change, not a rewrite —
the same way the auth surface (AUTH-1) makes the credential swappable.

## The honest limit

This survives interruption; it does not survive **corruption of committed state**.
The defenses are `validate.py` + `validate_state.py` (a red repo halts the loop) and
git history (any bad commit is revertible with a note). That is the constitution's
append-only-history law doing double duty as the durability floor.
