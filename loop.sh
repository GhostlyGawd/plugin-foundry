#!/usr/bin/env bash
# loop.sh — the harness. Runs Claude Code against LOOP.md, one iteration per pass.
#
#   ./loop.sh            # 10 iterations (default)
#   ./loop.sh 50         # 50 iterations
#   touch STOP           # halt gracefully at the next pass boundary
#
# Env knobs:
#   LOOP_MODEL=opus            pass a model to claude (optional)
#   LOOP_PERMS="--permission-mode acceptEdits"   safer, semi-supervised mode
#   LOOP_SLEEP=5               seconds between iterations (default 3)
#
# Default permission mode is --dangerously-skip-permissions, which is what makes
# unattended loops possible — and is exactly as risky as it sounds. Run this inside
# a container or dedicated VM with only this repo mounted. Git is your undo button.

set -uo pipefail
cd "$(dirname "$0")"

MAX="${1:-10}"
SLEEP="${LOOP_SLEEP:-3}"
PERMS="${LOOP_PERMS:---dangerously-skip-permissions}"
MODEL_ARGS=()
[ -n "${LOOP_MODEL:-}" ] && MODEL_ARGS=(--model "$LOOP_MODEL")

command -v claude >/dev/null 2>&1 || {
  echo "loop.sh: 'claude' not found. Install Claude Code first:"
  echo "  npm install -g @anthropic-ai/claude-code"
  exit 1
}
command -v git >/dev/null 2>&1 || { echo "loop.sh: git is required."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "loop.sh: python3 is required."; exit 1; }

# One-time acknowledgment when running with permissions bypassed.
if [[ "$PERMS" == *dangerously* && ! -f .sandbox-ack ]]; then
  if [ -n "${CI:-}" ] || [ ! -t 0 ]; then
    echo "loop.sh: CI/non-interactive run detected — treating the ephemeral runner as the sandbox (ADR-002)."
    touch .sandbox-ack
  else
  cat <<'WARN'
+--------------------------------------------------------------------------+
|  This harness defaults to --dangerously-skip-permissions: Claude Code    |
|  will edit files and run shell commands here WITHOUT asking.             |
|                                                                          |
|  Run it inside a container / dedicated VM with only this repo mounted.   |
|  Safer alternative:  LOOP_PERMS="--permission-mode acceptEdits" ./loop.sh|
+--------------------------------------------------------------------------+
WARN
  read -r -p 'Type SANDBOXED to acknowledge and continue: ' ACK
  [ "$ACK" = "SANDBOXED" ] || { echo "Not acknowledged. Exiting."; exit 1; }
  touch .sandbox-ack
  fi
fi

# The repo is the memory; git is the audit trail and the undo button.
if [ ! -d .git ]; then
  git init -q
  git add -A && git commit -qm "loop(i0/genesis): seed the workshop"
  echo "loop.sh: initialized git and committed the seed."
fi

# Budget governor (ADR-008): with LOOP_MONTHLY_BUDGET_USD set, an exhausted month
# skips the shift cleanly instead of overspending.
if ! python3 tools/budget.py check; then
  python3 tools/alarm.py "Governor halt — $(date -u +%Y-%m) budget exhausted" \
    "The monthly LOOP_MONTHLY_BUDGET_USD cap is spent (state/BUDGET.jsonl). Shifts self-skip until the month rolls or the cap is raised." || true
  echo "loop.sh: governor halt — see state/BUDGET.jsonl"; exit 0
fi

# Auth surface (AUTH-1, ADR-031): one module decides whether a usable credential
# exists. In CI with none, fail LOUDLY now — a silent no-op shift is worse than
# a red one (the 2026-07-07 lesson).
if ! python3 tools/auth.py check; then
  python3 tools/alarm.py "Auth halt — no usable credential in CI" \
    "tools/auth.py found neither ANTHROPIC_API_KEY nor CLAUDE_CODE_OAUTH_TOKEN. See its printed remedy; the loop refuses to no-op silently." || true
  echo "loop.sh: auth halt — see tools/auth.py remedy above"; exit 1
fi

mkdir -p state/runs
FAILS=0

echo "loop.sh: up to $MAX iteration(s) | perms: $PERMS | stop anytime with: touch STOP"
for ((i = 1; i <= MAX; i++)); do
  if [ -f STOP ]; then
    echo "loop.sh: STOP file present — halting before iteration $i."
    break
  fi

  LOG="state/runs/$(date -u +%Y%m%dT%H%M%SZ).log"
  echo "── pass $i/$MAX ──────────────────────────────────────────── $(date -u +%H:%M:%SZ)"

  if [ -n "${CI:-}" ]; then
    # JSON mode: capture cost for the ledger, surface the result text for the log.
    if claude -p "$(cat LOOP.md)" $PERMS "${MODEL_ARGS[@]}" --output-format json > "$LOG.json" 2>"$LOG.err"; then
      python3 tools/budget.py add "$LOG.json" || true
      python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d.get('result') or d)" "$LOG.json" | tee "$LOG"
      RC=0
    else
      cat "$LOG.err" | tee "$LOG"; RC=1
    fi
  else
    claude -p "$(cat LOOP.md)" $PERMS "${MODEL_ARGS[@]}" 2>&1 | tee "$LOG"; RC=$?
  fi
  if [ "$RC" -eq 0 ]; then
    FAILS=0
  else
    FAILS=$((FAILS + 1))
    echo "loop.sh: claude exited nonzero (streak: $FAILS). Log: $LOG"
    # AUTH-1 (ADR-031): classify the failure. Auth-shaped → halt on the FIRST
    # one, loudly, with the remedy — never streak silently on a dead token.
    python3 tools/auth.py probe "$LOG.json" "$LOG.err" "$LOG"; PROBE_RC=$?
    if [ "$PROBE_RC" -eq 2 ]; then
      python3 tools/alarm.py "Auth halt — credential rejected mid-shift" \
        "tools/auth.py classified the claude failure as an auth failure (see the run log tail in the Actions diagnostic step). Remedy printed by auth.py; the loop halted on the first failure instead of streaking." || true
      echo "loop.sh: AUTH FAILURE — halting immediately (see remedy above)."
      break
    fi
    if [ "$FAILS" -ge 3 ]; then
      echo "loop.sh: 3 consecutive failures — halting for a human. See state/runs/."
      break
    fi
  fi

  # Belt-and-suspenders: never let a red repo roll into the next pass.
  if ! python3 tools/validate.py >/dev/null 2>&1; then
    echo "loop.sh: repo failed validation after the pass — halting for a human."
    python3 tools/validate.py || true
    break
  fi

  sleep "$SLEEP"
done

echo "── done ─────────────────────────────────────────────────────"
python3 - <<'PY' 2>/dev/null || true
import json
state = json.load(open("state/STATE.json"))
name = state.get("name") or state.get("codename")
print(f"{name}: iteration {state['iteration']}, phase {state['phase']}")
PY
echo "latest journal:"; grep '^## i' state/JOURNAL.md | tail -n 3
