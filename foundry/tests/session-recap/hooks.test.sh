#!/usr/bin/env bash
# session-recap hooks — safety + behavior suite (v13 B5).
# Stop nudge: suggest a recap once per session when there's uncommitted work and
# no recap today. SessionStart recall: surface the last handoff title. Both
# fail-open (exit 0 always), read-only, silent on the empty/opt-out paths.
set -uo pipefail
P="${PLUGIN_DIR:-plugins/session-recap}"
NUDGE="$PWD/$P/scripts/recap-nudge.sh"
RECALL="$PWD/$P/scripts/recap-recall.sh"
CLAUDE_HOOKS="$PWD/$P/hooks/hooks.json"
GEMINI_HOOKS="$PWD/$P/hooks/gemini.json"
CURSOR_HOOKS="$PWD/$P/hooks/cursor.json"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
export TMPDIR="$WORK/tmp"; mkdir -p "$TMPDIR"

mkrepo() { local d="$WORK/$1"; mkdir -p "$d"; git -C "$d" init -q .; echo "$d"; }

# 1 — Stop: uncommitted work, no recap → nudge once, exit 0
d=$(mkrepo dirty); echo x > "$d/app.py"
out=$( cd "$d" && printf '{"session_id":"s1"}' | bash "$NUDGE" ); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q '"systemMessage"' && echo "$out" | grep -qi 'recap'; then
  echo "ok: check1 uncommitted work nudges, exit 0"
else echo "fail: check1 — rc=$rc out=$out"; fi

# 2 — Stop: same session again → silent (once-per-session marker)
out=$( cd "$d" && printf '{"session_id":"s1"}' | bash "$NUDGE" ); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check2 once-per-session" || echo "fail: check2 — rc=$rc out=$out"

# 3 — Stop: clean tree → silent
d=$(mkrepo clean); git -C "$d" -c user.email=a@b.c -c user.name=x commit -q --allow-empty -m base
out=$( cd "$d" && printf '{"session_id":"s3"}' | bash "$NUDGE" ); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check3 clean tree silent" || echo "fail: check3 — rc=$rc out=$out"

# 4 — Stop: recap already written today → silent
d=$(mkrepo recapped); echo x > "$d/app.py"; printf '## %s — done\n' "$(date -u +%F)" > "$d/SESSION-RECAP.md"
out=$( cd "$d" && printf '{"session_id":"s4"}' | bash "$NUDGE" ); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check4 recapped-today silent" || echo "fail: check4 — rc=$rc out=$out"

# 5 — SessionStart recall: file present → surfaces the last title
d=$(mkrepo recall); printf '## 2026-01-01 — old\n## 2026-07-07 — latest handoff\n' > "$d/SESSION-RECAP.md"
out=$( printf '{"cwd":"%s"}' "$d" | bash "$RECALL" ); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -q 'latest handoff'; then
  echo "ok: check5 recall surfaces most recent handoff"
else echo "fail: check5 — rc=$rc out=$out"; fi

# 6 — SessionStart recall: no file → silent
d=$(mkrepo norecall)
out=$( printf '{"cwd":"%s"}' "$d" | bash "$RECALL" ); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check6 no recap file → silent" || echo "fail: check6 — rc=$rc out=$out"

# 7 — opt-out + garbage stdin → exit 0, silent (nudge & recall)
out=$( cd "$d" && echo z > z.py && printf '{"session_id":"s7"}' | SESSION_RECAP_SILENT=1 bash "$NUDGE" ); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ok: check7a SESSION_RECAP_SILENT opts out" || echo "fail: check7a — rc=$rc out=$out"
out=$( printf 'not json' | bash "$RECALL" ); rc1=$?
out2=$( printf 'not json' | bash "$NUDGE" < /dev/null ); rc2=$?
{ [ "$rc1" -eq 0 ] && [ "$rc2" -eq 0 ]; } && echo "ok: check7b garbage stdin exit 0 (both hooks)" || echo "fail: check7b — recall=$rc1 nudge=$rc2"

# 8 — structural: equivalent native lifecycle maps and executable scripts
if python3 -c "
import json
c=json.load(open('$CLAUDE_HOOKS'))['hooks']
g=json.load(open('$GEMINI_HOOKS'))['hooks']
u=json.load(open('$CURSOR_HOOKS'))['hooks']
assert set(c)=={'SessionStart','Stop'}, 'open plugin events'
assert set(g)=={'SessionStart','AfterAgent'}, 'gemini events'
assert set(u)=={'sessionStart','stop'}, 'cursor events'
assert all('\"\${CLAUDE_PLUGIN_ROOT}' in x[0]['hooks'][0]['command'] for x in c.values())
assert all('\"\${extensionPath}' in x[0]['hooks'][0]['command'] for x in g.values())
assert all('\"\${CURSOR_PLUGIN_ROOT}' in x[0]['command'] for x in u.values())
" 2>/dev/null && [ -x "$NUDGE" ] && [ -x "$RECALL" ] \
   && head -1 "$NUDGE" | grep -q '^#!' && head -1 "$RECALL" | grep -q '^#!'; then
  echo "ok: check8 native lifecycle maps + quoted roots + executable scripts"
else echo "fail: check8 structural"; fi
