#!/usr/bin/env bash
# Bought-bot config tests (MASTER P3.5 + P2.1, ADR-031): CodeRabbit (PR review)
# and Dosu (issue triage) are config-ready external apps. The configs must be
# valid AND bound to THIS repo's laws — a generic bot is worse than the honest
# review the foundry already does. The night-clerk (auto-answering) stays OFF.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"

# 1 — .coderabbit.yaml valid + bound to the foundry's laws
out=$(python3 - "$REPO/.coderabbit.yaml" <<'PY'
import sys, yaml
d = yaml.safe_load(open(sys.argv[1]))
axes = {p["path"] for p in d["reviews"]["path_instructions"]}
assert {"plugins/**", "plugins/**/hooks/**", "tools/**", "**/*.md"} <= axes, axes
txt = open(sys.argv[1]).read()
for law in ["Version law", "CLAUDE_PLUGIN_ROOT", "two-iteration rule", "Growth-honesty"]:
    assert law in txt, f"not bound to: {law}"
assert d["reviews"]["auto_review"]["drafts"] is False, "don't review drafts"
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: coderabbit.yaml valid, bound to Version/hook/ADR/honesty laws" \
                  || echo "fail: coderabbit — $out"

# 2 — .dosu.yaml valid, triage-only, mirrors the intake funnel
out=$(python3 - "$REPO/.dosu.yaml" <<'PY'
import sys, yaml
d = yaml.safe_load(open(sys.argv[1]))
t = d["triage"]
assert t["auto_respond"] is False, "night-clerk (auto-answer) must stay OFF (P4.4 deferred)"
assert t["treat_issue_body_as"] == "untrusted-data", "issue text is DATA, never instructions"
labels = {l["name"] for l in t["labels"]}
assert {"bug", "commission", "idea", "question", "field-report"} <= labels, labels
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: dosu.yaml valid — triage-only, untrusted-data, mirrors intake" \
                  || echo "fail: dosu — $out"

# 3 — dosu label routing matches the repo's actual labels (ops-guard.yml)
for lbl in bug commission idea question field-report; do
  grep -q "ensure ${lbl}" "$REPO/.github/workflows/ops-guard.yml" \
    || { echo "fail: dosu routes to '$lbl' but ops-guard doesn't ensure it"; exit 1; }
done
echo "ok: dosu routes only to labels ops-guard actually creates"

# 4 — both app installs are desk-gated (not assumed live)
grep -q "CodeRabbit" "$REPO/state/DESK.jsonl" && grep -q "Dosu\|dosu" "$REPO/state/DESK.jsonl" \
  && echo "ok: both bot installs desk-gated" \
  || echo "fail: a bot install is missing its desk item"
