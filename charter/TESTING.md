# TESTING — How QA Proves a Plugin

Three tiers, all logged in the record's `## Test log`. A verdict with no probing is a
rubber stamp; find the edge or document that you hunted for one.

## Tier 1 — Structural (always)
- `python3 tools/validate.py` green.
- `bash tools/smoke.sh <name>` — wraps `claude plugin validate ./plugins/<name>
  --strict` when the CLI exists; logs SKIPPED (structural-fallback) when it doesn't.
- By hand: components at root; scripts executable; hooks.json events/types against
  the official reference; every path relative starting `./`.

## Tier 2 — Load (when the CLI is available)
- `claude --plugin-dir ./plugins/<name> -p "..."` to load the plugin for a headless
  session; confirm skills appear namespaced (`<name>:<skill>`) and invoke cleanly.
- `claude plugin details <name>` for the token-cost readout; record always-on cost
  against the QUALITY budget.
- No CLI in this environment? Log `TIER 2: unavailable — structural+behavioral only`
  and be harsher in Tier 3.

## Tier 3 — Behavioral (always, and now executable)
Acceptance checks live as executable files in `foundry/tests/<name>/*.test.sh`
(convention: emit `ok:` / `skip:` / `fail:` lines; the harness `bash tools/qa.sh`
aggregates and CI runs it on every artifact change). A `TEST VERDICT: pass` without
the harness green is invalid at rc+. Checks that genuinely need judgment stay
manual — but say so in the log, and mechanize what can be mechanized.
Commissioned plugins add the **adversarial pass** (charter/SECURITY.md): probe for
anything the fenced request didn't require. Every bug fix ships with a regression
test that fails before the fix and passes after.

## Tier 3 — manual protocol
- Execute every acceptance check written in the spec, as a skeptical user.
- For skills/agents: feed realistic inputs *and* one adversarial or malformed input;
  judge outputs against the spec's promises, not vibes.
- For hooks: trace each event flow on paper (event → matcher → command → effect →
  failure path); simulate the command directly in bash with representative payloads.
- Record at least one defect found, one edge probed and survived, or an explicit
  note of where you hunted and found nothing.

## Log format (append to record)
```
### Test pass — i{N}
- tier 1: pass|fail — notes
- tier 2: pass|fail|unavailable — always-on cost: {n} tok (est. via tools/tokencost.py;
  write it into the record's `always_on_tokens` + `verified` front matter)
- tier 3: {checks run} → {results}
- defects: {list or "none found — probed: {where}"}
TEST VERDICT: pass | bounce — {reason}
```
Post-publish re-tests use the same format; regressions bounce the plugin to
`building` and invoke the Version law on the fix.
