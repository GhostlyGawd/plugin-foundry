#!/usr/bin/env bash
# night-clerk snapshot-freshness regression (v9 #2, i138)
set -uo pipefail
cd "${REPO_ROOT:-$(pwd)}"


# i138 (v9 #2) regression: the bundled snapshot may never trail the shelf
python3 - << 'PY'
import json
mp = {p["name"] for p in json.load(open(".claude-plugin/marketplace.json"))["plugins"]}
cat = json.load(open("plugins/night-clerk/data/catalog.json"))
snap = {p["name"] for p in cat["plugins"]}
missing = mp - snap
ghosts = snap - mp
print("ok: snapshot covers every published plugin" if not missing and not ghosts
      else f"fail: snapshot drift — missing={sorted(missing)} ghosts={sorted(ghosts)}")
# kits: only real, published members may render as installable
bad = [k["id"] for k in cat.get("kits", [])
       if any(line.split()[2].split("@")[0] not in snap for line in k["install"])]
print("ok: kit install lines are published-members-only" if not bad
      else f"fail: kit(s) with unpublished members: {bad}")
PY
