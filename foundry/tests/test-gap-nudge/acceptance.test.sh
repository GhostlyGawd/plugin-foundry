#!/usr/bin/env bash
# test-gap-nudge acceptance checks 1–7 (record: foundry/records/test-gap-nudge.md)
set -uo pipefail
SCRIPT="$PWD/${PLUGIN_DIR:-plugins/test-gap-nudge}/scripts/nudge.sh"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
export TMPDIR="$WORK/tmp"; mkdir -p "$TMPDIR"

mkrepo() { local d="$WORK/$1"; mkdir -p "$d"; git -C "$d" init -q .; echo "$d"; }
run() { # run <dir> <session> ; echoes output, returns exit code
  ( cd "$1" && printf '{"session_id":"%s"}' "$2" | bash "$SCRIPT" ); }

# 1 — dirty src, no tests → systemMessage names the file, exit 0
d=$(mkrepo one); echo x > "$d/app.py"
out=$(run "$d" s1); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q '"systemMessage"' && echo "$out" | grep -q 'app.py'; then
  echo "ok: check1 gap nudged with filename, exit 0"
else echo "fail: check1 — rc=$rc out=$out"; fi

# 4 — same session again → silent (marker)
out=$(run "$d" s1); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check4 once-per-session" || echo "fail: check4 — rc=$rc out=$out"

# 2 — src + untracked test file → silent
d=$(mkrepo two); echo x > "$d/app.py"; mkdir -p "$d/tests"; echo t > "$d/tests/test_app.py"
out=$(run "$d" s2); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check2 test activity silences" || echo "fail: check2 — rc=$rc out=$out"

# 2b — filename-convention test beside source → silent
d=$(mkrepo twob); echo x > "$d/app.py"; echo t > "$d/app.spec.py"
out=$(run "$d" s2b); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check2b *.spec.* counts as tests" || echo "fail: check2b — rc=$rc out=$out"

# 3 — clean tree → silent; non-repo dir → silent; no git on PATH → silent
d=$(mkrepo three)
out=$(run "$d" s3); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check3a clean tree silent" || echo "fail: check3a — rc=$rc out=$out"
mkdir -p "$WORK/plain"
out=$( cd "$WORK/plain" && printf '{}' | bash "$SCRIPT" ); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check3b non-repo silent" || echo "fail: check3b — rc=$rc out=$out"
d=$(mkrepo nogit); echo x > "$d/app.py"
BASH_BIN=$(command -v bash)
out=$( cd "$d" && printf '{}' | env PATH=/nonexistent "$BASH_BIN" "$SCRIPT" ); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check3c no git on PATH silent" || echo "fail: check3c — rc=$rc out=$out"

# 5 — malformed/empty stdin → still exit 0, never exit 2
d=$(mkrepo five); echo x > "$d/app.py"
out=$( cd "$d" && printf 'not json at all' | bash "$SCRIPT" ); rc=$?
[ "$rc" -eq 0 ] && echo "ok: check5a malformed stdin exit 0" || echo "fail: check5a — rc=$rc"
out=$( cd "$d" && bash "$SCRIPT" < /dev/null ); rc=$?
[ "$rc" -eq 0 ] && echo "ok: check5b empty stdin exit 0" || echo "fail: check5b — rc=$rc"

# 6 — docs-only change → silent
d=$(mkrepo six); echo x > "$d/README.md"; echo y > "$d/config.json"
out=$(run "$d" s6); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check6 docs/config-only silent" || echo "fail: check6 — rc=$rc out=$out"

# 7 — structural: Stop event, quoted plugin root, executable script with shebang
H="$PWD/${PLUGIN_DIR:-plugins/test-gap-nudge}/hooks/hooks.json"
if python3 -c "
import json,sys
h=json.load(open('$H'))['hooks']
assert list(h)==['Stop'], 'event'
cmd=h['Stop'][0]['hooks'][0]['command']
assert '\"\${CLAUDE_PLUGIN_ROOT}' in cmd, 'quoting'
" 2>/dev/null && [ -x "$SCRIPT" ] && head -1 "$SCRIPT" | grep -q '^#!'; then
  echo "ok: check7 hooks.json Stop + quoted root + executable shebang script"
else echo "fail: check7 structural"; fi
