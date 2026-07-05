#!/usr/bin/env bash
# commit-craft guard: blocks malformed `git commit -m` messages (exit 2 + stderr
# reason); everything else passes. FAILS OPEN by design — any parse trouble,
# non-commit command, or interactive commit exits 0 (charter: hooks are guests).
set -u
PAYLOAD="$(cat 2>/dev/null || true)"
export PAYLOAD
python3 - << 'PY'
import json, os, re, sys
try:
    payload = json.loads(os.environ.get("PAYLOAD", ""))
    cmd = payload.get("tool_input", {}).get("command", "")
except Exception:
    sys.exit(0)  # garbled input -> fail open
if not isinstance(cmd, str) or not re.search(r"\bgit\s+commit\b", cmd):
    sys.exit(0)  # not a commit -> none of our business
m = re.search(r"-m\s+\"((?:[^\"\\]|\\.)*)\"", cmd) or re.search(r"-m\s+'([^']*)'", cmd)
if not m:
    sys.exit(0)  # interactive/editor commit -> can't check, fail open
msg = m.group(1).replace('\\"', '"')
if re.match(r"^(feat|fix|docs|refactor|test|chore|perf)(\(.+\))?: .{1,72}$", msg.splitlines()[0]):
    sys.exit(0)
print("commit-craft: message %r isn't conventional — want `type(scope): subject` "
      "with type in feat|fix|docs|refactor|test|chore|perf and subject <=72 chars. "
      "The commit skill writes these for you." % msg.splitlines()[0][:80], file=sys.stderr)
sys.exit(2)
PY
exit $?
