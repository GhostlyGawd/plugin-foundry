#!/usr/bin/env bash
# smoke.sh — wraps `claude plugin validate --strict` for one plugin or all of them.
# Usage: bash tools/smoke.sh [plugin-name]
set -uo pipefail
cd "$(dirname "$0")/.."

FAIL=0
run_one() {
  local d="plugins/$1"
  [ -d "$d" ] || { echo "smoke: $d missing"; FAIL=1; return; }
  if command -v claude >/dev/null 2>&1; then
    if claude plugin validate "./$d" --strict; then
      echo "smoke: $1 — official validate --strict: PASS"
    else
      echo "smoke: $1 — official validate --strict: FAIL"; FAIL=1
    fi
  else
    echo "smoke: $1 — SKIPPED (claude CLI not on PATH; structural fallback = tools/validate.py). Log this in the Test log."
  fi
}

if [ "${1:-}" ]; then run_one "$1"; else
  for d in plugins/*/; do [ -d "$d" ] && run_one "$(basename "$d")"; done
fi
exit $FAIL
