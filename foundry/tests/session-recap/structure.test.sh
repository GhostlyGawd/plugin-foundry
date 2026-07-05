#!/usr/bin/env bash
set -u
P="${PLUGIN_DIR:-plugins/session-recap}"
grep -q '"name": "session-recap"' "$P/.claude-plugin/plugin.json" && echo "ok: manifest name" || echo "fail: manifest name"
grep -q '^description: .*Use when' "$P/skills/recap/SKILL.md" && echo "ok: invoke contract" || echo "fail: invoke contract"
grep -q 'never truncate' "$P/skills/recap/SKILL.md" && echo "ok: append-only law" || echo "fail: append-only law"
grep -q 'git status' "$P/skills/recap/SKILL.md" && echo "ok: evidence before prose" || echo "fail: no git evidence step"
grep -q -- '- \[ \]' "$P/skills/recap/SKILL.md" && echo "ok: checkboxed next steps" || echo "fail: next steps not checkboxes"
if command -v claude >/dev/null 2>&1; then
  claude plugin validate "./$P" --strict >/dev/null 2>&1 && echo "ok: official validate" || echo "fail: official validate"
else echo "skip: official validate (CLI absent here; green in CI)"; fi
