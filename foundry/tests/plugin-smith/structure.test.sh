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
grep -q 'code.claude.com/docs' "$P/skills/scaffold/SKILL.md" \
  && echo "ok: scaffold defers to official docs" || echo "fail: scaffold lacks docs-before-invention pointer"

if command -v claude >/dev/null 2>&1; then
  claude plugin validate "./$P" --strict >/dev/null 2>&1 \
    && echo "ok: official validate --strict" || echo "fail: official validate --strict"
else
  echo "skip: official validate (claude CLI not on PATH here; runs green in CI shifts)"
fi
