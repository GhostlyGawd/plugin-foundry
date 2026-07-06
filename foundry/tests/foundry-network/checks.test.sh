#!/usr/bin/env bash
# foundry-network acceptance checks 1–3 (record: foundry/records/foundry-network.md)
set -uo pipefail
cd "${REPO_ROOT:-$(pwd)}"

# 1 — empty network renders nothing anywhere
python3 - << 'PY'
import json
d = json.load(open("site/data.json"))
net = json.load(open("foundry/network.json")).get("network", [])
if net:
    print("skip: check1 network no longer empty — rendering covered by check1b below")
else:
    s = open("site/saga.html").read()
    ok = d.get("network") == [] and "Family tree" not in s
    print(("ok: " if ok else "fail: ") + "check1 empty network renders nothing (data empty, saga section absent)")
PY

# 1b — a fixture entry flows to both surfaces, then is fully restored
python3 - << 'PY'
import json, pathlib, subprocess
reg = pathlib.Path("foundry/network.json"); orig = reg.read_text()
try:
    reg.write_text(json.dumps({"network": [{"name": "QA Fixture Forge", "url": "https://example.invalid/forge",
                                            "pages": "", "registered": "2026-07-06", "note": "fixture"}]}))
    subprocess.run(["python3", "tools/build.py"], check=True, capture_output=True)
    d = json.load(open("site/data.json")); s = open("site/saga.html").read()
    ok = d["network"][0]["name"] == "QA Fixture Forge" and "Family tree" in s and "QA Fixture Forge" in s
    print(("ok: " if ok else "fail: ") + "check1b fixture sister reaches window data + saga tree")
finally:
    reg.write_text(orig)
    subprocess.run(["python3", "tools/build.py"], check=True, capture_output=True)
PY

# 2 — registration path documented with verification duty
grep -q "sister-foundry" .github/ISSUE_TEMPLATE/sister-foundry.yml 2>/dev/null || [ -f .github/ISSUE_TEMPLATE/sister-foundry.yml ] \
  && echo "ok: check2a issue template exists" || echo "fail: check2a issue template missing"
grep -q "LOOP.md" .github/ISSUE_TEMPLATE/sister-foundry.yml && grep -qi "verifies\|verification" .github/ISSUE_TEMPLATE/sister-foundry.yml \
  && echo "ok: check2b template states the verification duty" || echo "fail: check2b verification duty not in template"
grep -q "Lane 4" CONTRIBUTING.md && grep -A10 "Lane 4" CONTRIBUTING.md | grep -q "foundry/records" \
  && echo "ok: check2c CONTRIBUTING Lane 4 carries the duty" || echo "fail: check2c Lane 4 missing or duty absent"

# 3 — links out only: the renderer never fetches; entries carry no remote content fields
python3 - << 'PY'
import re
src = open("tools/build.py").read()
m = re.search(r"function renderNetwork\(\).*?\n}", src, re.S)
body = m.group(0) if m else ""
bad = any(tok in body for tok in ("fetch(", "XMLHttpRequest", "iframe"))
print(("ok: " if body and not bad else "fail: ") + "check3 renderNetwork links out only (no fetch/iframe)")
PY
