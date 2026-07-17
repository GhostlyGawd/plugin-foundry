#!/usr/bin/env bash
# loop.sh — attended-session launcher (ADR-032).
#
# The former headless Claude loop is retired. This script never accepts a prompt,
# iterates unattended, or runs in CI; it can only open the interactive Codex TUI in
# a real terminal. The operator then chooses and reviews one LOOP.md iteration.

set -uo pipefail
cd "$(dirname "$0")"

if [ -n "${CI:-}" ] || [ ! -t 0 ] || [ ! -t 1 ]; then
  echo "loop.sh: refused — model work requires a live, attended interactive terminal."
  echo "Open this repository in Codex interactively; headless and CI execution are disabled."
  exit 2
fi

if [ "$#" -gt 0 ]; then
  echo "loop.sh: iteration arguments are retired; interactive sessions run one reviewed task at a time."
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "loop.sh: 'codex' is not installed or not on PATH."
  echo "Install Codex, sign in with ChatGPT locally, then run 'codex' from this repository."
  exit 1
fi

cat <<'NOTICE'
Nightshift Foundry model automation is paused.

Opening an attended Codex session. Ask it to read LOOP.md and complete exactly one
iteration, review every proposed action, and submit the result through a pull request.
Do not use `codex exec`, a scheduler, CI, or another headless runner.
NOTICE

exec codex
