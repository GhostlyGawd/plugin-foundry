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

# i154 (v10 #1): every catalog entry carries the shelf version, matching its record
python3 - << 'PY'
import json, re, pathlib
cat = json.load(open("plugins/night-clerk/data/catalog.json"))
bad = [p["name"] for p in cat["plugins"]
       if not re.match(r"^\d+\.\d+\.\d+$", p.get("version", ""))]
print("ok: every catalog entry has a semver version" if not bad
      else f"fail: entries without a semver version: {bad}")
drift = []
for p in cat["plugins"]:
    rec = pathlib.Path(f"foundry/records/{p['name']}.md").read_text()
    m = re.search(r"^version: (.+)$", rec, re.M)
    if not m or m.group(1).strip() != p.get("version"):
        drift.append(p["name"])
print("ok: catalog versions match the records" if not drift
      else f"fail: catalog version drift vs records: {drift}")
PY
