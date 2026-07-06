#!/usr/bin/env bash
# qa.sh — the executable QA harness (Tier 1). Runs every executable *.test.sh under
# foundry/tests/<plugin>/ with PLUGIN_DIR set. Tests emit lines starting
# "ok:", "skip:", or "fail:"; any fail (or nonzero exit) fails the harness.
# Usage: bash tools/qa.sh [plugin-name]
set -uo pipefail
cd "$(dirname "$0")/.."
FAIL=0; OK=0; SKIP=0

run_suite() {
  local name="$1" dir="foundry/tests/$1"
  [ -d "$dir" ] || { echo "qa: $name — no test suite (fine before rc; required at rc+)"; return; }
  local found=0
  for t in "$dir"/*.test.sh; do
    [ -f "$t" ] || continue
    # a test that lost its exec bit is a silently-disabled test — that's a FAIL,
    # not a skip (audit-004 P3; the validator only catches the zero-executables
    # case at rc+, this catches the one-lost-chmod case everywhere)
    if [ ! -x "$t" ]; then
      echo "  [$name] fail: $t exists but is not executable (chmod +x)"
      FAIL=$((FAIL + 1)); found=1; continue
    fi
    found=1
    local out rc
    out=$(PLUGIN_DIR="plugins/$name" REPO_ROOT="$PWD" bash "$t" 2>&1); rc=$?
    echo "$out" | sed "s/^/  [$name] /"
    OK=$((OK + $(echo "$out" | grep -c '^ok:' || true)))
    SKIP=$((SKIP + $(echo "$out" | grep -c '^skip:' || true)))
    local f; f=$(echo "$out" | grep -c '^fail:' || true)
    [ "$rc" -ne 0 ] && [ "$f" -eq 0 ] && f=1
    FAIL=$((FAIL + f))
  done
  [ "$found" -eq 0 ] && echo "qa: $name — suite dir exists but holds no *.test.sh"
}

if [ "${1:-}" ]; then run_suite "$1"; else
  for d in foundry/tests/*/; do [ -d "$d" ] && run_suite "$(basename "$d")"; done
fi
echo "qa: $OK ok · $SKIP skip · $FAIL fail"
[ "$FAIL" -eq 0 ]
