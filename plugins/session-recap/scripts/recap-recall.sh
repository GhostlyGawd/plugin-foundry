#!/usr/bin/env bash
# session-recap SessionStart hook: if a SESSION-RECAP.md exists, surface the most
# recent handoff's title so the next session picks up where the last left off.
# Contract: exit 0 ALWAYS; read-only; no network; silent when no recap file
# exists or with SESSION_RECAP_SILENT=1. The `recap` skill reads the full section.
set -u
exec 2>/dev/null || true
trap 'exit 0' ERR

[ "${SESSION_RECAP_SILENT:-}" = "1" ] && exit 0

STDIN_DATA=$(cat 2>/dev/null || true)
ROOT=$(printf '%s' "$STDIN_DATA" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
{ [ -n "$ROOT" ] && [ -d "$ROOT" ]; } || ROOT="$PWD"

FILE="$ROOT/SESSION-RECAP.md"
[ -f "$FILE" ] || exit 0

# last "## " heading = most recent handoff (recap appends, newest last)
TITLE=$(grep -n '^## ' "$FILE" 2>/dev/null | tail -1 | sed 's/^[0-9]*:## *//')
[ -n "$TITLE" ] || exit 0

# JSON-escape (quotes + backslashes; the title is repo-authored text)
esc=$(printf '%s' "$TITLE" | sed 's/\\/\\\\/g; s/"/\\"/g')
printf '{"systemMessage": "session-recap: last handoff — %s. Say \\"where did we leave off?\\" to read the full recap."}\n' "$esc"
exit 0
