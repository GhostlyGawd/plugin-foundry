#!/usr/bin/env bash
# Dogfood-card tests (MASTER P1.4, ADR-031): the card's whole value is HONESTY —
# it must count genuine use (not a plugin's own construction), show 'not-yet'
# plugins instead of hiding them, and grade only published plugins.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# 1 — build/publish mentions do NOT count as dogfooding; use/friction lines do
out=$(cd "$REPO" && python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import dogfood
j_build = "## i5 — builder\n- did: built commit-craft and published commit-craft.\n"
g = dogfood.grade("commit-craft", j_build, set())
assert g["use_lines"] == 0, f"construction counted as use: {g}"
j_use = "## i9 — builder\n- did: used commit-craft to draft this commit; noted friction.\n"
g2 = dogfood.grade("commit-craft", j_use, set())
assert g2["use_lines"] == 1, f"genuine use not counted: {g2}"
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: construction ≠ dogfood; genuine use counts" \
                  || echo "fail: use-signal — $out"

# 2 — a never-used plugin is graded not-yet, shown (not hidden)
out=$(cd "$REPO" && python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
import dogfood
g = dogfood.grade("ghost-plugin", "nothing here mentions it", set())
assert g["grade"] == "not-yet" and g["score"] == 0, g
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: unused plugin graded not-yet (honest, shown)" \
                  || echo "fail: not-yet — $out"

# 3 — the real card grades exactly the published shelf, no more
out=$(cd "$REPO" && python3 - <<'PY'
import json, sys, io, contextlib; sys.path.insert(0, "tools")
import dogfood
with contextlib.redirect_stdout(io.StringIO()):
    dogfood.main(["grade"])
d = json.load(open("foundry/dogfood.json"))
carded = {c["plugin"] for c in d["cards"]}
mp = {p["name"] for p in json.load(open(".claude-plugin/marketplace.json"))["plugins"]}
# every carded plugin is a real published plugin
assert carded <= mp, carded - mp
assert len(carded) >= 10, len(carded)
# summary adds up
s = d["summary"]
assert sum(s.values()) == len(d["cards"]), s
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: card grades the real shelf; summary consistent" \
                  || echo "fail: shelf coverage — $out"

# 4 — the card renders on the site with the honesty note
python3 -c "import sys; sys.path.insert(0,'$REPO/tools'); import build; build.ROOT.__str__()" 2>/dev/null || true
(cd "$REPO" && python3 tools/build.py >/dev/null)
if grep -q 'id="dogfood"' "$REPO/site/index.html" \
   && grep -q "grades its own use of what it ships" "$REPO/site/index.html"; then
  echo "ok: dogfood card renders with the honesty framing"
else echo "fail: dogfood card not rendered"; fi
