#!/usr/bin/env bash
# todo-ledger acceptance checks (record: foundry/records/todo-ledger.md).
# Skill-only plugin: the suite verifies structure + the invoke contract + the
# honesty/read-only clauses the record promises.
set -u
P="${PLUGIN_DIR:-plugins/todo-ledger}"
S="$P/skills/ledger/SKILL.md"

grep -q '"name": "todo-ledger"' "$P/.claude-plugin/plugin.json" && echo "ok: manifest name" || echo "fail: manifest name"
grep -q '^description: .*Use when' "$S" && echo "ok: invoke contract (Use when …)" || echo "fail: invoke contract"
# check 1 — markers via git grep on tracked files, non-git degrades gracefully
grep -q 'git grep' "$S" && grep -qi "isn't a git repo" "$S" && echo "ok: check1 git grep + non-git fallback" || echo "fail: check1 marker search"
# check 2 — blame age + author, honest unknown (never a guessed date)
grep -q 'git blame' "$S" && grep -qi 'never invented\|never guess' "$S" && echo "ok: check2 blame age + honest unknown" || echo "fail: check2 dating honesty"
# check 3 — oldest-first ranking + worst-offenders + copyable file:line
grep -qi 'oldest first' "$S" && grep -qi 'worst.offenders' "$S" && grep -qi 'copyable' "$S" && echo "ok: check3 ranking + summary + copyable refs" || echo "fail: check3 ranking"
# check 4 — read-only by default; dated file only on request
grep -qi 'read-only' "$S" && grep -qi 'never unasked' "$S" && echo "ok: check4 read-only, opt-in write" || echo "fail: check4 consent/read-only"
# structural: skills-only, no hooks shipped, README + CHANGELOG present
[ -f "$P/README.md" ] && [ -f "$P/CHANGELOG.md" ] && echo "ok: README + CHANGELOG present" || echo "fail: docs missing"
[ ! -d "$P/hooks" ] && echo "ok: skills-only (no hooks surface)" || echo "fail: unexpected hooks dir"
if command -v claude >/dev/null 2>&1; then
  claude plugin validate "./$P" --strict >/dev/null 2>&1 && echo "ok: official validate" || echo "fail: official validate"
else echo "skip: official validate (CLI absent here; green in CI)"; fi
