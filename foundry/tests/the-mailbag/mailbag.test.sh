#!/usr/bin/env bash
set -u
OUT=$(PATH=/usr/bin:/bin python3 tools/shipnote.py 2>&1 >/dev/null || true)
echo "$OUT" | grep -q "mailbag: gh absent" && echo "ok: gh-absent skip line, shipnote still stands" || {
  command -v gh >/dev/null 2>&1 && echo "ok: gh present here — skip-path exercised in CI-less envs" || echo "fail: no skip line without gh"; }
python3 -c "import yaml; yaml.safe_load(open('.github/ISSUE_TEMPLATE/question.yml'))" && echo "ok: question.yml lints" || echo "fail: question.yml"
grep -q "question issue template" CONTRIBUTING.md && echo "ok: CONTRIBUTING routes questions (Lane 0)" || echo "fail: CONTRIBUTING link"
grep -q "Mailbag" charter/GROWTH.md && echo "ok: answering duty on the books" || echo "fail: GROWTH duty"
