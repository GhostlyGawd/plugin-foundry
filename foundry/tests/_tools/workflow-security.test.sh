#!/usr/bin/env bash
# Hosted-model pause boundary: Actions cannot hold a model credential or invoke a
# model, while deterministic security and PR-only automation remain enforced.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
WF="$REPO/.github/workflows"
SHIFT="$WF/run-shift.yml"
DEMOS="$WF/record-demos.yml"
ORCHESTRATE="$WF/orchestrate.yml"
QA="$WF/qa.yml"

model_secrets=$(grep -rlE 'OPENAI_API_KEY|ANTHROPIC_API_KEY|CLAUDE_CODE_OAUTH_TOKEN|auth\.json' "$WF" || true)
[ -z "$model_secrets" ] && echo "ok: workflows contain no model credential path" \
  || echo "fail: model credential reference remains in: $model_secrets"

model_calls=$(grep -rlE 'openai/codex-action|codex[[:space:]]+exec|claude[[:space:]]+-p' "$WF" || true)
[ -z "$model_calls" ] && echo "ok: workflows contain no hosted or headless model call" \
  || echo "fail: hosted/headless model call remains in: $model_calls"

for path in "$SHIFT" "$DEMOS"; do
  if grep -q 'workflow_dispatch:' "$path" \
    && grep -q 'if: \${{ false }}' "$path" \
    && ! grep -q 'schedule:' "$path" \
    && ! grep -q 'uses:' "$path"; then
    echo "ok: $(basename "$path") is an inert pause notice"
  else
    echo "fail: $(basename "$path") can execute model automation"
  fi
done

set +e
launcher_out=$(cd "$REPO" && CI=1 bash loop.sh 2>&1)
launcher_rc=$?
set -e
if [ "$launcher_rc" -ne 0 ] && echo "$launcher_out" | grep -qi 'attended interactive'; then
  echo "ok: loop.sh rejects CI and headless execution"
else
  echo "fail: loop.sh did not fail closed in CI"
fi

python3 - "$WF" <<'PY' \
  && echo "ok: every GitHub Action is full-SHA pinned" \
  || echo "fail: mutable GitHub Action reference remains"
import pathlib, re, sys
bad = []
for path in pathlib.Path(sys.argv[1]).glob("*.yml"):
    for action, ref in re.findall(r"uses:\s*([^@\s]+)@([^\s#]+)", path.read_text()):
        if not action.startswith("./") and not re.fullmatch(r"[0-9a-f]{40}", ref):
            bad.append(f"{path.name}: {action}@{ref}")
assert not bad, bad
PY

CODEQL="$WF/codeql.yml"
if grep -q 'security-events: write' "$CODEQL" \
  && grep -q 'languages: python' "$CODEQL" \
  && [ "$(grep -c 'github/codeql-action/.*@7188fc363630916deb702c7fdcf4e481b751f97a' "$CODEQL")" -eq 2 ]; then
  echo "ok: CodeQL is pinned and least-privilege"
else
  echo "fail: CodeQL workflow or permissions drifted"
fi

if grep -q 'python3 tools/orchestrator.py run --mode pr' "$ORCHESTRATE" \
  && grep -q 'gh pr create --base main' "$ORCHESTRATE" \
  && grep -q 'gh pr create --base main' "$QA" \
  && ! grep -Eq '^[[:space:]]+git push[[:space:]]*$' "$ORCHESTRATE" "$QA"; then
  echo "ok: deterministic automated mutations remain PR-only"
else
  echo "fail: an automated main-branch landing path remains"
fi
