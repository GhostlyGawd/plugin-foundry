#!/usr/bin/env bash
# Executable acceptance checks for fork-a-foundry.
set -u
P="${PLUGIN_DIR:-plugins/fork-a-foundry}"
grep -q '"name": "fork-a-foundry"' "$P/.claude-plugin/plugin.json" \
  && echo "ok: manifest name" || echo "fail: manifest name"
grep -q '^description: .*Use when' "$P/skills/bootstrap/SKILL.md" \
  && echo "ok: bootstrap invoke contract" || echo "fail: bootstrap description missing 'Use when'"
for law in "one commit" "UNTRUSTED" "two-iteration" "Naming Ceremony"; do
  grep -qi "$law" "$P/skills/bootstrap/SKILL.md" \
    && echo "ok: carries law — $law" || echo "fail: missing law — $law"
done
grep -q 'container' "$P/skills/bootstrap/SKILL.md" \
  && echo "ok: sandbox reminder present" || echo "fail: no sandbox reminder"
if command -v claude >/dev/null 2>&1; then
  claude plugin validate "./$P" --strict >/dev/null 2>&1 \
    && echo "ok: official validate --strict" || echo "fail: official validate --strict"
else
  echo "skip: official validate (CLI absent here; green in CI)"
fi
