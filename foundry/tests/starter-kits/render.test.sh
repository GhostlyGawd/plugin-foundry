#!/usr/bin/env bash
# starter-kits acceptance checks (record: foundry/records/starter-kits.md)
# 1. copy-block pastes one command per line (i89 bounce regression)
# 2. members carry honest stage/published flags; published members are real marketplace entries
# 3. validator law: unknown kit member fails validate
set -uo pipefail
cd "${REPO_ROOT:-$(pwd)}"

# check 1 — kit copy-blocks must not inherit the shelf's nowrap (i89 bounce)
if grep -q '.kit .install{white-space:pre}' site/index.html; then
  echo "ok: kit copy-block renders one command per line (white-space:pre)"
else
  echo "fail: kit install block missing white-space:pre override — multi-line paste breaks"
fi

python3 - << 'PY'
import json, sys
data = json.load(open("site/data.json"))
mp = {p["name"] for p in json.load(open(".claude-plugin/marketplace.json"))["plugins"]}
kits = data.get("kits", [])
if not kits:
    print("fail: no kits in data.json"); sys.exit(0)
bad = []
for k in kits:
    for m in k.get("members", []):
        if not {"name", "title", "stage", "published"} <= set(m):
            bad.append(f"{k['id']}/{m.get('name')}: missing keys")
        elif m["published"] and m["name"] not in mp:
            bad.append(f"{k['id']}/{m['name']}: published=true but not in marketplace.json")
        elif not m["published"] and m["name"] in mp:
            bad.append(f"{k['id']}/{m['name']}: published=false but IS in marketplace.json")
print("fail: " + "; ".join(bad) if bad else "ok: kit members honest — flags match marketplace.json")

# check 3 — validator rejects a kit naming a plugin that has no record
import pathlib, shutil, tempfile
sys.path.insert(0, "tools")
import validate as v
tmp = pathlib.Path(tempfile.mkdtemp())
(tmp / "foundry").mkdir()
(tmp / "foundry" / "kits.json").write_text(json.dumps(
    {"kits": [{"id": "bogus", "plugins": ["no-such-plugin"]}]}))
old_root, v.ROOT = v.ROOT, tmp
errors = []
v.check_kits({"plugin-smith": {}}, errors)
v.ROOT = old_root
shutil.rmtree(tmp)
print("ok: validator fails unknown kit member" if errors else
      "fail: validator accepted a kit with an unknown member")
PY
