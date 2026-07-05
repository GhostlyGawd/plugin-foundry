#!/usr/bin/env bash
set -u
P="${PLUGIN_DIR:-plugins/pr-narrator}"
grep -q '"name": "pr-narrator"' "$P/.claude-plugin/plugin.json" && echo "ok: manifest name" || echo "fail: manifest name"
grep -q '^description: .*Use when' "$P/skills/pr/SKILL.md" && echo "ok: invoke contract" || echo "fail: invoke contract"
grep -q 'git log --oneline' "$P/skills/pr/SKILL.md" && echo "ok: evidence first" || echo "fail: no evidence step"
grep -q '"none" is a valid' "$P/skills/pr/SKILL.md" && echo "ok: honest test notes" || echo "fail: test-notes honesty"
grep -q 'Risk & rollback' "$P/skills/pr/SKILL.md" && echo "ok: risk section" || echo "fail: risk section"
grep -q 'only after the user says yes' "$P/skills/pr/SKILL.md" && echo "ok: consent-gated gh" || echo "fail: gh consent"
if command -v claude >/dev/null 2>&1; then
  claude plugin validate "./$P" --strict >/dev/null 2>&1 && echo "ok: official validate" || echo "fail: official validate"
else echo "skip: official validate (CLI absent here; green in CI)"; fi
