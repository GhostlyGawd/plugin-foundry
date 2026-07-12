#!/usr/bin/env bash
# Agent-ops tests (MASTER P0.3/P0.4/P0.9, ADR-026): identity, shared-state
# validation, and liveness. Each rail is proven to fire, not just to exist.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# ---------- Part A — validate_state.py (P0.4) ----------

# A0 — the real repo's shared state is well-formed
out=$(cd "$REPO" && python3 tools/validate_state.py 2>&1); rc=$?
[ "$rc" -eq 0 ] && echo "ok: A0 real repo state validates" \
                || echo "fail: A0 real repo state — $out"

mkfx() { # minimal state fixture with lawful STATE.json + agents dir
  FX="$WORK/$1"; rm -rf "$FX"
  mkdir -p "$FX/tools" "$FX/state" "$FX/foundry/agents/reader"
  cp "$REPO"/tools/{lib.py,validate_state.py} "$FX/tools/"
  cat > "$FX/state/STATE.json" <<'J'
{"schema_version":1,"codename":"fx","name":"Fixture","iteration":1,"phase":"grow","role_queue":["builder"],"notes":"fixture"}
J
  cat > "$FX/foundry/agents/reader/agent.json" <<'J'
{"id":"reader","role":"reads","trigger":"schedule","trust_tier":"trusted","quota_tier":"low","capability":"read_only","outputs":["x"],"heartbeat":{"interval_hours":24}}
J
  cat > "$FX/foundry/agents/identities.json" <<'J'
{"reader":{"name":"fx reader","email":"reader@fx.invalid"}}
J
  ( cd "$FX" && python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
from lib import build_agent_registry
build_agent_registry(".")
PY
  )
}

VS() { (cd "$FX" && python3 tools/validate_state.py 2>&1); }

# A1 — baseline fixture green
mkfx a1
out=$(VS); rc=$?
[ "$rc" -eq 0 ] && echo "ok: A1 state fixture baseline green" \
                || echo "fail: A1 baseline red — $out"

# A2 — malformed METRICS.jsonl line is caught with line number
mkfx a2
printf '{"ts":"2026-07-12T00:00:00Z","stars":0}\n{oops}\n' > "$FX/state/METRICS.jsonl"
out=$(VS); rc=$?
if [ "$rc" -ne 0 ] && echo "$out" | grep -q "METRICS.jsonl:2"; then
  echo "ok: A2 malformed METRICS line caught at its line"
else echo "fail: A2 — $out"; fi

# A3 — bad DESK entry is caught
mkfx a3
printf '{"id":"nope","ts":"t"}\n' > "$FX/state/DESK.jsonl"
out=$(VS); rc=$?
if [ "$rc" -ne 0 ] && echo "$out" | grep -q "DESK.jsonl:1.*d-"; then
  echo "ok: A3 bad desk id caught"
else echo "fail: A3 — $out"; fi

# A4 — broken verified.json is caught
mkfx a4
mkdir -p "$FX/foundry"; printf '{"verified":"yes"}\n' > "$FX/foundry/verified.json"
out=$(VS); rc=$?
if [ "$rc" -ne 0 ] && echo "$out" | grep -q "verified.*list"; then
  echo "ok: A4 broken verified.json caught"
else echo "fail: A4 — $out"; fi

# A5 — agent without identity is caught (P0.3 ∩ P0.4)
mkfx a5
printf '{}\n' > "$FX/foundry/agents/identities.json"
out=$(VS); rc=$?
if [ "$rc" -ne 0 ] && echo "$out" | grep -q "no identity for 'reader'"; then
  echo "ok: A5 registry⊆identities enforced"
else echo "fail: A5 — $out"; fi

# A6 — stray metrics string where number-or-null belongs
mkfx a6
printf '{"ts":"2026-07-12T00:00:00Z","stars":"many"}\n' > "$FX/state/METRICS.jsonl"
out=$(VS); rc=$?
if [ "$rc" -ne 0 ] && echo "$out" | grep -q "honest-null"; then
  echo "ok: A6 non-numeric metric caught (honest-null law)"
else echo "fail: A6 — $out"; fi

# ---------- Part B — commit.py + the trailer law (P0.3) ----------

GFX="$WORK/gitfx"
python3 "$HERE/fixture.py" "$GFX"
mkdir -p "$GFX/foundry/agents/foundry-loop"
cat > "$GFX/foundry/agents/foundry-loop/agent.json" <<'J'
{"id":"foundry-loop","role":"loop","trigger":"schedule","trust_tier":"trusted","quota_tier":"product","capability":"writes:**","outputs":["plugins/"],"heartbeat":{"interval_hours":24}}
J
cat > "$GFX/foundry/agents/identities.json" <<'J'
{"foundry-loop":{"name":"fx loop","email":"foundry-loop@fx.invalid"}}
J
( cd "$GFX" && python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
from lib import build_agent_registry
build_agent_registry(".")
PY
)
git -C "$GFX" init -q
git -C "$GFX" -c user.name=op -c user.email=op@fx.invalid add -A
git -C "$GFX" -c user.name=op -c user.email=op@fx.invalid commit -qm "genesis"

# B1 — a raw commit under an agent identity WITHOUT the trailer fails validate
echo x >> "$GFX/README-op.md"
git -C "$GFX" add -A
git -C "$GFX" -c user.name="fx loop" -c user.email="foundry-loop@fx.invalid" \
  commit -qm "sneaky untrailed commit"
out=$(cd "$GFX" && python3 tools/validate.py 2>&1); rc=$?
if [ "$rc" -ne 0 ] && echo "$out" | grep -q "lacks its 'Agent: foundry-loop' trailer"; then
  echo "ok: B1 untrailed agent commit fails the gate"
else echo "fail: B1 — rc=$rc $out"; fi

# B2 — commit.py commits with author + trailer, and the gate passes
echo y >> "$GFX/README-op.md"
out=$(cd "$GFX" && python3 tools/commit.py --agent foundry-loop --add-all \
      -m "loop(fx): lawful commit" 2>&1); rc=$?
log=$(git -C "$GFX" log -1 --format='%an|%ae|%B')
if [ "$rc" -eq 0 ] && echo "$log" | grep -q '^fx loop|foundry-loop@fx.invalid' \
   && echo "$log" | grep -q 'Agent: foundry-loop'; then
  echo "ok: B2 commit.py stamps author + Agent trailer"
else echo "fail: B2 — rc=$rc log=$log"; fi
out=$(cd "$GFX" && python3 tools/validate.py 2>&1); rc=$?
[ "$rc" -eq 0 ] && echo "ok: B3 trailed agent commit passes the gate" \
                || echo "fail: B3 — $out"

# B4 — unknown agent: no manifest, no pen
out=$(cd "$GFX" && python3 tools/commit.py --agent ghost -m x 2>&1); rc=$?
if [ "$rc" -ne 0 ] && echo "$out" | grep -q "no manifest, no pen"; then
  echo "ok: B4 unknown agent refused"
else echo "fail: B4 — $out"; fi

# ---------- Part C — heartbeat.py (P0.9) ----------

HFX="$WORK/hfx"
mkdir -p "$HFX/tools" "$HFX/foundry/agents/reader" "$HFX/foundry/agents/sleeper"
cp "$REPO"/tools/{lib.py,heartbeat.py,alarm.py} "$HFX/tools/"
cat > "$HFX/foundry/agents/reader/agent.json" <<'J'
{"id":"reader","role":"reads","trigger":"schedule","trust_tier":"trusted","quota_tier":"low","capability":"read_only","outputs":["x"],"heartbeat":{"interval_hours":24},"status":"active"}
J
cat > "$HFX/foundry/agents/sleeper/agent.json" <<'J'
{"id":"sleeper","role":"paused","trigger":"schedule","trust_tier":"trusted","quota_tier":"low","capability":"read_only","outputs":["x"],"heartbeat":{"interval_hours":1},"status":"dormant"}
J

# C1 — unknown agent cannot beat
out=$(cd "$HFX" && python3 tools/heartbeat.py beat ghost 2>&1); rc=$?
[ "$rc" -ne 0 ] && echo "ok: C1 unknown agent cannot beat" \
                || echo "fail: C1 — $out"

# C2 — beat then fresh check is green; dormant agent exempt despite no beat
(cd "$HFX" && python3 tools/heartbeat.py beat reader --note fx >/dev/null)
out=$(cd "$HFX" && python3 tools/heartbeat.py check 2>&1); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q "dormant exempt"; then
  echo "ok: C2 fresh beat green; dormant exempt"
else echo "fail: C2 — rc=$rc $out"; fi

# C3 — a stale beat is called out by name (clock injected)
out=$(cd "$HFX" && FOUNDRY_NOW="2036-01-01T00:00:00Z" python3 tools/heartbeat.py check 2>&1); rc=$?
if [ "$rc" -eq 2 ] && echo "$out" | grep -q "STALE reader"; then
  echo "ok: C3 stale agent named (exit 2)"
else echo "fail: C3 — rc=$rc $out"; fi

# C4 — a never-beaten ACTIVE agent is stale immediately
rm -f "$HFX/foundry/agents/heartbeats.json"
out=$(cd "$HFX" && python3 tools/heartbeat.py check 2>&1); rc=$?
if [ "$rc" -eq 2 ] && echo "$out" | grep -q "no heartbeat ever recorded"; then
  echo "ok: C4 never-beaten active agent is stale"
else echo "fail: C4 — rc=$rc $out"; fi
