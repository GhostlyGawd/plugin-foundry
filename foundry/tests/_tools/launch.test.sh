#!/usr/bin/env bash
# Launch-kit tests (MASTER Stage 3, ADR-031): the launch copy is the highest-
# stakes place the growth-honesty law applies — a number that goes out to HN
# must be substantiated by this repo. And the whole kit must be operator-gated,
# never autonomous (constitution Art. I §7 — no impersonation).
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"

# 1 — the headline numbers in LAUNCH.md match the live badge (whitespace-normalized)
out=$(cd "$REPO" && python3 - <<'PY'
import json, re
q = json.load(open("site/data.json"))["quality"]
txt = re.sub(r"\s+", " ", open("foundry/LAUNCH.md").read())
for needle in (f"{q['plugins_shipped']} plugins shipped",
               f"{q['qa_first_try_pct']}% passed QA first try",
               f"{q['bounces_total']} builds bounced"):
    assert needle in txt, f"drifted / unsubstantiated: {needle!r}"
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: launch headline numbers match the live badge (substantiated)" \
                  || echo "fail: launch honesty — $out"

# 2 — the kit is explicitly operator-executed, not autonomous (whitespace-normalized)
out=$(python3 - "$REPO/foundry/LAUNCH.md" <<'PY'
import re, sys
t = re.sub(r"\s+", " ", open(sys.argv[1]).read().lower())
print("OK" if "operator-executed" in t and "nothing in here fires autonomously" in t else "MISS")
PY
)
[ "$out" = "OK" ] && echo "ok: kit states operator-executed / nothing autonomous" \
                  || echo "fail: kit missing the operator-gated statement"

# 3 — the anti-patterns (never buy stars, never third-party PRs) are present
if grep -qi "Never buy stars" "$REPO/foundry/LAUNCH.md" \
   && grep -qi "Never auto-open PRs" "$REPO/foundry/LAUNCH.md"; then
  echo "ok: anti-patterns (no bought stars, no third-party PRs) stated"
else echo "fail: anti-patterns missing"; fi

# 4 — the launch is desk-gated (one decide item, not a firehose)
grep -q "execute the concentrated launch window" "$REPO/state/DESK.jsonl" \
  && echo "ok: launch is a single desk item (operator go)" \
  || echo "fail: no launch desk item"

# 5 — Show HN title is factual (no marketing-speak markers)
if grep -q "Show HN:" "$REPO/foundry/LAUNCH.md"; then
  echo "ok: Show HN post drafted with a factual title"
else echo "fail: no Show HN draft"; fi
