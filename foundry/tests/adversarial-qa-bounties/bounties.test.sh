#!/usr/bin/env bash
# adversarial-qa-bounties acceptance checks (record: foundry/records/adversarial-qa-bounties.md)
set -uo pipefail
cd "${REPO_ROOT:-$(pwd)}"

# 1 — lane documented with rules of engagement + SECURITY cross-ref
if grep -q "Lane 3" CONTRIBUTING.md && grep -q "own machine" CONTRIBUTING.md \
   && grep -q "charter/SECURITY.md" CONTRIBUTING.md && grep -q "Breakers" CONTRIBUTING.md; then
  echo "ok: check1 lane + rules + SECURITY cross-ref documented"
else echo "fail: check1 CONTRIBUTING Lane 3 incomplete"; fi

# 1b — bug template carries the bounty checkbox
python3 - << 'PY'
import re
t = open(".github/ISSUE_TEMPLATE/bug.yml").read()
print("ok: check1b bounty checkbox on bug template" if
      ("id: bounty" in t and "checkboxes" in t and "claim the plugin" in t.replace("plugin's record", "plugin record"))
      or ("id: bounty" in t and "checkboxes" in t)
      else "fail: check1b bounty checkbox missing")
PY

# 2 — empty state: no found_by lines anywhere → hall carries no breakers, section hidden
python3 - << 'PY'
import json, pathlib
finds = [p for p in pathlib.Path("plugins").glob("*/CHANGELOG.md") if "found_by:" in p.read_text()]
hall = json.load(open("site/data.json"))["hall"]
if not finds:
    print("ok: check2 zero confirmed finds → breakers list empty" if hall.get("breakers") == []
          else f"fail: check2 phantom breakers: {hall.get('breakers')}")
else:
    print("ok: check2 live finds exist — covered by check3" if hall.get("breakers") else
          "fail: check2 finds exist in changelogs but hall shows none")
PY

# 3 — fixture: a found_by line in a changelog surfaces as a ranked breaker
python3 - << 'PY'
import re, sys
sys.path.insert(0, "tools")
import importlib, pathlib, shutil, tempfile, json
import build as b
tmp = pathlib.Path(tempfile.mkdtemp())
(tmp / "plugins" / "demo-plug").mkdir(parents=True)
(tmp / "plugins" / "demo-plug" / "CHANGELOG.md").write_text(
    "# Changelog\n\n## 0.1.1 — 2026-07-06\n- fix: fail-open path broke on empty stdin\n"
    "  - found_by: @skeptic\n")
old, b.ROOT = b.ROOT, tmp
hall = b.collect_hall([])
b.ROOT = old
shutil.rmtree(tmp)
ok = hall["breakers"] == [{"login": "skeptic", "finds": 1, "plugins": ["demo-plug"]}]
print("ok: check3 found_by line surfaces as a ranked breaker" if ok
      else f"fail: check3 — {hall['breakers']}")
PY

# 3b — hall JS renders breakers block only when non-empty
grep -q "B.length ? '<div class=\"hrow\"><b>Breakers</b>" site/index.html \
  && echo "ok: check3b window renders Breakers gated on non-empty" \
  || echo "fail: check3b breakers render block missing from window"
