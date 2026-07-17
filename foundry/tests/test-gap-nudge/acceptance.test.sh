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

# 7 — structural: equivalent native stop/after-agent maps, executable script
HROOT="$PWD/${PLUGIN_DIR:-plugins/test-gap-nudge}/hooks"
if python3 -c "
import json,sys
c=json.load(open('$HROOT/hooks.json'))['hooks']
g=json.load(open('$HROOT/gemini.json'))['hooks']
u=json.load(open('$HROOT/cursor.json'))['hooks']
assert list(c)==['Stop'] and list(g)==['AfterAgent'] and list(u)==['stop']
assert '\"\${CLAUDE_PLUGIN_ROOT}' in c['Stop'][0]['hooks'][0]['command']
assert '\"\${extensionPath}' in g['AfterAgent'][0]['hooks'][0]['command']
assert '\"\${CURSOR_PLUGIN_ROOT}' in u['stop'][0]['command']
" 2>/dev/null && [ -x "$SCRIPT" ] && head -1 "$SCRIPT" | grep -q '^#!'; then
  echo "ok: check7 native stop maps + quoted roots + executable script"
else echo "fail: check7 structural"; fi

# 8 — i102 bounce regression: source file inside a brand-new directory still nudges
d=$(mkrepo eight); git -C "$d" commit -q --allow-empty -m base
mkdir -p "$d/newmod"; echo x > "$d/newmod/core.py"
out=$(run "$d" s8); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q 'newmod/core.py'; then
  echo "ok: check8 new-directory source nudges (-uall regression)"
else echo "fail: check8 — rc=$rc out=$out"; fi

# 8b — and a brand-new tests directory still silences
d=$(mkrepo eightb); git -C "$d" commit -q --allow-empty -m base
echo x > "$d/app.py"; mkdir -p "$d/tests"; echo t > "$d/tests/test_core.py"
out=$(run "$d" s8b); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check8b new tests dir silences" || echo "fail: check8b — rc=$rc out=$out"

# i155 (v10 #2): TEST_GAP_NUDGE_EXTS knob
d=$(mkrepo knob1); echo x > "$d/app.zig"
out=$( ( cd "$d" && printf '{"session_id":"k1"}' | TEST_GAP_NUDGE_EXTS="zig" bash "$SCRIPT" ) ); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q 'app.zig'; then
  echo "ok: knob1 custom extension nudges"
else echo "fail: knob1 — rc=$rc out=$out"; fi
d=$(mkrepo knob2); echo x > "$d/app.py"
out=$( ( cd "$d" && printf '{"session_id":"k2"}' | TEST_GAP_NUDGE_EXTS="zig" bash "$SCRIPT" ) ); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: knob2 override excludes defaults" || echo "fail: knob2 — rc=$rc out=$out"
d=$(mkrepo knob3); echo x > "$d/app.zig"
out=$( ( cd "$d" && printf '{"session_id":"k3"}' | TEST_GAP_NUDGE_EXTS='$(boom)|zig' bash "$SCRIPT" ) ); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q 'app.zig'; then
  echo "ok: knob3 hostile chars stripped, knob still works"
else echo "fail: knob3 — rc=$rc out=$out"; fi
d=$(mkrepo knob4); echo x > "$d/app.py"
out=$( ( cd "$d" && printf '{"session_id":"k4"}' | TEST_GAP_NUDGE_EXTS='%%%' bash "$SCRIPT" ) ); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q 'app.py'; then
  echo "ok: knob4 all-garbage value falls back to defaults"
else echo "fail: knob4 — rc=$rc out=$out"; fi

# i164 (v10 #10): debug trail — off by default, on when asked, behavior identical
d=$(mkrepo dbg1); echo x > "$d/app.py"
out=$( ( cd "$d" && printf '{"session_id":"dz1"}' | bash "$SCRIPT" ) ); rc=$?
[ ! -f "$TMPDIR/test-gap-nudge-debug.log" ] && echo "ok: dbg-off writes no log" || echo "fail: dbg-off wrote a log"
d=$(mkrepo dbg2); echo x > "$d/app.py"
out2=$( ( cd "$d" && printf '{"session_id":"dz2"}' | TEST_GAP_NUDGE_DEBUG=1 bash "$SCRIPT" ) ); rc2=$?
if [ "$rc" -eq "$rc2" ] && echo "$out2" | grep -q '"systemMessage"' && grep -q 'nudge: 1 source' "$TMPDIR/test-gap-nudge-debug.log"; then
  echo "ok: dbg-on logs trail, output/exit unchanged"
else echo "fail: dbg-on — rc=$rc2 out=$out2"; fi
