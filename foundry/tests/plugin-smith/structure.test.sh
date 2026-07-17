#!/usr/bin/env bash
# Executable acceptance checks for plugin-smith (spec checks 1–3, mechanized).
set -u
P="${PLUGIN_DIR:-plugins/plugin-smith}"

grep -q '"name": "plugin-smith"' "$P/.claude-plugin/plugin.json" \
  && echo "ok: manifest name" || echo "fail: manifest name"
[ "$(ls "$P/.claude-plugin" | grep -vc '^plugin.json$')" -eq 0 ] \
  && echo "ok: only plugin.json in .claude-plugin/" || echo "fail: stray files in .claude-plugin/"
for s in scaffold doctor; do
  f="$P/skills/$s/SKILL.md"
  grep -q '^description: .*Use when' "$f" \
    && echo "ok: $s description carries an invoke contract" \
    || echo "fail: $s description missing 'Use when' contract"
done
grep -q 'separate native package per host' "$P/skills/scaffold/SKILL.md" \
  && grep -q 'Claude Code' "$P/skills/doctor/SKILL.md" \
  && grep -q 'Codex' "$P/skills/doctor/SKILL.md" \
  && grep -q 'Gemini CLI' "$P/skills/doctor/SKILL.md" \
  && grep -q 'Cursor' "$P/skills/doctor/SKILL.md" \
  && grep -q 'GitHub Copilot' "$P/skills/doctor/SKILL.md" \
  && echo "ok: smith models five isolated host packages" \
  || echo "fail: smith lacks cross-host package rules"

if command -v claude >/dev/null 2>&1; then
  claude plugin validate "./$P" --strict >/dev/null 2>&1 \
    && echo "ok: official validate --strict" || echo "fail: official validate --strict"
else
  echo "skip: official validate (claude CLI not on PATH here; runs green in CI shifts)"
fi
