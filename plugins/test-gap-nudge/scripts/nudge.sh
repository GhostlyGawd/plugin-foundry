#!/usr/bin/env bash
# test-gap-nudge — advisory Stop hook: source files changed, no tests touched → say
# so once. Contract (record spec): exit 0 ALWAYS; read-only except a TMPDIR marker;
# no network; stdin is untrusted data — only a session id is extracted from it.
set -u
exec 2>/dev/null || true

# swallow any internal error into a silent, non-blocking exit
trap 'exit 0' ERR

STDIN_DATA=$(cat 2>/dev/null || true)

# opt-in debug trail (v10 #10): TEST_GAP_NUDGE_DEBUG=1 appends the decision
# path to a temp log. With it unset, dbg is a no-op — behavior byte-identical.
DBGLOG="${TMPDIR:-/tmp}/test-gap-nudge-debug.log"
dbg() { [ "${TEST_GAP_NUDGE_DEBUG:-}" = "1" ] && printf '%s %s\n' "$(date -u +%FT%TZ 2>/dev/null)" "$*" >> "$DBGLOG" 2>/dev/null; true; }
dbg "run: pwd=$PWD"

command -v git >/dev/null 2>&1 || { dbg "exit: no git on PATH"; exit 0; }
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { dbg "exit: not a work tree"; exit 0; }

# session id: permissive extraction; anything but [A-Za-z0-9_-] is discarded.
SID=$(printf '%s' "$STDIN_DATA" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([A-Za-z0-9_-]*\)".*/\1/p' | head -1)
if [ -z "$SID" ]; then
  SID=$(git rev-parse --show-toplevel 2>/dev/null | cksum | cut -d' ' -f1)
fi
MARKER="${TMPDIR:-/tmp}/test-gap-nudge-${SID:-fallback}"
[ -f "$MARKER" ] && { dbg "exit: already nudged this session ($MARKER)"; exit 0; }

# which extensions count as "source" — override with TEST_GAP_NUDGE_EXTS
# (pipe/comma/space-separated, e.g. "py|rs|zig"); anything but [A-Za-z0-9|] is
# stripped so a malformed value can never break the regex; empty → default.
SRC_EXT_DEFAULT='py|js|ts|tsx|jsx|mjs|go|rb|rs|java|c|cc|cpp|h|hpp|sh|php|cs|kt|swift|scala'
SRC_EXT=$(printf '%s' "${TEST_GAP_NUDGE_EXTS:-}" | tr ', ' '||' | tr -cd 'A-Za-z0-9|' | tr -s '|')
SRC_EXT=${SRC_EXT#|}; SRC_EXT=${SRC_EXT%|}
[ -z "$SRC_EXT" ] && SRC_EXT="$SRC_EXT_DEFAULT"
src_hits=()
test_seen=0

while IFS= read -r line; do
  [ -n "$line" ] || continue
  path=${line:3}
  # renames report "old -> new"; judge the new path
  case "$path" in *" -> "*) path=${path##* -> } ;; esac
  case "$path" in \"*\") path=${path%\"}; path=${path#\"} ;; esac
  base=${path##*/}
  # test path? (dir segment or filename convention)
  if [[ "$path" =~ (^|/)(test|tests|spec|__tests__)(/|$) ]] || \
     [[ "$base" == test_* || "$base" == *_test.* || "$base" == *.test.* || "$base" == *.spec.* ]]; then
    test_seen=1
    continue
  fi
  ext=${base##*.}
  if [ "$ext" != "$base" ] && [[ "$ext" =~ ^($SRC_EXT)$ ]]; then
    src_hits+=("$path")
  fi
done < <(git status --porcelain -uall 2>/dev/null)

dbg "classified: src=${#src_hits[@]} test_seen=$test_seen exts=$SRC_EXT"
[ "$test_seen" -eq 1 ] && { dbg "exit: test activity seen — silent"; exit 0; }
[ "${#src_hits[@]}" -eq 0 ] && { dbg "exit: no source changes — silent"; exit 0; }

names=$(printf '%s, ' "${src_hits[@]:0:3}")
names=${names%, }
[ "${#src_hits[@]}" -gt 3 ] && names="$names, …"
# best-effort marker; failure to write must not silence the nudge
touch "$MARKER" 2>/dev/null || true

dbg "nudge: ${#src_hits[@]} source file(s), no tests — emitting systemMessage"
# JSON-escape the file list (quotes and backslashes only; names are repo paths)
esc=$(printf '%s' "$names" | sed 's/\\/\\\\/g; s/"/\\"/g')
printf '{"systemMessage": "test-gap-nudge: %s source file(s) changed, no test files touched — %s"}\n' \
  "${#src_hits[@]}" "$esc"
exit 0
