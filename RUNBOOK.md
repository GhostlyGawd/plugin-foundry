# RUNBOOK — operator procedures for when the factory needs a human

Terse, do-this-now procedures. Each entry is earned by an incident; postmortems in
`reviews/postmortems/` carry the full story. The postmortem agent (MASTER P5.4)
appends deltas here.

## A model workflow or headless runner was enabled
Symptom: a GitHub workflow, scheduler, background service, `codex exec`, or
`claude -p` attempts to invoke a model.

Do:

1. Cancel the run and disable the model workflow or scheduler.
2. Confirm `run-shift.yml` and `record-demos.yml` are inert and schedule-free.
3. Remove any model credential from GitHub without printing or copying its value.
4. Reopen the repository in an attended interactive coding-agent session and
   submit any intended change through a pull request.

PM-001 remains the historical record of the 2026-07-07 token rejection. ADR-032
supersedes its provisioning remedy: no reusable model credential belongs in GitHub.
`tools/auth.py probe` still classifies old logs but directs recovery to an attended
local session.

## Governor / quota halt
Symptom: `budget.py`/`quota.py` halts a shift; an `ops-alarm` opens.
Do: treat the entry as historical while ADR-032 is active; no unattended model run
should be consuming a budget. If an active runner produced it, follow the procedure
above and disable that runner.

## The owner's desk has items
Symptom: `site/desk.html` / the pinned `ops-desk` issue lists open decisions.
Do: `python3 tools/desk.py queue` to see them ranked; resolve with
`python3 tools/desk.py resolve <id> approved|rejected --note "…"`. The orchestrator
lands approvals on its next run. Nothing requiring approval auto-merges.

## A stale agent alarm fired
Symptom: `ops-alarm: agent '<id>' heartbeat stale`.
Do: check that agent's workflow ran; inspect `foundry/agents/heartbeats.json`. A
dormant agent is exempt — if it's meant to be paused, set `status: "dormant"` in its
manifest. Otherwise re-enable its schedule.
