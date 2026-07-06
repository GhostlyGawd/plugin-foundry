#!/usr/bin/env bash
# Gate tests (v10 #6, ADR-018): validate.py is the law everything else trusts —
# this suite proves each law actually fires, against disposable fixtures.
# Pattern: build a minimal VALID foundry, assert green; then break exactly one
# law per case and assert the specific error message appears.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

fresh() { rm -rf "$WORK/fx"; python3 "$HERE/fixture.py" "$WORK/fx"; }
V() { (cd "$WORK/fx" && python3 tools/validate.py 2>&1); }

# case 0 — the baseline fixture is green (everything below depends on this)
fresh
out=$(V); rc=$?
if [ "$rc" -eq 0 ]; then echo "ok: baseline fixture validates green"
else echo "fail: baseline fixture is red — every case below is meaningless"; echo "$out" | sed 's/^/    /'; exit 1; fi

expect_error() { # expect_error <case-label> <grep-pattern>
  local label="$1" pat="$2" out rc
  out=$(V); rc=$?
  if [ "$rc" -ne 0 ] && echo "$out" | grep -q "$pat"; then
    echo "ok: $label"
  else
    echo "fail: $label — rc=$rc, wanted /$pat/ in: $(echo "$out" | tail -3 | tr '\n' ' ')"
  fi
}

# 1 — missing cumulative section
fresh; sed -i 's/### Acceptance checks/### Something else/' "$WORK/fx/foundry/records/demo-plug.md"
expect_error "missing stage section is caught" "requires section '### Acceptance checks'"

# 2 — bad semver in manifest
fresh; sed -i 's/"version": "0.1.0"/"version": "0.1"/' "$WORK/fx/plugins/demo-plug/.claude-plugin/plugin.json"
expect_error "non-semver manifest version is caught" "is not semver"

# 3 — record/manifest version drift
fresh; sed -i 's/^version: 0.1.0$/version: 0.2.0/' "$WORK/fx/foundry/records/demo-plug.md"
expect_error "record vs plugin.json version drift is caught" "record version"

# 4 — published but missing from the marketplace
fresh; python3 - "$WORK/fx" << 'PY'
import json, sys, pathlib
p = pathlib.Path(sys.argv[1]) / ".claude-plugin" / "marketplace.json"
mp = json.loads(p.read_text()); mp["plugins"] = []; p.write_text(json.dumps(mp))
PY
expect_error "published-but-unlisted is caught" "missing from marketplace.json"

# 5 — unknown hook event + banned .* matcher + unquoted plugin root
fresh; mkdir -p "$WORK/fx/plugins/demo-plug/hooks"
cat > "$WORK/fx/plugins/demo-plug/hooks/hooks.json" << 'JSON'
{"hooks": {"PreToolUsee": [{"matcher": ".*",
  "hooks": [{"type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/x.sh"}]}]}}
JSON
expect_error "unknown hook event is caught" "unknown hook event"
expect_error "banned .* matcher is caught" "matcher '.\*' is banned"
expect_error "unquoted CLAUDE_PLUGIN_ROOT is caught" "unquoted"

# 6 — unterminated front matter
fresh; printf -- '---\nname: demo-plug\nno terminator' > "$WORK/fx/foundry/records/demo-plug.md"
expect_error "unterminated front matter is caught" "unterminated front matter"

# 7 — published without an executable suite (exec bit lost)
fresh; chmod -x "$WORK/fx/foundry/tests/demo-plug/smoke.test.sh"
expect_error "published without executable suite is caught" "requires at least one executable"

# 8 — published without review approval
fresh; sed -i 's/REVIEW: approved/REVIEW: pending/' "$WORK/fx/foundry/records/demo-plug.md"
expect_error "published without REVIEW: approved is caught" "requires 'REVIEW: approved'"

# 9 — orphan artifact (plugin dir with no record)
fresh; mkdir -p "$WORK/fx/plugins/ghost-plug"
expect_error "orphan artifact is caught" "no foundry record"

# 10 — non-executable script inside the shipped plugin
fresh; mkdir -p "$WORK/fx/plugins/demo-plug/scripts"
printf '#!/usr/bin/env bash\ntrue\n' > "$WORK/fx/plugins/demo-plug/scripts/run.sh"
chmod -x "$WORK/fx/plugins/demo-plug/scripts/run.sh"
expect_error "non-executable shipped script is caught" "not executable"

# 11 — build.py runs green on the valid fixture (needs the site scaffolding)
fresh
mkdir -p "$WORK/fx/site"
printf '{}\n' > "$WORK/fx/foundry/site-config.json"
printf '# JOURNAL\n\n## i1 — fixture — 2026-07-06T00:00:00Z\n- did: fixture\n' > "$WORK/fx/state/JOURNAL.md"
printf '# DECISIONS\n' > "$WORK/fx/state/DECISIONS.md"
printf '# BACKLOG\n' > "$WORK/fx/state/BACKLOG.md"
out=$( (cd "$WORK/fx" && python3 tools/build.py 2>&1) ); rc=$?
if [ "$rc" -eq 0 ] && [ -f "$WORK/fx/site/index.html" ] && [ -f "$WORK/fx/site/data.json" ]; then
  echo "ok: build.py green on minimal fixture (index + data emitted)"
else
  echo "fail: build.py on fixture — rc=$rc: $(echo "$out" | tail -2 | tr '\n' ' ')"
fi
