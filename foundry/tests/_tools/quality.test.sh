#!/usr/bin/env bash
# Quality-number tests (MASTER GAP-A, ADR-031): the headline stat is computed
# only from what the repo substantiates — Test logs, Review logs, the journal,
# the ledger. A fake number here is red-build severity (growth-honesty law).
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# 1 — real repo: shipped == marketplace plugin count (the shelf is the truth)
out=$(cd "$REPO" && python3 - <<'PY'
import json
q = json.load(open("site/data.json"))["quality"]
mp = json.load(open(".claude-plugin/marketplace.json"))
assert q["plugins_shipped"] == len(mp["plugins"]), (q["plugins_shipped"], len(mp["plugins"]))
assert q["qa_first_try_pct"] is None or 0 <= q["qa_first_try_pct"] <= 100
assert q["iterations"] > 0
assert q["bounces_total"] >= 5  # append-only history: bounces never vanish
print("OK")
PY
) && echo "ok: real-repo quality substantiated (shipped==marketplace, bounces kept)" \
  || echo "fail: real-repo quality — $out"

# 2 — badge endpoint is valid shields.io schema
out=$(cd "$REPO" && python3 - <<'PY'
import json
b = json.load(open("site/quality.json"))
assert b["schemaVersion"] == 1 and b["label"] and b["message"]
print("OK")
PY
) && echo "ok: quality.json is a valid shields endpoint" \
  || echo "fail: badge schema — $out"

# 3 — fixture semantics: a review bounce disqualifies first-try; totals honest
FX="$WORK/fx"
mkdir -p "$FX/foundry/records" "$FX/state" "$FX/site"
cat > "$FX/foundry/records/clean.md" <<'R'
---
name: clean
stage: published
kind: plugin
---
## Test log
TEST VERDICT: pass
## Review log
REVIEW: approved
R
cat > "$FX/foundry/records/bounced.md" <<'R'
---
name: bounced
stage: published
kind: plugin
---
## Test log
TEST VERDICT: pass
## Review log
REVIEW: bounced — fix the thing
REVIEW: approved
R
printf '## i1 — builder — t\n- did: x\n## i2 — qa — t\n- did: y\n' > "$FX/state/JOURNAL.md"
printf '{"ts":"2026-07-12T00:00:00Z","kind":"quota_run"}\n{"ts":"2026-07-12T01:00:00Z","cost_usd":1.5,"usage":{}}\n' > "$FX/state/BUDGET.jsonl"
out=$(cd "$REPO" && python3 - "$FX" <<'PY'
import sys, json
from pathlib import Path
sys.path.insert(0, "tools")
import build
fx = Path(sys.argv[1])
build.ROOT = fx
build.RECORDS = fx / "foundry" / "records"
q = build.build_quality([])
assert q["plugins_shipped"] == 2, q
assert q["qa_first_try_pct"] == 50, q          # bounced.md disqualified
assert q["bounces_total"] == 1, q
assert q["iterations"] == 2, q
assert q["ci_shifts"] == 2 and q["api_spend_usd"] == 1.5, q
badge = json.load(open(fx / "site" / "quality.json"))
assert "50% first-try QA" in badge["message"], badge
print("OK")
PY
) && echo "ok: fixture semantics — review bounce disqualifies first-try (50%)" \
  || echo "fail: fixture semantics — $out"
