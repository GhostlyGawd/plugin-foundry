#!/usr/bin/env bash
# dep-bump-brief acceptance checks 1–4 (record: foundry/records/dep-bump-brief.md)
set -u
P="${PLUGIN_DIR:-plugins/dep-bump-brief}"
S="$P/skills/dep-brief/SKILL.md"

# 1 — frontmatter + verbatim invoke contract
grep -q '^name: dep-brief$' "$S" && echo "ok: check1a skill name" || echo "fail: check1a skill name"
grep -q '^description: Summarize dependency bumps in the current branch or diff into an honest review brief\. Use when' "$S" \
  && echo "ok: check1b verbatim description + invoke contract" || echo "fail: check1b description drift from spec"

# 2 — honesty rules verbatim
grep -q '"changelog not checked"' "$S" && echo "ok: check2a changelog-not-checked path" || echo "fail: check2a"
grep -q 'NEVER invent' "$S" && echo "ok: check2b never-invent clause" || echo "fail: check2b"
grep -q 'never summarized from memory' "$S" && echo "ok: check2c unread-source rule" || echo "fail: check2c"

# 3 — four ecosystems named
ok=1
for eco in package.json requirements Cargo.toml go.mod; do
  grep -q "$eco" "$S" || { ok=0; echo "fail: check3 — ecosystem marker missing: $eco"; }
done
[ "$ok" -eq 1 ] && echo "ok: check3 js/python/rust/go all covered"

# 4 — structural: manifest name, semver, README Manage section, official validate
grep -q '"name": "dep-bump-brief"' "$P/.claude-plugin/plugin.json" && echo "ok: check4a manifest name" || echo "fail: check4a"
grep -q '## Manage' "$P/README.md" && echo "ok: check4b README Manage section (v11 convention)" || echo "fail: check4b"
python3 tools/doctor.py "$P" > /dev/null 2>&1 && echo "ok: check4c foundry doctor green" || echo "fail: check4c doctor red"
if command -v claude >/dev/null 2>&1; then
  claude plugin validate "./$P" --strict >/dev/null 2>&1 && echo "ok: check4d official validate" || echo "fail: check4d official validate"
else echo "skip: check4d official validate (CLI absent here; green in CI)"; fi
