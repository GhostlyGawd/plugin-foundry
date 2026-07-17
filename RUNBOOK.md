# RUNBOOK — operator procedures for when the factory needs a human

Terse, do-this-now procedures. Each entry is earned by an incident; postmortems in
`reviews/postmortems/` carry the full story. The postmortem agent (MASTER P5.4)
appends deltas here.

## Hosted Codex API key rejected / missing  *(supersedes PM-001 for Actions)*
Symptom: the read-only Codex job fails authentication, or the trusted intake job
reports that `OPENAI_API_KEY` is unavailable.

Do:

1. Create or rotate a project-scoped OpenAI API key with the smallest practical budget.
2. Update the `OPENAI_API_KEY` Actions secret; never paste the value into an issue,
   pull request, workflow input, artifact, or log.
3. Dispatch one shift and confirm that the Codex job completes and the
   keyless landing job opens a validation pull request.
4. Remove the root `STOP` file in a reviewed pull request only after that dry run is green.

PM-001 remains the historical record of the retired hosted Claude OAuth setup.
`loop.sh` and `tools/auth.py` are an optional legacy local Claude harness; they are
not used by hosted Actions and their credentials must never be stored in this repo.

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
