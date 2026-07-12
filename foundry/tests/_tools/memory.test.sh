#!/usr/bin/env bash
# Factory-brain tests (MASTER P5.1, ADR-031): the differentiated discipline is
# DEDUP-ON-WRITE (never append-everything — the staleness/poisoning failure
# mode). Prove: a near-duplicate is refused, distinct lessons are kept, recall
# is relevant and deterministic, the backend seam falls back to the local floor.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

FX="$WORK/fx"
mkdir -p "$FX/tools" "$FX/foundry"
cp "$REPO/tools/memory.py" "$FX/tools/"
M() { (cd "$FX" && python3 tools/memory.py "$@" 2>&1); }

# 1 — distinct lessons are added
M add "Fence untrusted text before any prompt." --tags security >/dev/null
M add "The quota governor sheds low then high, never product." --tags quota >/dev/null
n=$(M list | grep -c '^m-')
[ "$n" -eq 2 ] && echo "ok: distinct lessons stored" || echo "fail: expected 2, got $n"

# 2 — dedup-on-write: a near-identical re-add is REFUSED (store stays 2)
out=$(M add "Fence untrusted text before any prompt" --tags security)
n=$(M list | grep -c '^m-')
if echo "$out" | grep -q "refused-duplicate" && [ "$n" -eq 2 ]; then
  echo "ok: dedup-on-write refuses a near-duplicate (no append-everything)"
else echo "fail: dedup — $out (store=$n)"; fi

# 3 — --force overrides dedup when an operator really means it
M add "Fence untrusted text before any prompt." --tags security --force >/dev/null
n=$(M list | grep -c '^m-')
[ "$n" -eq 3 ] && echo "ok: --force overrides dedup deliberately" || echo "fail: force — store=$n"

# 4 — recall returns the relevant lesson, scored
out=$(M recall "how do we handle quota pressure")
if echo "$out" | grep -q "sheds low then high"; then
  echo "ok: recall surfaces the relevant lesson"
else echo "fail: recall — $out"; fi

# 5 — recall is deterministic (same query → same order twice)
a=$(M recall "fence untrusted prompt security" --k 3)
b=$(M recall "fence untrusted prompt security" --k 3)
[ "$a" = "$b" ] && echo "ok: recall is deterministic" || echo "fail: recall nondeterministic"

# 6 — an irrelevant query returns nothing (no forced noise)
out=$(M recall "bicycle maintenance schedules")
echo "$out" | grep -q "no relevant lesson" \
  && echo "ok: irrelevant query returns nothing (no hallucinated hit)" \
  || echo "fail: irrelevant recall — $out"

# 7 — backend seam: an unknown backend falls back to the local floor
out=$(cd "$FX" && MEMORY_BACKEND=mem0 python3 tools/memory.py add "new lesson via seam" 2>&1)
echo "$out" | grep -q "local store used" \
  && echo "ok: unknown backend falls back to the local floor" \
  || echo "fail: backend seam — $out"

# 8 — the real repo shipped a seeded, deduped store
n=$(grep -c '"id"' "$REPO/foundry/memory.jsonl")
[ "$n" -ge 5 ] && echo "ok: repo ships $n seeded lessons" || echo "fail: seed store thin ($n)"
