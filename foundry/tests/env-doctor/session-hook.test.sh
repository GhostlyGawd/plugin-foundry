#!/usr/bin/env bash
# env-doctor SessionStart hook — safety + behavior suite (v13 A2).
# Contract: exit 0 ALWAYS; systemMessage only on a clear declared-vs-installed
# mismatch; silent on match, no declaration, or ENV_DOCTOR_SILENT=1.
set -uo pipefail
P="${PLUGIN_DIR:-plugins/env-doctor}"
SCRIPT="$PWD/$P/scripts/session-envcheck.sh"
CLAUDE_HOOKS="$PWD/$P/hooks/hooks.json"
GEMINI_HOOKS="$PWD/$P/hooks/gemini.json"
CURSOR_HOOKS="$PWD/$P/hooks/cursor.json"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

mkrepo() { local d="$WORK/$1"; mkdir -p "$d"; git -C "$d" init -q .; echo "$d"; }
run() { printf '{"cwd":"%s"}' "$1" | bash "$SCRIPT"; }  # run <dir>

# 1 — clear python mismatch → systemMessage names the tool, exit 0
d=$(mkrepo miss); echo "3.99" > "$d/.python-version"
out=$(run "$d"); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q '"systemMessage"' && echo "$out" | grep -q 'python'; then
  echo "ok: check1 declared-version mismatch warns, exit 0"
else echo "fail: check1 — rc=$rc out=$out"; fi

# 2 — matching version → silent
d=$(mkrepo match); python3 -c 'import sys;print("%d.%d"%sys.version_info[:2])' > "$d/.python-version"
out=$(run "$d"); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check2 matching version silent" || echo "fail: check2 — rc=$rc out=$out"

# 3 — no declaration files → silent
d=$(mkrepo bare)
out=$(run "$d"); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check3 nothing declared → silent" || echo "fail: check3 — rc=$rc out=$out"

# 4 — ENV_DOCTOR_SILENT=1 → silent even on a real mismatch (opt-out)
d=$(mkrepo optout); echo "3.99" > "$d/.python-version"
out=$(printf '{"cwd":"%s"}' "$d" | ENV_DOCTOR_SILENT=1 bash "$SCRIPT"); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check4 ENV_DOCTOR_SILENT opts out" || echo "fail: check4 — rc=$rc out=$out"

# 5 — garbage/empty stdin → still exit 0, never blocks
out=$(printf 'not json at all' | bash "$SCRIPT"); rc=$?
[ "$rc" -eq 0 ] && echo "ok: check5a garbage stdin exit 0" || echo "fail: check5a — rc=$rc"
out=$(bash "$SCRIPT" < /dev/null); rc=$?
[ "$rc" -eq 0 ] && echo "ok: check5b empty stdin exit 0" || echo "fail: check5b — rc=$rc"

# 6 — structural: equivalent native SessionStart maps, executable script
if python3 -c "
import json
c=json.load(open('$CLAUDE_HOOKS'))['hooks']
g=json.load(open('$GEMINI_HOOKS'))['hooks']
u=json.load(open('$CURSOR_HOOKS'))['hooks']
assert list(c)==['SessionStart'] and list(g)==['SessionStart'], 'start events'
assert list(u)==['sessionStart'], 'cursor start event'
assert '\"\${CLAUDE_PLUGIN_ROOT}' in c['SessionStart'][0]['hooks'][0]['command']
assert '\"\${extensionPath}' in g['SessionStart'][0]['hooks'][0]['command']
assert '\"\${CURSOR_PLUGIN_ROOT}' in u['sessionStart'][0]['command']
" 2>/dev/null && [ -x "$SCRIPT" ] && head -1 "$SCRIPT" | grep -q '^#!'; then
  echo "ok: check6 native SessionStart maps + quoted roots + executable shebang"
else echo "fail: check6 structural"; fi
