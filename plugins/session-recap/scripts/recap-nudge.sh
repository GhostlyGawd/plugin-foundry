#!/usr/bin/env bash
# session-recap Stop hook: at session end, if there's uncommitted work and no
# recap was written today, gently suggest one — once per session. Contract:
# exit 0 ALWAYS; read-only except a TMPDIR marker; no network; silent when the
# tree is clean, a recap already exists for today, outside a git repo, or with
# SESSION_RECAP_SILENT=1. The `recap` skill does the actual writing.
set -u
exec 2>/dev/null || true
trap 'exit 0' ERR

[ "${SESSION_RECAP_SILENT:-}" = "1" ] && exit 0

DBGLOG="${TMPDIR:-/tmp}/session-recap-debug.log"
dbg() { [ "${SESSION_RECAP_DEBUG:-}" = "1" ] && printf '%s %s\n' "$(date -u +%FT%TZ 2>/dev/null)" "$*" >> "$DBGLOG" 2>/dev/null; true; }

STDIN_DATA=$(cat 2>/dev/null || true)
command -v git >/dev/null 2>&1 || { dbg "exit: no git"; exit 0; }
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { dbg "exit: not a work tree"; exit 0; }

# once per session
SID=$(printf '%s' "$STDIN_DATA" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([A-Za-z0-9_-]*\)".*/\1/p' | head -1)
[ -n "$SID" ] || SID=$(git rev-parse --show-toplevel 2>/dev/null | cksum | cut -d' ' -f1)
MARKER="${TMPDIR:-/tmp}/session-recap-nudge-${SID:-fallback}"
[ -f "$MARKER" ] && { dbg "exit: already nudged ($MARKER)"; exit 0; }

# any uncommitted work at all?
[ -n "$(git status --porcelain 2>/dev/null)" ] || { dbg "exit: clean tree"; exit 0; }

# already recapped today? (recap skill writes a "## <YYYY-MM-DD ...>" heading)
TODAY=$(date -u +%F 2>/dev/null)
ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -n "$TODAY" ] && [ -f "$ROOT/SESSION-RECAP.md" ] && grep -q "^## $TODAY" "$ROOT/SESSION-RECAP.md" 2>/dev/null; then
  dbg "exit: recap already written today"; exit 0
fi

touch "$MARKER" 2>/dev/null || true
dbg "nudge: uncommitted work, no recap today"
printf '{"systemMessage": "session-recap: uncommitted work at session end — say \\"recap this session\\" to leave a dated handoff before you go."}\n'
exit 0
