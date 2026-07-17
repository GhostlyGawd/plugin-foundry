#!/usr/bin/env bash
# Interactive auth boundary: no reusable model credential is read or recommended.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

A() { env -i PATH="$PATH" "$@" python3 "$REPO/tools/auth.py" check 2>&1; }

# 1 — CI/headless execution fails loudly and points to an attended session.
out=$(A CI=true); rc=$?
if [ "$rc" -eq 1 ] && echo "$out" | grep -qi "interactive"; then
  echo "ok: CI model execution fails closed"
else echo "fail: CI boundary — rc=$rc $out"; fi

# 2 — a local process reports interactive-local without inspecting credentials.
out=$(A); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q "interactive-local"; then
  echo "ok: local execution defers to the interactive host"
else echo "fail: local mode — $out"; fi

# 3 — credential-shaped environment variables cannot enable CI or leak values.
out=$(A CI=true OPENAI_API_KEY=SECRETVALUE ANTHROPIC_API_KEY=OTHERSECRET); rc=$?
if [ "$rc" -eq 1 ] && ! echo "$out" | grep -Eq "SECRETVALUE|OTHERSECRET"; then
  echo "ok: environment credentials neither enable nor leak"
else echo "fail: credential environment bypass — $out"; fi

# 4 — historical auth failures remain classifiable without provisioning advice.
LOG="$WORK/run.json"
printf '{"type":"result","is_error":true,"result":"OAuth token has expired."}\n' > "$LOG"
out=$(python3 "$REPO/tools/auth.py" probe "$LOG" 2>&1); rc=$?
if [ "$rc" -eq 2 ] && echo "$out" | grep -q "AUTH FAILURE" \
  && echo "$out" | grep -qi "interactive" && ! echo "$out" | grep -q "setup-token"; then
  echo "ok: historical auth failure points to interactive recovery"
else echo "fail: historical probe — rc=$rc $out"; fi

# 5 — 401 remains auth-shaped; unrelated failures do not become false auth alarms.
printf 'API Error: 401 authentication_error\n' > "$LOG"
python3 "$REPO/tools/auth.py" probe "$LOG" >/dev/null 2>&1
[ "$?" -eq 2 ] && echo "ok: 401 classified" || echo "fail: 401 not classified"
printf 'ENOSPC no space left on device\n' > "$LOG"
out=$(python3 "$REPO/tools/auth.py" probe "$LOG" 2>&1); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q "not auth-shaped"; then
  echo "ok: unrelated failure stays unrelated"
else echo "fail: false auth classification — $out"; fi

# 6 — missing logs stay calm; auth.py contains no model credential read.
python3 "$REPO/tools/auth.py" probe "$WORK/missing" >/dev/null 2>&1
[ "$?" -eq 0 ] && echo "ok: missing log tolerated" || echo "fail: missing log"
if grep -Eq 'getenv\([^)]*(OPENAI|ANTHROPIC|TOKEN)|environ[^\n]*(OPENAI|ANTHROPIC|TOKEN)' "$REPO/tools/auth.py"; then
  echo "fail: auth.py still reads a reusable model credential"
else
  echo "ok: auth.py reads no reusable model credential"
fi
