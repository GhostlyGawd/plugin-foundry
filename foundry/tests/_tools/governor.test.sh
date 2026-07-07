#!/usr/bin/env bash
# Governor tool tests (v12 2.3, ADR-021): budget.py halts overspending shifts
# and metrics.py arms every experiment baseline — a silent parse regression in
# either disables a safety rail. Fixture repos + stub gh, same seams as the
# gate and intake suites.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

FX="$WORK/fx"; mkdir -p "$FX/tools" "$FX/state" "$FX/foundry" "$FX/.claude-plugin" "$FX/bin"
cp "$REPO"/tools/*.py "$FX/tools/"
printf '{}\n' > "$FX/foundry/site-config.json"
printf '{"name":"fixture","owner":{"name":"t"},"plugins":[{"name":"a"},{"name":"b"}]}\n' > "$FX/.claude-plugin/marketplace.json"
git -C "$FX" init -q .

# ---------- budget.py ----------
# b1 — no cap set: governor idle, exit 0
out=$( (cd "$FX" && python3 tools/budget.py check) ); rc=$?
[ "$rc" -eq 0 ] && echo "$out" | grep -q "governor idle" && echo "ok: b1 no cap -> idle" || echo "fail: b1 rc=$rc out=$out"

# b2 — add from a real claude result json
printf '{"total_cost_usd": 1.25, "usage": {"output_tokens": 42}}\n' > "$WORK/run.json"
(cd "$FX" && python3 tools/budget.py add "$WORK/run.json" > /dev/null)
grep -q '"cost_usd": 1.25' "$FX/state/BUDGET.jsonl" && echo "ok: b2 cost parsed into ledger" || echo "fail: b2"

# b3 — add from garbage: null, never a guess
printf 'not json' > "$WORK/garbage.json"
(cd "$FX" && python3 tools/budget.py add "$WORK/garbage.json" > /dev/null)
tail -1 "$FX/state/BUDGET.jsonl" | grep -q '"cost_usd": null' && echo "ok: b3 unparseable -> null (never a guess)" || echo "fail: b3"

# b4 — corrupt ledger line is skipped, not fatal
echo '{{{corrupt' >> "$FX/state/BUDGET.jsonl"
out=$( (cd "$FX" && LOOP_MONTHLY_BUDGET_USD=100 python3 tools/budget.py check) ); rc=$?
[ "$rc" -eq 0 ] && echo "$out" | grep -q 'clear to run' && echo "ok: b4 corrupt line skipped, under cap clear" || echo "fail: b4 rc=$rc out=$out"

# b5 — GOVERNOR HALT at/over the cap (exit 1)
out=$( (cd "$FX" && LOOP_MONTHLY_BUDGET_USD=1 python3 tools/budget.py check) ); rc=$?
[ "$rc" -eq 1 ] && echo "$out" | grep -q "GOVERNOR HALT" && echo "ok: b5 over cap -> halt, exit 1" || echo "fail: b5 rc=$rc out=$out"

# b6 — report divides by shipped without crashing
out=$( (cd "$FX" && python3 tools/budget.py report) )
echo "$out" | grep -q 'shipped plugins 2' && echo "ok: b6 report reads marketplace" || echo "fail: b6 out=$out"

# ---------- metrics.py ----------
cat > "$FX/bin/gh" << 'GH'
#!/usr/bin/env bash
# stub gh api: fixture per endpoint; MODE=dead simulates total API failure
[ "${MODE:-}" = "dead" ] && exit 1
case "$2" in
  repos/t/r) echo '{"stargazers_count": 7, "subscribers_count": 3, "forks_count": 2}' ;;
  repos/t/r/traffic/*) exit 1 ;;  # traffic API often 403s on new repos — must record null
  *labels=idea*) echo '[{"number": 5, "title": "an idea", "reactions": {"+1": 4}, "html_url": "u"}]' ;;
  *) echo '[]' ;;
esac
GH
chmod +x "$FX/bin/gh"

# m1 — live stub: real values recorded, unreachable traffic recorded as null
(cd "$FX" && PATH="$FX/bin:$PATH" GITHUB_REPOSITORY=t/r python3 tools/metrics.py > /dev/null)
python3 - "$FX" << 'PY'
import json, sys, pathlib
snap = json.loads(pathlib.Path(sys.argv[1] + "/state/METRICS.jsonl").read_text().splitlines()[-1])
ok = (snap["stars"] == 7 and snap["views_14d"] is None
      and snap["open_ideas"] == 1 and snap["idea_votes_total"] == 4)
print(("ok: " if ok else "fail: ") + f"m1 real values + honest nulls (stars=7, views=None, votes=4) got {snap['stars']},{snap['views_14d']},{snap['idea_votes_total']}")
PY

# m2 — votes.json ranked and written
python3 - "$FX" << 'PY'
import json, sys, pathlib
v = json.loads(pathlib.Path(sys.argv[1] + "/foundry/votes.json").read_text())
print(("ok: " if v.get("5", {}).get("votes") == 4 else "fail: ") + "m2 votes.json carries the +1 count")
PY

# m3 — total API failure: every remote field null, zero guesses
(cd "$FX" && PATH="$FX/bin:$PATH" MODE=dead GITHUB_REPOSITORY=t/r python3 tools/metrics.py > /dev/null)
python3 - "$FX" << 'PY'
import json, sys, pathlib
snap = json.loads(pathlib.Path(sys.argv[1] + "/state/METRICS.jsonl").read_text().splitlines()[-1])
remote = [snap[k] for k in ("stars", "watchers", "forks", "views_14d", "uniques_14d", "clones_14d", "pageviews_total")]
print(("ok: " if all(v is None for v in remote) else "fail: ") + "m3 dead API -> all nulls, never a guess")
PY
