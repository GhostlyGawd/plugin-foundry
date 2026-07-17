#!/usr/bin/env bash
# Eval-harness tests (MASTER P5.2, ADR-030): the golden evals must (a) all pass
# against the real safety tools, and (b) actually FAIL when a tool regresses —
# an eval suite that can't go red is theater.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# 1 — the real fixtures all pass against the real tools
out=$(cd "$REPO" && python3 tools/evals.py run 2>&1); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -qE "evals: [0-9]+/[0-9]+ golden cases pass" \
   && ! echo "$out" | grep -q "✗"; then
  echo "ok: all golden evals pass against the live guard + fence"
else echo "fail: real evals — $out"; fi

# 2 — inventory is non-trivial (guard + fence both have cases)
out=$(cd "$REPO" && python3 tools/evals.py list 2>&1)
gn=$(echo "$out" | sed -n 's/.*guard — \([0-9]*\).*/\1/p')
fn=$(echo "$out" | sed -n 's/.*fence — \([0-9]*\).*/\1/p')
if [ "${gn:-0}" -ge 10 ] && [ "${fn:-0}" -ge 8 ]; then
  echo "ok: fixture inventory covers guard ($gn) + fence ($fn)"
else echo "fail: thin inventory — guard=$gn fence=$fn"; fi

# 3 — the suite CAN go red: a regressed guard fixture is caught
FX="$WORK/fx"
mkdir -p "$FX/tools" "$FX/foundry/evals" "$FX/foundry/agents/foundry-loop"
cp "$REPO"/tools/{lib.py,guard.py,fence.py,desk.py,evals.py} "$FX/tools/"
cp "$REPO"/foundry/evals/fence.jsonl "$FX/foundry/evals/"
cat > "$FX/foundry/agents/foundry-loop/agent.json" <<'J'
{"id":"foundry-loop","role":"loop","trigger":"schedule","trust_tier":"trusted","quota_tier":"product","capability":"writes:**","outputs":["x"],"heartbeat":{"interval_hours":24}}
J
( cd "$FX" && python3 - <<'PY'
import sys; sys.path.insert(0,"tools")
from lib import build_agent_registry
build_agent_registry(".")
PY
)
# a POISONED fixture: claims deleting the journal should be "allow" (it must block)
cat > "$FX/foundry/evals/guard.jsonl" <<'J'
{"note":"poison — journal deletion mislabeled allow","agent":"foundry-loop","changes":[{"path":"state/JOURNAL.md","action":"delete"}],"expect":"allow"}
J
out=$(cd "$FX" && python3 tools/evals.py run 2>&1); rc=$?
if [ "$rc" -eq 1 ] && echo "$out" | grep -q "✗ guard#1"; then
  echo "ok: eval harness goes red on a regression (not theater)"
else echo "fail: harness didn't catch the poison — rc=$rc $out"; fi

# 4 — the promptfoo lane is explicitly paused and contains no callable provider.
out=$(cd "$REPO" && python3 tools/evals.py run 2>&1)
if echo "$out" | grep -q "llm-graded suite paused" \
  && grep -q '^providers: \[\]$' "$REPO/foundry/evals/promptfoo.yaml" \
  && grep -q '^prompts: \[\]$' "$REPO/foundry/evals/promptfoo.yaml" \
  && grep -q '^tests: \[\]$' "$REPO/foundry/evals/promptfoo.yaml" \
  && ! grep -Eqi 'anthropic:|openai:|google:|api.?key' "$REPO/foundry/evals/promptfoo.yaml"; then
  echo "ok: llm-graded lane is inert; deterministic fixtures remain"
else
  echo "fail: LLM eval lane can still arm — $out"
fi
