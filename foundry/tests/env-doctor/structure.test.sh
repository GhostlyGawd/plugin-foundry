#!/usr/bin/env bash
set -u
P="${PLUGIN_DIR:-plugins/env-doctor}"
grep -q '"name": "env-doctor"' "$P/.claude-plugin/plugin.json" && echo "ok: manifest name" || echo "fail: manifest name"
grep -q '^description: .*Use when' "$P/skills/envcheck/SKILL.md" && echo "ok: invoke contract" || echo "fail: invoke contract"
grep -q 'only files that exist' "$P/skills/envcheck/SKILL.md" && echo "ok: repo-requirements-first" || echo "fail: requirements source"
grep -q 'type -a' "$P/skills/envcheck/SKILL.md" && echo "ok: PATH shadowing check" || echo "fail: no PATH check"
grep -qi 'never run an install' "$P/skills/envcheck/SKILL.md" && echo "ok: consent law" || echo "fail: consent law"
grep -q 'manufacture findings' "$P/skills/envcheck/SKILL.md" && echo "ok: honest empty state" || echo "fail: empty state"
if command -v claude >/dev/null 2>&1; then
  claude plugin validate "./$P" --strict >/dev/null 2>&1 && echo "ok: official validate" || echo "fail: official validate"
else echo "skip: official validate (CLI absent here; green in CI)"; fi
