#!/usr/bin/env bash
# Content-generation tests (MASTER P1.1/P4.2/P5.5, ADR-031): the halo content
# engine. Every generator must produce substantiated content (growth-honesty),
# be deterministic, and the two new agents must be contract-valid.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
(cd "$REPO" && python3 tools/build.py >/dev/null)

# 1 — briefing carries the live number + ranked desk items, reads short
out=$(cd "$REPO" && python3 tools/briefing.py)
pct=$(python3 -c "import json;print(json.load(open('$REPO/site/data.json'))['quality']['qa_first_try_pct'])")
if echo "$out" | grep -q "${pct}% first-try QA" && echo "$out" | grep -q "The desk"; then
  echo "ok: briefing shows the live number + the desk"
else echo "fail: briefing — $out"; fi

# 2 — shipnote --social is one substantiated post; weekly still works (regression)
soc=$(cd "$REPO" && python3 tools/shipnote.py --social)
if echo "$soc" | grep -q "first-try QA" && echo "$soc" | grep -q "#ClaudeCode" \
   && [ "$(printf '%s' "$soc" | wc -l)" -le 1 ]; then
  echo "ok: shipnote --social is one substantiated post"
else echo "fail: social — $soc"; fi
# capture fully first (a piped grep -q closes the pipe early → SIGPIPE under pipefail)
weekly=$(cd "$REPO" && python3 tools/shipnote.py 2>/dev/null)
echo "$weekly" | grep -q "^# Shipnote" \
  && echo "ok: weekly shipnote regression intact" || echo "fail: weekly shipnote broke"

# 3 — quarterly cites real movement + names failures honestly
q=$(cd "$REPO" && python3 tools/quarterly.py 2>/dev/null)
if echo "$q" | grep -q "bounced by QA/review" && echo "$q" | grep -qi "postmortem" \
   && echo "$q" | grep -q "Recommendations"; then
  echo "ok: quarterly names failures + lands recommendations"
else echo "fail: quarterly — $q"; fi

# 4 — quarterly's recommendations dedup at the desk (run twice, no doubling)
before=$(grep -c '"kind": "decide"' "$REPO/state/DESK.jsonl" 2>/dev/null || echo 0)
(cd "$REPO" && python3 tools/quarterly.py >/dev/null 2>&1)
after=$(grep -c '"kind": "decide"' "$REPO/state/DESK.jsonl" 2>/dev/null || echo 0)
[ "$before" = "$after" ] && echo "ok: quarterly recs dedup at the desk (no firehose)" \
                         || echo "fail: quarterly duplicated desk items ($before→$after)"

# 5 — briefing + quarterly agents are contract-valid and in the registry
out=$(cd "$REPO" && python3 - <<'PY'
import json, sys; sys.path.insert(0, "tools")
from lib import load_agents
errs = []; a = {x["id"]: x for x in load_agents(errs)}
assert not errs, errs
for aid in ("briefing", "quarterly"):
    assert a[aid]["capability"] == "read_only" and a[aid]["quota_tier"] == "low", a[aid]
reg = {x["id"] for x in json.load(open("foundry/agents/registry.json"))["agents"]}
assert {"briefing", "quarterly"} <= reg, reg
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: briefing + quarterly agents contract-valid, in registry" \
                  || echo "fail: manifests — $out"

# 6 — determinism: briefing twice = identical
a=$(cd "$REPO" && python3 tools/briefing.py); b=$(cd "$REPO" && python3 tools/briefing.py)
[ "$a" = "$b" ] && echo "ok: briefing deterministic" || echo "fail: briefing churns"
