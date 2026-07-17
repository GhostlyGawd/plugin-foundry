#!/usr/bin/env bash
# Postmortem tests (MASTER P5.4, ADR-031): the trust artifact must be real
# (a genuine incident, cited), blameless, and complete (the "why it looked fine"
# section is the load-bearing one). The agent manifest must be contract-valid.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
PM="$REPO/reviews/postmortems/pm-001-token-rejection.md"

# 1 — the manifest is contract-valid and in the registry (proposes/high/event)
out=$(cd "$REPO" && python3 - <<'PY'
import json, sys; sys.path.insert(0, "tools")
from lib import load_agents
errs = []
agents = {a["id"]: a for a in load_agents(errs)}
assert not errs, errs
a = agents["postmortem"]
assert a["capability"] == "proposes" and a["quota_tier"] == "high" and a["trigger"] == "event", a
reg = {x["id"] for x in json.load(open("foundry/agents/registry.json"))["agents"]}
assert "postmortem" in reg
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: postmortem manifest contract-valid, in registry" \
                  || echo "fail: manifest — $out"

# 2 — pm-001 has every required section (esp. the silent-failure one)
missing=""
for sec in "## Summary" "## Timeline" "## Why it looked fine" "## Root cause" "## The fix" "## Runbook delta" "## Lesson"; do
  grep -qF "$sec" "$PM" || missing="$missing '$sec'"
done
[ -z "$missing" ] && echo "ok: pm-001 has all required sections" \
                  || echo "fail: pm-001 missing:$missing"

# 3 — it cites the real incident (the token, the fix ADR)
if grep -q "CLAUDE_CODE_OAUTH_TOKEN" "$PM" && grep -q "AUTH-1" "$PM" && grep -q "2026-07-07" "$PM"; then
  echo "ok: pm-001 cites the real incident + the fix (AUTH-1)"
else echo "fail: pm-001 not grounded in the real incident"; fi

# 4 — blameless: no person/agent blamed (the discipline)
if grep -iqE "\b(fault of|blame|culprit|screwed up|incompetent|stupid)\b" "$PM"; then
  echo "fail: postmortem contains blame language"
else echo "ok: postmortem is blameless"; fi

# 5 — the runbook carries the interactive-only remediation without erasing history
if grep -q "A model workflow or headless runner was enabled" "$REPO/RUNBOOK.md" \
   && grep -q "PM-001 remains the historical record" "$REPO/RUNBOOK.md" \
   && grep -q "no reusable model credential belongs in GitHub" "$REPO/RUNBOOK.md"; then
  echo "ok: RUNBOOK has current interactive-only remediation + historical context"
else echo "fail: runbook delta missing"; fi

# 6 — the lesson is a closed loop: pm-001 cites m-001, and m-001 exists in the
#     factory brain carrying the same silent-failure insight
out=$(cd "$REPO" && python3 - <<'PY'
import json, re
pm = open("reviews/postmortems/pm-001-token-rejection.md").read()
assert re.search(r"\bm-001\b", pm), "postmortem doesn't cite its memory id"
mem = {json.loads(l)["id"]: json.loads(l)["lesson"]
       for l in open("foundry/memory.jsonl") if l.strip()}
assert "m-001" in mem, "m-001 not in memory"
low = mem["m-001"].lower()
assert "auth" in low and ("silent" in low or "streak" in low or "reports success" in low), low
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: pm-001 ↔ m-001 closed loop (postmortem cites the seeded lesson)" \
                  || echo "fail: lesson linkage — $out"
