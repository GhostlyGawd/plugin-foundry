#!/usr/bin/env bash
# Executable acceptance checks 3–4 for commit-craft's message-guard hook:
# blocks bad messages (exit 2 + reason), passes good ones, FAILS OPEN on anything odd.
set -u
S="${PLUGIN_DIR:-plugins/commit-craft}/scripts/check-commit-msg.sh"
if [ ! -f "$S" ]; then
  echo "skip: hook script not built yet (record stage < building) — suite arms itself when it lands"
  exit 0
fi
payload() { printf '{"tool_name":"Bash","tool_input":{"command":%s}}' "$1"; }

payload '"git commit -m \"bad message\""' | bash "$S" >/dev/null 2>&1
[ $? -eq 2 ] && echo "ok: malformed message blocked (exit 2)" || echo "fail: malformed message not blocked"
payload '"git commit -m \"feat(core): add thing\""' | bash "$S" >/dev/null 2>&1
[ $? -eq 0 ] && echo "ok: conforming message passes" || echo "fail: conforming message blocked"
payload '"ls -la"' | bash "$S" >/dev/null 2>&1
[ $? -eq 0 ] && echo "ok: non-commit command ignored (fail-open)" || echo "fail: non-commit command blocked"
printf 'not json at all' | bash "$S" >/dev/null 2>&1
[ $? -eq 0 ] && echo "ok: garbled payload fails open" || echo "fail: garbled payload did not fail open"

# i155 (v10 #2): COMMIT_CRAFT_TYPES knob
payload '"git commit -m \"build: wire ci\""' | COMMIT_CRAFT_TYPES="feat fix build" bash "$S" >/dev/null 2>&1
[ $? -eq 0 ] && echo "ok: knob override admits configured type" || echo "fail: knob override rejected configured type"
payload '"git commit -m \"build: wire ci\""' | bash "$S" >/dev/null 2>&1
[ $? -eq 2 ] && echo "ok: knob default still blocks unconfigured type" || echo "fail: default admitted unconfigured type"
payload '"git commit -m \"zzz: nope\""' | COMMIT_CRAFT_TYPES='.*' bash "$S" >/dev/null 2>&1
[ $? -eq 2 ] && echo "ok: knob regex injection dropped (default enforced)" || echo "fail: regex injection changed guard behavior"
