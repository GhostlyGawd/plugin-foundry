#!/usr/bin/env bash
# Replay proof-artifact tests (MASTER GAP-A3, ADR-031): the artifact is a
# LABELED replay of real record history — the honesty laws allow sped-up
# truth, never simulation — and the gate-block frame is present (the point).
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SVG="$REPO/foundry/assets/replay.svg"

# 1 — regenerating is deterministic (no clocks → no churn)
before=$(sha256sum "$SVG" | cut -d' ' -f1)
(cd "$REPO" && python3 tools/replay.py >/dev/null)
after=$(sha256sum "$SVG" | cut -d' ' -f1)
[ "$before" = "$after" ] && echo "ok: replay.svg deterministic (no churn)" \
                         || echo "fail: replay.svg churns on regenerate"

# 2 — the replay label + source citation are in the artifact itself
if grep -q "REPLAY · real iterations i89–i93" "$SVG" \
   && grep -q "foundry/records/starter-kits.md" "$SVG"; then
  echo "ok: labeled as a replay, cites its record"
else echo "fail: replay label/citation missing"; fi

# 3 — the gate-block frame exists and quotes the real bounce
if grep -q "GATE BLOCKS" "$SVG" && grep -q "REVIEW: bounced — multi-line kit copy-block" "$SVG"; then
  echo "ok: gate-block frame quotes the real i89 bounce"
else echo "fail: gate-block frame missing"; fi

# 4 — the quoted facts still match the record (drift guard)
if grep -q "REVIEW: bounced — multi-line kit copy-block collapses to one unrunnable line" \
     "$REPO/foundry/records/starter-kits.md"; then
  echo "ok: replay facts verified against the record"
else echo "fail: record no longer contains the quoted bounce (drift)"; fi

# 5 — 7 animated frames, SMIL (works in READMEs, no JS)
n=$(grep -o "<animate " "$SVG" | wc -l)
[ "$n" -eq 7 ] && echo "ok: 7 SMIL-animated frames" \
               || echo "fail: expected 7 animate elements, got $n"

# 6 — build ships it to the site
if [ -f "$REPO/site/replay.svg" ] && cmp -s "$SVG" "$REPO/site/replay.svg"; then
  echo "ok: build copies the artifact to site/replay.svg"
else echo "fail: site copy missing or diverged"; fi
