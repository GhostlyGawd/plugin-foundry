#!/usr/bin/env bash
# Perception-agent tests (MASTER P1.2/P1.3/P1.5, ADR-031): ask-the-factory
# answers only from sourced history, the diagnostician classifies real failure
# shapes, and the untrusted-ingesting agents (scout, ask) are fenced by the
# contract. Read-only, all of them.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

# 1 — ask returns SOURCED passages (never an ungrounded claim)
out=$(cd "$REPO" && python3 tools/ask.py "constitution guard block" --k 2)
if echo "$out" | grep -qE "\[(JOURNAL|DECISIONS|record)\]" && echo "$out" | grep -qi "relevance"; then
  echo "ok: ask returns sourced passages with provenance"
else echo "fail: ask — $out"; fi

# 2 — ask is honest about an unanswerable query (single guaranteed-absent token)
out=$(cd "$REPO" && python3 tools/ask.py "qzxwvymkjpflooble")
echo "$out" | grep -q "no sourced answer" \
  && echo "ok: ask admits when history has no answer (no fabrication)" \
  || echo "fail: ask should have found nothing — $out"

# 3 — diagnostician classifies the auth-failure shape
printf 'claude: OAuth token has expired\n' > "$WORK/auth.log"
out=$(cd "$REPO" && python3 tools/diagnose.py "$WORK/auth.log"); rc=$?
if [ "$rc" -eq 2 ] && echo "$out" | grep -qi "authentication failure" && echo "$out" | grep -q "NEXT STEP"; then
  echo "ok: diagnostician classifies auth failure + names a next step"
else echo "fail: diagnose auth — rc=$rc $out"; fi

# 4 — diagnostician classifies distinct shapes (quota, gate-red) not just auth
printf 'quota: HALT foundry-loop — pressure 1.10\n' > "$WORK/q.log"
out=$(cd "$REPO" && python3 tools/diagnose.py "$WORK/q.log")
echo "$out" | grep -qi "quota" && echo "ok: diagnostician distinguishes quota halt" \
                               || echo "fail: quota class — $out"

# 5 — an unknown failure is NOT force-fit into a wrong diagnosis
printf 'some totally novel error nobody has seen before xyzzy\n' > "$WORK/u.log"
out=$(cd "$REPO" && python3 tools/diagnose.py "$WORK/u.log"); rc=$?
if [ "$rc" -eq 0 ] && echo "$out" | grep -qi "no known failure signature"; then
  echo "ok: unknown failure → honest 'inspect the raw log', not a wrong guess"
else echo "fail: unknown class — rc=$rc $out"; fi

# 6 — the untrusted-ingesting agents are fenced + read_only (contract enforced)
out=$(cd "$REPO" && python3 - <<'PY'
import sys; sys.path.insert(0, "tools")
from lib import load_agents
errs = []; a = {x["id"]: x for x in load_agents(errs)}
assert not errs, errs
for aid in ("scout", "ask"):
    assert a[aid]["trust_tier"] == "ingests_untrusted", aid
    assert a[aid].get("fenced") is True, f"{aid} not fenced"
    assert a[aid]["capability"] == "read_only", f"{aid} holds a pen"
assert a["diagnostician"]["capability"] == "read_only"
print("OK")
PY
)
[ "$out" = "OK" ] && echo "ok: scout+ask fenced & read_only (read/act split holds)" \
                  || echo "fail: contract — $out"

# 7 — the scout/ask prompts reference the fence (unfenced-ingestion lint would fail otherwise)
if grep -qi "fence\|UNTRUSTED" "$REPO/foundry/agents/scout/prompt.md" \
   && grep -qi "fence\|UNTRUSTED" "$REPO/foundry/agents/ask/prompt.md"; then
  echo "ok: untrusted-ingest prompts route through the fence"
else echo "fail: a prompt skips the fence"; fi
