#!/usr/bin/env bash
# Publish-kit tests (MASTER GAP-B, ADR-031): submissions prepared to the
# repo's edge, desk-gated, and constitutionally clean — the tool must be
# incapable of talking to the network.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"

# 1 — static law: no network machinery in the tool at all
if grep -nE "requests|urlopen|http\.client|socket|curl|subprocess" "$REPO/tools/publish.py"; then
  echo "fail: publish.py contains network/exec machinery (Art. I §1 risk)"
else
  echo "ok: publish.py is provably offline (no network/exec imports)"
fi

# 2 — the kit lists every marketplace plugin
n=$(python3 -c "import json; print(len(json.load(open('$REPO/.claude-plugin/marketplace.json'))['plugins']))")
listed=$(grep -c '^\- \*\*' "$REPO/foundry/SUBMISSIONS.md")
[ "$listed" -eq "$n" ] && echo "ok: all $n shelf plugins have blurbs" \
                       || echo "fail: $listed blurbs for $n plugins"

# 3 — the prefilled link targets THEIR intake, encoded
if grep -q "awesome-claude-code/issues/new?title=" "$REPO/foundry/SUBMISSIONS.md" \
   && grep -q "Prefilled submission issue" "$REPO/foundry/SUBMISSIONS.md"; then
  echo "ok: prefilled intake link present"
else echo "fail: prefilled link missing"; fi

# 4 — regeneration is deterministic and desk item dedups
before=$(sha256sum "$REPO/foundry/SUBMISSIONS.md" | cut -d' ' -f1)
out=$(cd "$REPO" && python3 tools/publish.py)
after=$(sha256sum "$REPO/foundry/SUBMISSIONS.md" | cut -d' ' -f1)
if [ "$before" = "$after" ] && echo "$out" | grep -q "already open"; then
  echo "ok: deterministic regen; desk item dedups"
else echo "fail: regen churns or desk duplicated — $out"; fi

# 5 — the constitution clause is quoted in the kit itself
grep -q "never opens PRs/issues on third-party" "$REPO/foundry/SUBMISSIONS.md" \
  && echo "ok: the we-don't-spam clause rides in the kit" \
  || echo "fail: constitution clause missing from the kit"
