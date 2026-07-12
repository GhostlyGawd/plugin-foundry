#!/usr/bin/env bash
# Agent-contract tests (MASTER.md P0.1, ADR-026): the loader in tools/lib.py is
# what makes charter/AGENTS.md enforceable — prove the schema loads a lawful
# manifest and that each of the four hard rules actually fires.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

FX="$WORK/fx"
mkdir -p "$FX/tools" "$FX/foundry/agents/scout"
cp "$REPO/tools/lib.py" "$FX/tools/"

mk() { # mk <json> — write the scout manifest
  printf '%s\n' "$1" > "$FX/foundry/agents/scout/agent.json"
}

check() { # check <label> <expect: ok|err> <grep-pattern-when-err>
  local label="$1" expect="$2" pat="${3:-}"
  local out rc
  out=$(cd "$FX" && python3 - <<'PY' 2>&1
import sys
sys.path.insert(0, "tools")
from lib import load_agents
errors = []
agents = load_agents(errors)
for e in errors:
    print("ERR", e)
print("LOADED", len(agents))
PY
); rc=$?
  if [ "$expect" = ok ]; then
    if [ "$rc" -eq 0 ] && echo "$out" | grep -q "LOADED 1" && ! echo "$out" | grep -q '^ERR'; then
      echo "ok: $label"
    else
      echo "fail: $label — $out"
    fi
  else
    if echo "$out" | grep -q "ERR.*$pat"; then
      echo "ok: $label"
    else
      echo "fail: $label — wanted /$pat/, got: $out"
    fi
  fi
}

BASE='{"id":"scout","role":"reads the ecosystem","trigger":"schedule","trust_tier":"ingests_untrusted","quota_tier":"low","capability":"read_only","outputs":["COMPETITIVE.md"],"heartbeat":{"interval_hours":168},"fenced":true}'

# 1 — a lawful manifest loads
mk "$BASE"
check "lawful ingests_untrusted read_only manifest loads" ok

# 2 — hard rule 1: writes: without lands_via orchestrator
mk '{"id":"scout","role":"r","trigger":"schedule","trust_tier":"trusted","quota_tier":"low","capability":"writes:state/**","outputs":["state/"],"heartbeat":{"interval_hours":24},"gates":["guard","validate_state"]}'
check "hard rule 1 fires (writes: needs lands_via orchestrator)" err "hard rule 1"

# 3 — hard rule 2a: untrusted ingestion may not hold a pen
mk '{"id":"scout","role":"r","trigger":"schedule","trust_tier":"ingests_untrusted","quota_tier":"low","capability":"writes:state/**","outputs":["state/"],"heartbeat":{"interval_hours":24},"fenced":true,"lands_via":"orchestrator","gates":["guard","validate_state"]}'
check "hard rule 2 fires (read/act split)" err "hard rule 2"

# 4 — hard rule 2b: untrusted ingestion must be fenced
mk '{"id":"scout","role":"r","trigger":"schedule","trust_tier":"ingests_untrusted","quota_tier":"low","capability":"read_only","outputs":["x"],"heartbeat":{"interval_hours":24}}'
check "hard rule 2 fires (unfenced untrusted ingestion)" err "fenced: true"

# 5 — hard rule 3: writes: without guard clearance
mk '{"id":"scout","role":"r","trigger":"schedule","trust_tier":"trusted","quota_tier":"high","capability":"writes:state/**","outputs":["state/"],"heartbeat":{"interval_hours":24},"lands_via":"orchestrator"}'
check "hard rule 3 fires (writes: without guard+validate_state gates)" err "hard rule 3"

# 6 — schema: unknown field rejected (closed schema)
mk '{"id":"scout","role":"r","trigger":"schedule","trust_tier":"trusted","quota_tier":"low","capability":"read_only","outputs":["x"],"heartbeat":{"interval_hours":24},"surprise":1}'
check "closed schema rejects unknown fields" err "unknown field"

# 7 — schema: bad enum rejected
mk '{"id":"scout","role":"r","trigger":"sometimes","trust_tier":"trusted","quota_tier":"low","capability":"read_only","outputs":["x"],"heartbeat":{"interval_hours":24}}'
check "bad trigger enum rejected" err "trigger"

# 8 — id/directory mismatch rejected
mk '{"id":"not-scout","role":"r","trigger":"schedule","trust_tier":"trusted","quota_tier":"low","capability":"read_only","outputs":["x"],"heartbeat":{"interval_hours":24}}'
check "id != directory rejected" err "directory"

# 9 — the real repo's manifests + registry are lawful and fresh
out=$(cd "$REPO" && python3 - <<'PY' 2>&1
import sys, json
sys.path.insert(0, "tools")
from lib import load_agents
errors = []
agents = load_agents(errors)
for e in errors:
    print("ERR", e)
reg = json.load(open("foundry/agents/registry.json"))
ids_disk = [a["id"] for a in agents]
ids_reg = [a["id"] for a in reg.get("agents", [])]
print("MATCH" if ids_disk == ids_reg and len(ids_disk) >= 1 else
      f"DRIFT disk={ids_disk} registry={ids_reg}")
PY
)
if echo "$out" | grep -q '^MATCH' && ! echo "$out" | grep -q '^ERR'; then
  echo "ok: repo manifests lawful; registry.json in sync"
else
  echo "fail: repo manifests/registry — $out"
fi
