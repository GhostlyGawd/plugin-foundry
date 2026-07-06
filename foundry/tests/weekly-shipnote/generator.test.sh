#!/usr/bin/env bash
# weekly-shipnote acceptance checks (record: foundry/records/weekly-shipnote.md)
# Runs the generator against FIXTURE repos so results don't drift with the live journal.
set -uo pipefail
cd "${REPO_ROOT:-$(pwd)}"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

mkfix() { # mkfix <name> — skeleton repo with tools/shipnote.py
  local d="$WORK/$1"
  mkdir -p "$d/tools" "$d/state" "$d/.claude-plugin" "$d/foundry/records"
  cp tools/shipnote.py "$d/tools/"
  echo '{"name":"foundry","plugins":[]}' > "$d/.claude-plugin/marketplace.json"
  echo "$d"
}
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TODAY=$(date -u +%Y-%m-%d)

# 1 — busy fixture: 14 moves + a fresh published plugin → all sections, pointer line
d=$(mkfix busy)
{ for n in $(seq 1 14); do printf '## i%s — builder — %s\n- line: thing-%s: idea → spec\n\n' "$n" "$NOW" "$n"; done; } > "$d/state/JOURNAL.md"
printf -- '---\nname: demo-plug\ntitle: Demo Plug\nstage: published\nkind: plugin\nversion: 0.1.0\nupdated: %s\n---\n' "$TODAY" > "$d/foundry/records/demo-plug.md"
out=$(cd "$d" && PATH=/usr/bin:/bin python3 tools/shipnote.py 2>/dev/null)
echo "$out" | grep -q '## Shipped' && echo "$out" | grep -q 'demo-plug@foundry' \
  && echo "$out" | grep -q '…and 2 earlier move(s)' \
  && echo "ok: check1 busy week — sections + honest truncation pointer" \
  || { echo "fail: check1 — $out"; }

# 2 — quiet fixture: empty journal → honest quiet copy, no pointer
d=$(mkfix quiet); : > "$d/state/JOURNAL.md"
out=$(cd "$d" && PATH=/usr/bin:/bin python3 tools/shipnote.py 2>/dev/null)
echo "$out" | grep -q '_a quiet week_' && echo "$out" | grep -q '_nothing this week' \
  && ! echo "$out" | grep -q 'earlier move' \
  && echo "ok: check2 quiet week honest, no phantom pointer" \
  || echo "fail: check2 — $out"

# 3 — exactly 12 moves → no pointer (boundary)
d=$(mkfix twelve)
{ for n in $(seq 1 12); do printf '## i%s — builder — %s\n- line: t%s: idea → spec\n\n' "$n" "$NOW" "$n"; done; } > "$d/state/JOURNAL.md"
out=$(cd "$d" && PATH=/usr/bin:/bin python3 tools/shipnote.py 2>/dev/null)
! echo "$out" | grep -q 'earlier move' && echo "ok: check3 boundary — 12 moves, no pointer" \
  || echo "fail: check3 — pointer fired at exactly 12"

# 4 — workflow guards: duplicate-week gate + ensure-label before create
if grep -q 'gh issue list --label shipnote --state all --search "Shipnote $WEEK"' .github/workflows/shipnote.yml \
   && grep -q 'gh label create shipnote' .github/workflows/shipnote.yml; then
  A=$(grep -n 'gh label create shipnote' .github/workflows/shipnote.yml | cut -d: -f1)
  B=$(grep -n 'gh issue create' .github/workflows/shipnote.yml | cut -d: -f1)
  [ "$A" -lt "$B" ] && echo "ok: check4 duplicate-week gate + label ensured before create" \
    || echo "fail: check4 — label created after issue create"
else
  echo "fail: check4 — workflow guards missing"
fi
