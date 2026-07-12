#!/usr/bin/env bash
# Desk v2 tests (MASTER P0.8, ADR-029): one ranked queue, one delivery,
# nothing requiring approval ever auto-merges (that half is pinned by the
# orchestrator suite). Here: ranking law, dedup, render, gh-less degradation,
# and the public desk page.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

FX="$WORK/fx"
mkdir -p "$FX/tools" "$FX/state"
cp "$REPO"/tools/desk.py "$FX/tools/"

D() { (cd "$FX" && python3 tools/desk.py "$@" 2>&1); }

# seed via the module (uses _append directly to control timestamps)
python3 - "$FX" <<'PY'
import sys, os
sys.path.insert(0, os.path.join(sys.argv[1], "tools"))
import desk
L = os.path.join(sys.argv[1], "state", "DESK.jsonl")
desk._append({"id": "d-0001", "ts": "2026-06-01T00:00:00Z", "kind": "decide",
              "title": "old naming question", "status": "open"}, L)
desk._append({"id": "d-0002", "ts": "2026-07-12T00:00:00Z", "kind": "approve",
              "title": "fresh approval", "status": "open"}, L)
desk._append({"id": "d-0003", "ts": "2026-07-12T00:00:00Z", "kind": "alarm",
              "title": "fresh alarm", "status": "open"}, L)
desk._append({"id": "d-0004", "ts": "2026-07-10T00:00:00Z", "kind": "ratify",
              "title": "law-book change", "status": "open"}, L)
PY

# 1 — ranking law: kind strictly dominates — alarm > ratify > approve > decide,
#     regardless of age (the 41-day-old decide still ranks LAST)
order=$(D queue | grep -o 'd-000[0-9]' | head -4 | tr '\n' ' ')
[ "$order" = "d-0003 d-0004 d-0002 d-0001 " ] \
  && echo "ok: ranking law (kind strictly dominates; age orders within kind only)" \
  || echo "fail: ranking — got $order"

# 2 — resolved items leave the queue
(cd "$FX" && python3 tools/desk.py resolve d-0003 approved --note done >/dev/null)
D queue | grep -q "d-0003" && echo "fail: resolved item still queued" \
                           || echo "ok: resolved items leave the queue"

# 3 — dedup: same (kind,title) while open returns the same id, no new line
n_before=$(grep -c 'd-' "$FX/state/DESK.jsonl")
out=$(D add --kind ratify --title "law-book change")
n_after=$(grep -c 'd-' "$FX/state/DESK.jsonl")
if echo "$out" | grep -q "already open d-0004" && [ "$n_before" -eq "$n_after" ]; then
  echo "ok: open-item dedup returns the existing id"
else echo "fail: dedup — $out"; fi

# 4 — the render carries the resolve instruction (the operator can act from it)
D queue | grep -q "tools/desk.py resolve" \
  && echo "ok: queue render tells the operator how to resolve" \
  || echo "fail: render lacks the resolve instruction"

# 5 — sync degrades to a log line without gh (ledger stays source of truth)
out=$(cd "$FX" && PATH="/usr/bin:/bin" python3 tools/desk.py sync 2>&1)
echo "$out" | grep -q "ledger-only" \
  && echo "ok: sync degrades gracefully without gh" \
  || echo "fail: gh-less sync — $out"

# 6 — the public desk page lists open items and hides resolved ones
out=$(cd "$REPO" && python3 - <<'PY'
from pathlib import Path
page = Path("site/desk.html").read_text()
import json
items = {}
for line in Path("state/DESK.jsonl").read_text().splitlines():
    rec = json.loads(line)
    items[rec["id"]] = {**items.get(rec["id"], {}), **rec}
open_ids = [i for i, it in items.items() if it.get("status") == "open"]
missing = [i for i in open_ids if i not in page]
resolved_shown = [i for i, it in items.items()
                  if it.get("status") != "open" and f">{i}<" in page]
print("OK" if not missing and not resolved_shown else f"missing={missing} shown={resolved_shown}")
PY
)
[ "$out" = "OK" ] && echo "ok: site/desk.html shows open items only" \
                  || echo "fail: desk page — $out"
