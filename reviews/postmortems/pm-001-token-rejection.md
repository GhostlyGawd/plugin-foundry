# PM-001 — the silent token rejection (2026-07-07)

*The foundry's first postmortem. Blameless: the failure was a system property —
a fail-soft loop plus a gitignored error stream — not anyone's mistake. Seeded by
the program (MASTER P5.4) from the real journal record; future postmortems are
written by the postmortem agent on the same template.*

## Summary
On the first live CI shift, the `CLAUDE_CODE_OAUTH_TOKEN` secret was present but
its value was rejected. `claude` exited nonzero ~3 seconds into pass 1/1 — an
authentication failure, not real work. The shift's PR carried only a
metrics-heartbeat line. Blast radius: one no-op shift and a false green. Duration:
caught the same day and re-paused.

## Timeline
- **2026-07-07T16:04Z** — operator configured the secret; the root `STOP` file was
  removed so shifts could run.
- **~16:20Z** — dispatch run #7 (mode:pr, 1 iteration) reached the loop; `claude`
  exited nonzero ~3s in with `loop.sh: claude exited nonzero (streak: 1)`.
- **16:26Z** — re-paused: `STOP` re-added; a fail-soft `if: always()` diagnostic
  step added to `run-shift.yml` that tails `state/runs/*.{err,json}`.

## Why it looked fine (the load-bearing section)
Two mechanisms combined to hide a total failure behind a green-looking run:
1. **`loop.sh` is fail-soft** — it halts only after a 3-failure streak, so a single
   rejected pass looks like an ordinary transient.
2. **The real error went to a gitignored, ephemeral stream.** In CI/JSON mode
   `claude` writes its error to `<log>.json` (stdout) while `loop.sh` printed only
   `<log>.err` (stderr), and `state/runs/` is gitignored — so the precise cause
   (`OAuth token … rejected`) never surfaced in the Actions log or the repo.

Together: a failed shift that reports success silently. A shift that *announces* its
failure is easy; this one didn't.

## Root cause
Not "the token was wrong" (that's the trigger). The system property: **an
auth-shaped failure was indistinguishable from a transient, and its evidence was
routed somewhere no human would look.** The loop had no notion of "this failure is
terminal, stop now and say why."

## The fix
- **Immediate (2026-07-07):** the `if: always()` diagnostic step surfaces the
  masked run logs on the next failure.
- **Structural (AUTH-1, ADR-031, i223):** `tools/auth.py` is now the single auth
  surface; `auth.py probe` classifies a run log as auth-shaped, and `loop.sh` halts
  on the **first** auth failure with the remedy instead of streaking. In CI with no
  usable credential, the shift now fails **loudly** rather than no-opping. The exact
  silence that produced PM-001 is closed.

## Runbook delta
See `RUNBOOK.md` → "CI token rejected / expired." In short: `claude setup-token` on
a subscription machine → update the `CLAUDE_CODE_OAUTH_TOKEN` secret → dispatch one
shift → delete `STOP`. `auth.py`'s remedy prints this on any auth failure.

## Lesson
A fail-soft loop that routes its errors to a gitignored stream will report success
while doing nothing — classify terminal failures and halt loudly on the first one.
(Added to `tools/memory.py` as m-001.)
