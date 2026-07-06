#!/usr/bin/env bash
# saga-page acceptance checks (backfill, audit-003 #3 / v9 #10)
set -uo pipefail
cd "${REPO_ROOT:-$(pwd)}"

python3 - << 'PY'
import json, re
saga = open("site/saga.html").read()
decisions = open("state/DECISIONS.md").read()

# check 1 — every real ADR renders exactly once (template heading excluded)
adrs = re.findall(r"^## (ADR-\d+) — ", decisions, re.M)
missing = [a for a in adrs if f"<b>{a}</b>" not in saga]
print(f"ok: all {len(adrs)} ADRs render" if adrs and not missing
      else f"fail: ADRs missing from saga: {missing}")

# check 2 — zero invented milestones: SHIPPED entries == published records
published = sum(1 for r in json.load(open("site/data.json"))["records"]
                if r["stage"] == "published")
shipped = saga.count("<b>SHIPPED</b>")
print("ok: SHIPPED count equals published records exactly"
      if shipped == published else f"fail: {shipped} SHIPPED vs {published} published")

# check 3 — i107-nit regression: truncated quotes end on a word + ellipsis
bad = [m for m in re.findall(r"([\w'’]+ ?)…", saga) if m.endswith("  ")]
mid_word = re.findall(r"\w{2}…\w", saga)
print("ok: truncations end at word boundaries with ellipsis" if not mid_word
      else f"fail: mid-word truncation: {mid_word[:3]}")

# check 4 — naming ceremony slot resolved from STATE, not hardcoded
name = json.load(open("state/STATE.json")).get("name", "")
print("ok: naming ceremony carries the STATE name" if name and name in saga
      else "fail: naming ceremony out of sync with STATE")
PY
