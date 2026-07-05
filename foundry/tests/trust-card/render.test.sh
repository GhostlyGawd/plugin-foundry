#!/usr/bin/env bash
set -u
grep -q 'PreToolUse · matcher: Bash' site/p/commit-craft.html && echo "ok: hook surface parsed from hooks.json" || echo "fail: hook surface"
grep -q '<b>hooks</b><span>none</span>' site/p/session-recap.html && echo "ok: skills-only shows hooks none" || echo "fail: hooks none"
grep -q 'none detected in executable surfaces (heuristic)' site/p/session-recap.html && echo "ok: network heuristic labeled" || echo "fail: network label"
grep -q 'class="trust"' site/p/community-voting.html && echo "fail: trust card leaked onto a feature" || echo "ok: features carry no trust card"
grep -q 'no hand-written safety claims' site/p/env-doctor.html && echo "ok: derivation-only note present" || echo "fail: derivation note"
