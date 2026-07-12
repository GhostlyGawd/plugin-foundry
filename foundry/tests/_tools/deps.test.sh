#!/usr/bin/env bash
# Dependency-hygiene config tests (MASTER P3.2 + GAP-D, ADR-031): the bought
# configs must be well-formed and carry the cooldown + no-automerge guards that
# are the whole point (auto-merging a fresh release is a documented malware
# vector). A malformed config that GitHub silently ignores would be worse than none.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"

# 1 — dependabot.yml parses and carries a cooldown + weekly grouping
out=$(python3 - "$REPO/.github/dependabot.yml" <<'PY'
import sys, yaml
d = yaml.safe_load(open(sys.argv[1]))
u = d["updates"][0]
assert u["package-ecosystem"] == "github-actions", u
assert "cooldown" in u, "GAP-D: dependabot must carry a cooldown"
assert u["schedule"]["interval"] == "weekly", "grouped weekly, not a firehose"
assert "groups" in u, "bumps must group into one PR"
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: dependabot.yml valid — cooldown + weekly grouping" \
                  || echo "fail: dependabot — $out"

# 2 — renovate.json is valid JSON and enforces cooldown + no automerge (GAP-D)
out=$(python3 - "$REPO/renovate.json" <<'PY'
import sys, json
d = json.load(open(sys.argv[1]))
assert d["minimumReleaseAge"].startswith("5"), "GAP-D: 5-day cooldown"
rules = d["packageRules"]
assert any(r.get("automerge") is False for r in rules), "nothing auto-merges (constitution)"
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: renovate.json valid — 5-day cooldown, no automerge" \
                  || echo "fail: renovate — $out"

# 3 — socket.yml parses and blocks the high-risk behaviors
out=$(python3 - "$REPO/socket.yml" <<'PY'
import sys, yaml
d = yaml.safe_load(open(sys.argv[1]))
r = d["issueRules"]
assert r["malware"]["action"] == "error", "malware must block"
assert r["installScripts"]["action"] == "error", "install scripts must block"
assert r["typosquat"]["action"] == "error", "typosquats must block"
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: socket.yml valid — malware/install-scripts/typosquat blocked" \
                  || echo "fail: socket — $out"

# 4 — the app-install half is desk-gated, not silently assumed active
grep -q "Renovate + Socket" "$REPO/state/DESK.jsonl" \
  && echo "ok: app-install desk item queued (not assumed live)" \
  || echo "fail: no desk item for the app installs"
