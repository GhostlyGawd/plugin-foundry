#!/usr/bin/env bash
# Guard tests (MASTER P0.5, ADR-027): the constitution is only as real as the
# code that enforces it. Fixture foundry + manifests; prove allow/desk/block
# each fire, the desk queue receives ratification items, and dedup holds.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

FX="$WORK/fx"
mkdir -p "$FX/tools" "$FX/state" \
         "$FX/foundry/agents/foundry-loop" "$FX/foundry/agents/scout" \
         "$FX/foundry/agents/postmortem" "$FX/foundry/agents/briefing"
cp "$REPO"/tools/lib.py "$REPO"/tools/guard.py "$REPO"/tools/desk.py "$FX/tools/"

cat > "$FX/foundry/agents/foundry-loop/agent.json" <<'J'
{"id":"foundry-loop","role":"product loop","trigger":"schedule","trust_tier":"trusted",
 "quota_tier":"product","capability":"writes:**","outputs":["plugins/"],
 "heartbeat":{"interval_hours":24}}
J
cat > "$FX/foundry/agents/scout/agent.json" <<'J'
{"id":"scout","role":"reads the ecosystem","trigger":"schedule","trust_tier":"ingests_untrusted",
 "quota_tier":"low","capability":"read_only","outputs":["COMPETITIVE.md"],
 "heartbeat":{"interval_hours":168},"fenced":true}
J
cat > "$FX/foundry/agents/postmortem/agent.json" <<'J'
{"id":"postmortem","role":"writes blameless postmortems","trigger":"event","trust_tier":"trusted",
 "quota_tier":"high","capability":"proposes","outputs":["reviews/postmortems/"],
 "heartbeat":{"interval_hours":720}}
J
cat > "$FX/foundry/agents/briefing/agent.json" <<'J'
{"id":"briefing","role":"per-shift briefing","trigger":"schedule","trust_tier":"trusted",
 "quota_tier":"low","capability":"writes:state/briefings/**","outputs":["state/briefings/"],
 "heartbeat":{"interval_hours":24},"lands_via":"orchestrator","gates":["guard","validate_state"]}
J

G() { # G <agent> <changes-json> [--queue] → sets OUT and RC
  local agent="$1" changes="$2"; shift 2
  OUT=$(cd "$FX" && printf '%s' "$changes" | python3 tools/guard.py --agent "$agent" --changes - "$@" 2>&1); RC=$?
}

case_rc() { # case_rc <label> <want-rc> <grep>
  local label="$1" want="$2" pat="${3:-}"
  if [ "$RC" -eq "$want" ] && { [ -z "$pat" ] || echo "$OUT" | grep -q "$pat"; }; then
    echo "ok: $label"
  else
    echo "fail: $label — rc=$RC (want $want): $(echo "$OUT" | tail -2 | tr '\n' ' ')"
  fi
}

# 1 — within-limits doc change by the product loop passes
G foundry-loop '[{"path":"README.md","action":"modify"}]'
case_rc "within-limits doc change allows (rc 0)" 0 "VERDICT ALLOW"

# 2 — validator edit is desk-routed, and --queue files the item
G foundry-loop '[{"path":"tools/validate.py","action":"modify"}]' --queue
case_rc "law-book edit desk-routes (rc 3)" 3 "Article I §5"
if [ -f "$FX/state/DESK.jsonl" ] && grep -q '"kind": "ratify"' "$FX/state/DESK.jsonl"; then
  echo "ok: desk item queued for ratification"
else
  echo "fail: desk item missing after --queue"
fi

# 3 — dedup: the same desk item is not queued twice
G foundry-loop '[{"path":"tools/validate.py","action":"modify"}]' --queue
if echo "$OUT" | grep -q "already open" && [ "$(grep -c '"kind": "ratify"' "$FX/state/DESK.jsonl")" -eq 1 ]; then
  echo "ok: desk dedup holds (one open ratify item)"
else
  echo "fail: desk dedup — $(grep -c '"kind": "ratify"' "$FX/state/DESK.jsonl" || true) ratify lines"
fi

# 4 — record deletion is blocked outright
G foundry-loop '[{"path":"foundry/records/demo.md","action":"delete"}]'
case_rc "record deletion blocks (rc 4)" 4 "Article I §2"

# 5 — journal deletion is blocked outright
G foundry-loop '[{"path":"state/JOURNAL.md","action":"delete"}]'
case_rc "journal deletion blocks (rc 4)" 4 "Article I §2"

# 6 — an agent editing its own governing rule is desk-routed
G briefing '[{"path":"foundry/agents/briefing/agent.json","action":"modify"}]'
case_rc "own-manifest edit desk-routes (rc 3)" 3 "Article I §6"

# 7 — out-of-scope write is blocked
G briefing '[{"path":"plugins/commit-craft/README.md","action":"modify"}]'
case_rc "out-of-capability write blocks (rc 4)" 4 "out of capability scope"

# 8 — in-scope write is allowed
G briefing '[{"path":"state/briefings/2026-07-12.md","action":"add"}]'
case_rc "in-scope write allows (rc 0)" 0 "VERDICT ALLOW"

# 9 — read_only agents hold no pen
G scout '[{"path":"COMPETITIVE.md","action":"modify"}]'
case_rc "read_only changeset blocks (rc 4)" 4 "read_only"

# 10 — proposes agents land only via the desk
G postmortem '[{"path":"reviews/postmortems/pm-001.md","action":"add"}]'
case_rc "proposes changeset desk-routes (rc 3)" 3 "desk approval"

# 11 — unknown agent: no manifest, no pen
G ghost '[{"path":"README.md","action":"modify"}]'
case_rc "unknown agent blocks (rc 4)" 4 "no manifest, no pen"

# 12 — path escape is blocked
G foundry-loop '[{"path":"../outside.txt","action":"add"}]'
case_rc "path escape blocks (rc 4)" 4 "escapes the repo"
