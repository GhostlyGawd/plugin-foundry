#!/usr/bin/env bash
# Auth-surface tests (MASTER AUTH-1, ADR-031): one module interprets
# credentials; switching billing modes is a secrets change, zero code; auth
# failures are classified and LOUD, never a silent no-op.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

A() { env -i PATH="$PATH" "$@" python3 "$REPO/tools/auth.py" check 2>&1; }

# 1 — API key wins (mirrors Claude Code's precedence)
out=$(A CI=true ANTHROPIC_API_KEY=sk-test CLAUDE_CODE_OAUTH_TOKEN=tok); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q "mode api"; then
  echo "ok: api key takes precedence"
else echo "fail: precedence — $out"; fi

# 2 — subscription mode
out=$(A CI=true CLAUDE_CODE_OAUTH_TOKEN=tok); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q "mode subscription"; then
  echo "ok: subscription mode resolves"
else echo "fail: subscription — $out"; fi

# 3 — CI with nothing fails LOUDLY with the remedy
out=$(A CI=true); rc=$?
if [ "$rc" -eq 1 ] && echo "$out" | grep -q "REMEDY" && echo "$out" | grep -q "CLAUDE_CODE_OAUTH_TOKEN"; then
  echo "ok: bare CI fails loudly with remedy"
else echo "fail: bare CI — rc=$rc $out"; fi

# 4 — local machine with nothing defers to claude's login
out=$(A); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q "local-login"; then
  echo "ok: local-login mode (no env, no CI)"
else echo "fail: local-login — $out"; fi

# 5 — no credential value is ever echoed
out=$(A CI=true ANTHROPIC_API_KEY=sk-SECRETVALUE)
if echo "$out" | grep -q "SECRETVALUE"; then
  echo "fail: credential value leaked into output"
else echo "ok: credentials never printed"; fi

# 6 — probe classifies the REAL 2026-07-07 failure shape
LOG="$WORK/run.json"
printf '{"type":"result","is_error":true,"result":"OAuth token has expired. Please obtain a new token or refresh your existing token."}\n' > "$LOG"
out=$(python3 "$REPO/tools/auth.py" probe "$LOG" 2>&1); rc=$?
if [ "$rc" -eq 2 ] && echo "$out" | grep -q "AUTH FAILURE" && echo "$out" | grep -q "setup-token"; then
  echo "ok: probe classifies expired-token log, prints remedy"
else echo "fail: probe expired — rc=$rc $out"; fi

# 7 — probe classifies 401/authentication_error
printf 'API Error: 401 {"type":"error","error":{"type":"authentication_error","message":"invalid x-api-key"}}\n' > "$LOG"
out=$(python3 "$REPO/tools/auth.py" probe "$LOG" 2>&1); rc=$?
[ "$rc" -eq 2 ] && echo "ok: probe classifies 401 authentication_error" \
                || echo "fail: probe 401 — rc=$rc $out"

# 8 — a non-auth failure is NOT classified as auth (no false halt)
printf 'Error: ENOSPC no space left on device while writing site/index.html\n' > "$LOG"
out=$(python3 "$REPO/tools/auth.py" probe "$LOG" 2>&1); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q "not auth-shaped"; then
  echo "ok: non-auth failure not misclassified"
else echo "fail: probe non-auth — rc=$rc $out"; fi

# 9 — missing log files: probe stays calm
out=$(python3 "$REPO/tools/auth.py" probe "$WORK/nope.json" 2>&1); rc=$?
[ "$rc" -eq 0 ] && echo "ok: probe tolerates missing logs" \
                || echo "fail: probe missing — $out"

# 10 — the abstraction lint: no tool but auth.py READS the token env vars
# (mentioning the names in operator-facing strings is fine; environ access
# outside the single surface is not)
leaks=$(grep -rlE "(environ|getenv)[^\n]*(CLAUDE_CODE_OAUTH_TOKEN|ANTHROPIC_API_KEY)" \
        "$REPO/tools" --include='*.py' | grep -v "auth.py" || true)
if [ -z "$leaks" ]; then
  echo "ok: auth surface is single (no other tool reads the token envs)"
else echo "fail: token envs read outside auth.py: $leaks"; fi
