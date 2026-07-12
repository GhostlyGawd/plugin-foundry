#!/usr/bin/env bash
# Quota governor v2 tests (MASTER P0.6, ADR-028): the §14 acceptance verbatim —
# "on a simulated near-limit day, low agents skip, then high, while product
# still executes; decisions are ledgered and visible in quota report."
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

FX="$WORK/fx"
mkdir -p "$FX/tools" "$FX/state" \
         "$FX/foundry/agents/foundry-loop" "$FX/foundry/agents/tripwire" \
         "$FX/foundry/agents/scout"
cp "$REPO"/tools/{lib.py,quota.py,desk.py} "$FX/tools/"
cat > "$FX/foundry/agents/foundry-loop/agent.json" <<'J'
{"id":"foundry-loop","role":"product","trigger":"schedule","trust_tier":"trusted","quota_tier":"product","capability":"writes:**","outputs":["plugins/"],"heartbeat":{"interval_hours":24}}
J
cat > "$FX/foundry/agents/tripwire/agent.json" <<'J'
{"id":"tripwire","role":"safety","trigger":"event","trust_tier":"trusted","quota_tier":"high","capability":"proposes","outputs":["reviews/"],"heartbeat":{"interval_hours":720}}
J
cat > "$FX/foundry/agents/scout/agent.json" <<'J'
{"id":"scout","role":"perception","trigger":"schedule","trust_tier":"ingests_untrusted","quota_tier":"low","capability":"read_only","outputs":["COMPETITIVE.md"],"heartbeat":{"interval_hours":168},"fenced":true}
J

export FOUNDRY_NOW="2026-07-12T12:00:00Z"
export QUOTA_WEEKLY_RUNS=10
unset LOOP_MONTHLY_BUDGET_USD || true

seed_runs() { # seed_runs <n> — n runs inside the window
  : > "$FX/state/BUDGET.jsonl"
  for _ in $(seq 1 "$1"); do
    printf '{"ts":"2026-07-12T01:00:00Z","kind":"quota_run","agent":"foundry-loop"}\n' >> "$FX/state/BUDGET.jsonl"
  done
  # one stale run outside the 168h window — must not count
  printf '{"ts":"2026-06-01T01:00:00Z","kind":"quota_run","agent":"foundry-loop"}\n' >> "$FX/state/BUDGET.jsonl"
}

Q() { (cd "$FX" && python3 tools/quota.py "$@" 2>&1); }

# 1 — low pressure: every tier goes
seed_runs 2
for a in foundry-loop tripwire scout; do
  out=$(Q check --agent "$a"); rc=$?
  [ "$rc" -eq 0 ] && echo "ok: p0.2 $a goes" || echo "fail: p0.2 $a — $out"
done

# 2 — pressure 0.7: low sheds, high + product go
seed_runs 7
out=$(Q check --agent scout); rc=$?
if [ "$rc" -eq 1 ] && echo "$out" | grep -q "SHED scout (low)"; then
  echo "ok: p0.7 low sheds"; else echo "fail: p0.7 low — $out"; fi
out=$(Q check --agent tripwire); rc=$?
[ "$rc" -eq 0 ] && echo "ok: p0.7 high still goes" || echo "fail: p0.7 high — $out"
out=$(Q check --agent foundry-loop); rc=$?
[ "$rc" -eq 0 ] && echo "ok: p0.7 product still goes" || echo "fail: p0.7 product — $out"

# 3 — pressure 0.9: high sheds too, product still goes
seed_runs 9
out=$(Q check --agent tripwire); rc=$?
if [ "$rc" -eq 1 ] && echo "$out" | grep -q "SHED tripwire (high)"; then
  echo "ok: p0.9 high sheds"; else echo "fail: p0.9 high — $out"; fi
out=$(Q check --agent foundry-loop); rc=$?
[ "$rc" -eq 0 ] && echo "ok: p0.9 product STILL goes (never shed on pressure)" \
                || echo "fail: p0.9 product — $out"

# 4 — kill switch: pressure ≥ 1.0 pauses product TO THE DESK
seed_runs 11
out=$(Q check --agent foundry-loop); rc=$?
if [ "$rc" -eq 1 ] && echo "$out" | grep -q "desk item d-"; then
  echo "ok: kill switch pauses product to the desk"
else echo "fail: kill switch — $out"; fi
grep -q '"kind": "quota_halt"' "$FX/state/BUDGET.jsonl" \
  && echo "ok: halt ledgered" || echo "fail: halt not ledgered"
out=$(Q check --agent foundry-loop)
echo "$out" | grep -q "already open" \
  && echo "ok: kill-switch desk item dedups" || echo "fail: desk dedup — $out"

# 5 — decisions visible in report (shed scout on this ledger first)
Q check --agent scout >/dev/null
out=$(Q report)
if echo "$out" | grep -q "quota_shed scout" && echo "$out" | grep -q "quota_halt foundry-loop" \
   && echo "$out" | grep -q "pressure 1.10"; then
  echo "ok: report shows pressure + ledgered decisions"
else echo "fail: report — $out"; fi

# 6 — dollar path is absolute (ADR-008): cap spent halts every tier
seed_runs 1
printf '{"ts":"2026-07-10T01:00:00Z","cost_usd":6.0,"usage":{}}\n' >> "$FX/state/BUDGET.jsonl"
out=$(cd "$FX" && LOOP_MONTHLY_BUDGET_USD=5 python3 tools/quota.py check --agent foundry-loop 2>&1); rc=$?
if [ "$rc" -eq 1 ] && echo "$out" | grep -q "ADR-008"; then
  echo "ok: dollar cap halts product too"
else echo "fail: dollar cap — rc=$rc $out"; fi

# 7 — unknown agent fails closed
out=$(Q check --agent ghost); rc=$?
if [ "$rc" -eq 1 ] && echo "$out" | grep -q "fail closed"; then
  echo "ok: unknown agent fails closed"
else echo "fail: unknown agent — $out"; fi

# 8 — legacy loop ledger lines count as runs (cost_usd entries)
: > "$FX/state/BUDGET.jsonl"
for _ in 1 2 3 4 5 6 7; do
  printf '{"ts":"2026-07-12T01:00:00Z","cost_usd":null,"usage":null}\n' >> "$FX/state/BUDGET.jsonl"
done
out=$(Q check --agent scout); rc=$?
if [ "$rc" -eq 1 ] && echo "$out" | grep -q "SHED scout"; then
  echo "ok: legacy ledger lines count toward the window"
else echo "fail: legacy lines — $out"; fi
