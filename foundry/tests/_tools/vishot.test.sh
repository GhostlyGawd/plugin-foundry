#!/usr/bin/env bash
# Visual-regression tests (MASTER P4.3, ADR-031): the narration wrapper must
# describe what the window actually shows (derived from the same data.json the
# page renders), be deterministic, and the capture must degrade gracefully
# without a browser. The bought differ (Argos) is config-gated.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"

# 1 — narration derives from data.json and matches the quality number
(cd "$REPO" && python3 tools/vishot.py narrate >/dev/null)
N="$REPO/foundry/assets/shots/narration.md"
pct=$(python3 -c "import json; print(json.load(open('$REPO/site/data.json'))['quality']['qa_first_try_pct'])")
if grep -q "${pct}% passed QA first try" "$N" && grep -q "plugins shipped" "$N"; then
  echo "ok: narration reflects the live quality number ($pct%)"
else echo "fail: narration doesn't match data.json"; fi

# 2 — deterministic: two runs produce identical narration
a=$(cd "$REPO" && python3 tools/vishot.py narrate >/dev/null; sha256sum "$N" | cut -d' ' -f1)
b=$(cd "$REPO" && python3 tools/vishot.py narrate >/dev/null; sha256sum "$N" | cut -d' ' -f1)
[ "$a" = "$b" ] && echo "ok: narration is deterministic" || echo "fail: narration churns"

# 3 — narration lists the real published shelf
n_pub=$(python3 -c "import json; d=json.load(open('$REPO/site/data.json')); print(sum(1 for r in d['records'] if r.get('stage')=='published' and r.get('kind','plugin')=='plugin'))")
grep -q "Shelf: ${n_pub} published plugins" "$N" \
  && echo "ok: narration counts the real shelf ($n_pub)" \
  || echo "fail: shelf count mismatch"

# 4 — capture degrades gracefully when node/browser is absent
out=$(cd "$REPO" && PATH="/usr/bin:/bin" python3 tools/vishot.py shoot 2>&1 || true)
if echo "$out" | grep -qiE "no browser|skip|captured [0-9]"; then
  echo "ok: capture degrades gracefully without a browser"
else echo "fail: capture didn't degrade — $out"; fi

# 5 — PNGs are gitignored (not committed — Argos stores baselines), narration IS tracked
if grep -q "foundry/assets/shots/\*.png" "$REPO/.gitignore"; then
  echo "ok: screenshots gitignored (bought differ owns baselines)"
else echo "fail: PNGs not gitignored — would bloat the repo"; fi

# 6 — Argos config present + desk-gated
if [ -f "$REPO/argos.config.json" ] && grep -q "Argos" "$REPO/state/DESK.jsonl"; then
  echo "ok: argos config-ready + install desk-gated"
else echo "fail: argos config or desk item missing"; fi
