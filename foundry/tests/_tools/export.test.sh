#!/usr/bin/env bash
# Multi-harness export tests (MASTER GAP-C, ADR-031): the exporter must extract
# the portable core of a real plugin, name adapter targets for the other
# harnesses, and NEVER touch the published plugin (names/versions are forever).
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

# 1 — exporting a real plugin yields its portable skills + version
out=$(cd "$REPO" && python3 tools/export.py commit-craft --out "$WORK/dist")
p="$WORK/dist/commit-craft/portable.json"
if [ -f "$p" ] && python3 - "$p" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
assert d["plugin"] == "commit-craft" and d["version"], d
assert d["skills"] and d["skills"][0]["name"] == "commit", d["skills"]
assert d["skills"][0]["when_to_use"] and d["skills"][0]["body"], "skill core empty"
print("OK")
PY
then echo "ok: exports the portable skill core + version"
else echo "fail: export core — $out"; fi

# 2 — adapters for the non-Claude harnesses are named
python3 - "$p" <<'PY' && echo "ok: adapter targets named (codex, cursor, gemini-cli)" || echo "fail: adapters"
import json, sys
a = json.load(open(sys.argv[1]))["notes"]["adapters"]
assert {"codex", "cursor", "gemini-cli"} <= set(a), a
print("", end="")
PY

# 3 — the published plugin is UNTOUCHED (no Version-law churn)
before=$(cd "$REPO" && git status --porcelain plugins/commit-craft | wc -l)
(cd "$REPO" && python3 tools/export.py commit-craft --out "$WORK/dist2" >/dev/null)
after=$(cd "$REPO" && git status --porcelain plugins/commit-craft | wc -l)
[ "$before" = "$after" ] && echo "ok: export never touches the published plugin" \
                         || echo "fail: export mutated the plugin"

# 4 — deterministic output
a=$(python3 -c "import json;print(json.load(open('$WORK/dist/commit-craft/portable.json')))")
b=$(python3 -c "import json;print(json.load(open('$WORK/dist2/commit-craft/portable.json')))")
[ "$a" = "$b" ] && echo "ok: export deterministic" || echo "fail: export churns"

# 5 — a plugin with hooks carries the harness-specific caveat (don't auto-port)
python3 - "$p" <<'PY' && echo "ok: hooks flagged harness-specific (no blind auto-port)" || echo "fail: hook caveat"
import json, sys
n = json.load(open(sys.argv[1]))["notes"]["hooks"]
assert "harness-specific" in n, n
print("", end="")
PY

# 6 — dist/ is gitignored (derived artifact, not committed)
grep -q "^dist/" "$REPO/.gitignore" && echo "ok: dist/ gitignored" || echo "fail: dist/ not ignored"
