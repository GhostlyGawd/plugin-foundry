#!/usr/bin/env bash
# Orchestrator tests (MASTER P0.7, ADR-026): the §14 acceptance — conflicting
# edits resolve deterministically by precedence (loser re-queues), guard and
# gate vetoes are honored, landings are attributed, the repo never stays red.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

FX="$WORK/fx"
python3 "$HERE/fixture.py" "$FX"
# the orchestrator's gates include validate_state + build: give the fixture a
# lawful STATE.json and the site-config build.py expects
cat > "$FX/state/STATE.json" <<'J'
{"schema_version":1,"codename":"fx","name":"Fixture","iteration":1,"phase":"grow","role_queue":["builder"],"notes":"fx"}
J
printf '{}\n' > "$FX/foundry/site-config.json"
printf '## i1 — builder — 2026-07-12T00:00:00Z\n- did: fixture genesis.\n' > "$FX/state/JOURNAL.md"
printf '## ADR-001 — fixture\n- Status: accepted\n' > "$FX/state/DECISIONS.md"
printf '{"ts":"2026-07-12T00:00:00Z","stars":0}\n' > "$FX/state/METRICS.jsonl"
printf '{"ts":"2026-07-12T00:00:00Z","cost_usd":null}\n' > "$FX/state/BUDGET.jsonl"
printf '{}\n' > "$FX/foundry/reports.json"
printf '{"kits":[]}\n' > "$FX/foundry/kits.json"
printf '[]\n' > "$FX/foundry/alarms.json"
printf '{"network":[]}\n' > "$FX/foundry/network.json"
printf '{"verified":[]}\n' > "$FX/foundry/verified.json"
printf '{}\n' > "$FX/foundry/votes.json"

mkA() { # mkA <id> <tier> <cap> [extra-json]
  mkdir -p "$FX/foundry/agents/$1"
  printf '{"id":"%s","role":"fx","trigger":"schedule","trust_tier":"trusted","quota_tier":"%s","capability":"%s","outputs":["x"],"heartbeat":{"interval_hours":24}%s}\n' \
    "$1" "$2" "$3" "${4:-}" > "$FX/foundry/agents/$1/agent.json"
}
mkA orchestrator product "writes:**"
mkA foundry-loop product "writes:**"
mkA briefing high "writes:state/notes/**" ',"lands_via":"orchestrator","gates":["guard","validate_state"]'
mkA shipnote low "writes:state/notes/**" ',"lands_via":"orchestrator","gates":["guard","validate_state"]'
cat > "$FX/foundry/agents/identities.json" <<'J'
{"orchestrator":{"name":"fx orchestrator","email":"orchestrator@fx.invalid"},
 "foundry-loop":{"name":"fx loop","email":"loop@fx.invalid"},
 "briefing":{"name":"fx briefing","email":"briefing@fx.invalid"},
 "shipnote":{"name":"fx shipnote","email":"shipnote@fx.invalid"}}
J
( cd "$FX" && python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
from lib import build_agent_registry
n, errs = build_agent_registry(".")
assert not errs, errs
PY
)
git -C "$FX" init -q
git -C "$FX" -c user.name=op -c user.email=op@fx.invalid add -A
git -C "$FX" -c user.name=op -c user.email=op@fx.invalid commit -qm genesis

CS() { # CS <agent> <cid> <ts> <rationale> <path> <action> [content]
  local a="$1" c="$2" ts="$3" why="$4" p="$5" act="$6" body="${7:-}"
  local d="$FX/foundry/agents/outbox/$a/$c"
  mkdir -p "$d"
  printf '{"id":"%s","agent":"%s","ts":"%s","rationale":"%s","changes":[{"path":"%s","action":"%s"}]}\n' \
    "$c" "$a" "$ts" "$why" "$p" "$act" > "$d/changeset.json"
  if [ "$act" != "delete" ]; then
    mkdir -p "$d/files/$(dirname "$p")"
    printf '%s\n' "$body" > "$d/files/$p"
  fi
}

O() { OUT=$(cd "$FX" && python3 tools/orchestrator.py run --no-beat 2>&1); ORC=$?; }

# 1 — a lawful changeset lands, attributed to its agent, outbox consumed
CS briefing cs-001 2026-07-12T01:00:00Z "morning brief" "state/notes/brief.md" add "The line is quiet."
O
log=$(git -C "$FX" log -1 --format='%an|%ae|%B')
if [ "$ORC" -eq 0 ] && [ -f "$FX/state/notes/brief.md" ] \
   && echo "$log" | grep -q '^fx briefing|briefing@fx.invalid' \
   && echo "$log" | grep -q 'Agent: briefing' \
   && [ ! -d "$FX/foundry/agents/outbox/briefing/cs-001" ]; then
  echo "ok: lawful changeset lands, attributed, outbox consumed"
else echo "fail: land — rc=$ORC out=$OUT log=$log"; fi

# 2 — conflict: higher precedence lands, loser DEFERS in place
CS briefing cs-002 2026-07-12T02:00:00Z "own the note" "state/notes/today.md" add "high tier content"
CS shipnote cs-003 2026-07-12T01:30:00Z "also wants it" "state/notes/today.md" add "low tier content"
O
if grep -q "high tier content" "$FX/state/notes/today.md" \
   && [ -d "$FX/foundry/agents/outbox/shipnote/cs-003" ] \
   && echo "$OUT" | grep -q "DEFER shipnote/cs-003"; then
  echo "ok: precedence wins the conflict; loser re-queues in place"
else echo "fail: conflict — $OUT"; fi
# the deferred one lands cleanly next run (conflict is per-run, not forever)…
O
if grep -q "low tier content" "$FX/state/notes/today.md"; then
  echo "ok: deferred changeset lands on the NEXT run (re-queue works)"
else echo "fail: re-queue — $OUT"; fi

# 3 — guard block: deleting a record is rejected with the verdict on file
CS foundry-loop cs-004 2026-07-12T03:00:00Z "tidy up" "foundry/records/demo-plug.md" delete
O
rej="$FX/foundry/agents/outbox/foundry-loop/rejected-cs-004"
if [ -f "$FX/foundry/records/demo-plug.md" ] && [ -f "$rej/verdict.txt" ] \
   && grep -q "Article I §2" "$rej/verdict.txt"; then
  echo "ok: guard block honored — record survives, verdict filed"
else echo "fail: guard block — $OUT"; fi

# 4 — desk flow: law-book edit held → operator approves → lands next run
CS briefing cs-005 2026-07-12T04:00:00Z "annotate the law" "tools/validate.py" modify \
   "$(cat "$FX/tools/validate.py"; echo '# fx: operator-ratified annotation')"
O
if [ -f "$FX/foundry/agents/outbox/briefing/cs-005/.held" ] \
   && grep -q '"kind": "ratify"' "$FX/state/DESK.jsonl"; then
  echo "ok: law-book edit HELD with a desk item"
else echo "fail: desk hold — $OUT"; fi
did=$(cd "$FX" && python3 -c "
import sys; sys.path.insert(0,'tools'); import desk
items = desk.read_items('state/DESK.jsonl')
print(next(i for i,it in items.items() if it.get('status')=='open'))")
(cd "$FX" && python3 tools/desk.py resolve "$did" approved --note "ratified in fx")
O
if grep -q "fx: operator-ratified annotation" "$FX/tools/validate.py" \
   && [ ! -d "$FX/foundry/agents/outbox/briefing/cs-005" ]; then
  echo "ok: desk approval lands the held changeset"
else echo "fail: desk approval — $OUT"; fi

# 5 — desk rejection retires a held changeset
CS briefing cs-006 2026-07-12T05:00:00Z "another law edit" "LOOP.md" modify "not the law anymore"
O
did=$(cd "$FX" && python3 -c "
import sys; sys.path.insert(0,'tools'); import desk
items = desk.read_items('state/DESK.jsonl')
print(next(i for i,it in items.items() if it.get('status')=='open'))")
(cd "$FX" && python3 tools/desk.py resolve "$did" rejected --note "no")
O
if [ -d "$FX/foundry/agents/outbox/briefing/rejected-cs-006" ] \
   && ! grep -q "not the law anymore" "$FX/LOOP.md" 2>/dev/null; then
  echo "ok: desk rejection retires the changeset"
else echo "fail: desk rejection — $OUT"; fi

# 6 — gate failure: a record-breaking changeset is reverted byte-for-byte
before=$(cat "$FX/foundry/records/demo-plug.md")
CS foundry-loop cs-007 2026-07-12T06:00:00Z "break the record" "foundry/records/demo-plug.md" modify "no front matter at all"
O
after=$(cat "$FX/foundry/records/demo-plug.md")
rej="$FX/foundry/agents/outbox/foundry-loop/rejected-cs-007"
if [ "$before" = "$after" ] && [ -f "$rej/verdict.txt" ] \
   && grep -q "gate 'validate' failed" "$rej/verdict.txt" \
   && (cd "$FX" && python3 tools/validate.py >/dev/null 2>&1); then
  echo "ok: red gate reverts byte-for-byte; repo stays green"
else echo "fail: gate revert — $OUT"; fi

# 7 — empty outbox: a clean quiet run
O
if [ "$ORC" -eq 0 ] && echo "$OUT" | grep -q "landed 0"; then
  echo "ok: empty outbox is a clean no-op"
else echo "fail: empty outbox — rc=$ORC $OUT"; fi
