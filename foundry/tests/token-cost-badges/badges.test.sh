#!/usr/bin/env bash
# token-cost-badges acceptance checks (record: foundry/records/token-cost-badges.md)
# 1. estimator deterministic per published plugin
# 2. badge states honest: est-labeled when measured, "unmeasured" otherwise
# 3. stale (>60d) verified dates dim — i94 bounce regression
set -uo pipefail
cd "${REPO_ROOT:-$(pwd)}"

python3 - << 'PY'
import json, subprocess, sys

# check 1 — estimator stable: two runs, same numbers, for every published plugin
mp = [p["name"] for p in json.load(open(".claude-plugin/marketplace.json"))["plugins"]]
bad = []
for name in mp:
    runs = [json.loads(subprocess.run(["python3", "tools/tokencost.py", name],
            capture_output=True, text=True).stdout)["always_on_tokens_est"] for _ in (1, 2)]
    if runs[0] != runs[1] or not isinstance(runs[0], int) or runs[0] < 0:
        bad.append(f"{name}: {runs}")
print("fail: estimator unstable — " + "; ".join(bad) if bad else
      f"ok: estimator deterministic for all {len(mp)} published plugins")

# check 2 — data.json only carries numbers the records substantiate
data = {e["name"]: e for e in json.load(open("site/data.json"))["records"]}
import re, pathlib
lied = []
for name, e in data.items():
    rec = pathlib.Path(f"foundry/records/{name}.md").read_text().split("---")[1]
    m = re.search(r"^always_on_tokens:\s*(\d+)", rec, re.M)
    rec_val = int(m.group(1)) if m else None
    site_raw = e.get("always_on_tokens")
    site_val = int(site_raw) if site_raw not in (None, "") else None
    if site_val != rec_val:
        lied.append(f"{name}: site says {e.get('always_on_tokens')}, record says {rec_val}")
print("fail: unsubstantiated badge — " + "; ".join(lied) if lied else
      "ok: every badge number traces to its record")

# check 3 — stale logic present and thresholded at 60 days (i94 bounce)
idx = open("site/index.html").read()
if "60*86400000" in idx and ".chip.tok.stale{opacity:.5}" in idx and "older than 60 days" in idx:
    print("ok: >60-day verified dates dim with explanatory title")
else:
    print("fail: stale-verified dimming missing or threshold changed silently")
PY
