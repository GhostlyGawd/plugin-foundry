# RUNBOOK — operator procedures for when the factory needs a human

Terse, do-this-now procedures. Each entry is earned by an incident; postmortems in
`reviews/postmortems/` carry the full story. The postmortem agent (MASTER P5.4)
appends deltas here.

## CI token rejected / expired  *(PM-001)*
Symptom: shifts no-op or fail ~3s in; `auth.py probe` classifies an auth failure;
or `loop.sh` halts with "AUTH FAILURE." The window may show an `ops-alarm`.
Do:
1. On a machine logged into an active Claude subscription: `claude setup-token`.
2. Update the `CLAUDE_CODE_OAUTH_TOKEN` Actions secret with the **full** value.
3. Dispatch one shift (mode:pr for a veto window) to confirm it authenticates.
4. Delete the root `STOP` file to resume the schedule.
Or migrate to API billing (any of the four triggers in `OPERATIONS.md §9`): set
`ANTHROPIC_API_KEY`, remove the OAuth secret — no code change (`tools/auth.py` is
the only auth surface).

## Governor / quota halt
Symptom: `budget.py`/`quota.py` halts a shift; an `ops-alarm` opens.
Do: check `state/BUDGET.jsonl`. If the monthly dollar cap is spent, raise
`LOOP_MONTHLY_BUDGET_USD` or wait for the month to roll. If quota pressure hit the
kill switch, the desk holds an `approve` item — raise `QUOTA_WEEKLY_RUNS` or wait
for the weekly window to roll. Product-tier work never sheds on pressure by design.

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
