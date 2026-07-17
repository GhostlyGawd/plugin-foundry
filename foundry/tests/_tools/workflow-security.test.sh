#!/usr/bin/env bash
# Hosted-agent secret boundary tests: the OpenAI key is scoped to the official
# Codex Action in a read-token job; write permissions exist only in keyless jobs.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
WF="$REPO/.github/workflows"
SHIFT="$WF/run-shift.yml"
DEMOS="$WF/record-demos.yml"

# 1 — no GitHub workflow consumes the retired Claude/Anthropic credentials.
old=$(grep -rlE 'CLAUDE_CODE_OAUTH_TOKEN|ANTHROPIC_API_KEY' "$WF" || true)
if [ -z "$old" ]; then
  echo "ok: workflows no longer consume Claude or Anthropic credentials"
else
  echo "fail: retired credential remains in: $old"
fi

# 2 — the API key is an action input, never a job/shell environment variable.
if grep -q 'openai-api-key:.*secrets.OPENAI_API_KEY' "$SHIFT" \
  && grep -q 'openai-api-key:.*secrets.OPENAI_API_KEY' "$DEMOS" \
  && ! grep -rEq '^[[:space:]]+OPENAI_API_KEY:' "$WF"; then
  echo "ok: OpenAI key is scoped to Codex Action inputs"
else
  echo "fail: OpenAI key is missing from action input or exposed through env"
fi

# 3 — Codex Action is commit-pinned and uses the hardened runner boundary.
PIN='openai/codex-action@52fe01ec70a42f454c9d2ebd47598f9fd6893d56'
if grep -q "$PIN" "$SHIFT" && grep -q "$PIN" "$DEMOS" \
  && [ "$(grep -h -c 'safety-strategy: drop-sudo' "$SHIFT" "$DEMOS" | awk '{s+=$1} END {print s}')" -eq 2 ] \
  && [ "$(grep -h -c 'sandbox: workspace-write' "$SHIFT" "$DEMOS" | awk '{s+=$1} END {print s}')" -eq 2 ]; then
  echo "ok: Codex Action is pinned, sandboxed, and drops sudo"
else
  echo "fail: Codex Action pin or hardening input drifted"
fi

# 4 — checkout credentials are absent from the preparation and model jobs.
if [ "$(grep -h -c 'persist-credentials: false' "$SHIFT" "$DEMOS" | awk '{s+=$1} END {print s}')" -eq 3 ]; then
  echo "ok: model jobs do not persist GitHub write credentials"
else
  echo "fail: model checkout credential boundary missing"
fi

# 5 — model diffs cross jobs as patches; only the landing side applies them.
if grep -q 'uses: actions/upload-artifact@' "$SHIFT" \
  && grep -q 'uses: actions/download-artifact@' "$SHIFT" \
  && grep -q 'git apply --index' "$SHIFT" \
  && grep -q 'uses: actions/upload-artifact@' "$DEMOS" \
  && grep -q 'uses: actions/download-artifact@' "$DEMOS" \
  && grep -q 'git apply --index' "$DEMOS"; then
  echo "ok: model output crosses into keyless landing jobs as patches"
else
  echo "fail: patch-artifact landing boundary missing"
fi

# 6 — top-level deny-all plus explicit read/write job permissions are present.
python3 - "$SHIFT" "$DEMOS" <<'PY' \
  && echo "ok: workflow permissions split read-token generation from keyless writes" \
  || echo "fail: workflow permission split drifted"
import re, sys
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    assert re.search(r"(?m)^permissions: \{\}$", text), path
    generate = text.split("\n  generate:\n", 1)[1].split("\n  propose:\n", 1)[0]
    propose = text.split("\n  propose:\n", 1)[1]
    assert re.search(r"(?m)^      contents: read$", generate), path
    assert not re.search(r"(?m)^      contents: write$", generate), path
    assert not re.search(r"(?m)^      issues: write$", generate), path
    assert re.search(r"(?m)^      contents: write$", propose), path
    assert "secrets.OPENAI_API_KEY" not in propose, path
PY

# 7 — every external action is pinned to an immutable full commit SHA.
python3 - "$WF" <<'PY' \
  && echo "ok: every GitHub Action is full-SHA pinned" \
  || echo "fail: mutable GitHub Action reference remains"
import pathlib, re, sys
bad = []
for path in pathlib.Path(sys.argv[1]).glob("*.yml"):
    for action, ref in re.findall(r"uses:\s*([^@\s]+)@([^\s#]+)", path.read_text()):
        if action.startswith("./"):
            continue
        if not re.fullmatch(r"[0-9a-f]{40}", ref):
            bad.append(f"{path.name}: {action}@{ref}")
assert not bad, bad
PY

# 8 — code scanning is a least-privilege, pinned, Python-only workflow.
CODEQL="$WF/codeql.yml"
if grep -q 'security-events: write' "$CODEQL" \
  && grep -q 'languages: python' "$CODEQL" \
  && [ "$(grep -c 'github/codeql-action/.*@7188fc363630916deb702c7fdcf4e481b751f97a' "$CODEQL")" -eq 2 ]; then
  echo "ok: CodeQL is pinned and least-privilege"
else
  echo "fail: CodeQL workflow or permissions drifted"
fi
