#!/usr/bin/env bash
# verified-by-foundry acceptance checks 1–4 (record: foundry/records/verified-by-foundry.md)
set -uo pipefail
cd "${REPO_ROOT:-$(pwd)}"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# 1 — doctor passes every shipped plugin
allok=1
for p in plugins/*/; do
  python3 tools/doctor.py "$p" > /dev/null 2>&1 || { allok=0; echo "fail: check1 — doctor red on $p"; }
done
[ "$allok" -eq 1 ] && echo "ok: check1 doctor green on the whole shelf"

# 2 — doctor fails a broken fixture naming each law
B="$WORK/bad-plug"; mkdir -p "$B/.claude-plugin" "$B/hooks" "$B/scripts"
echo '{"name":"Bad_Plug","version":"1.0"}' > "$B/.claude-plugin/plugin.json"
printf '{"hooks":{"PreToolUsee":[{"matcher":".*","hooks":[{"type":"command","command":"${CLAUDE_PLUGIN_ROOT}/x.sh"}]}]}}\n' > "$B/hooks/hooks.json"
printf 'true\n' > "$B/scripts/x.sh"; chmod -x "$B/scripts/x.sh" 2>/dev/null
out=$(python3 tools/doctor.py "$B" 2>&1); rc=$?
if [ "$rc" -eq 1 ]; then
  for law in "kebab-case" "not semver" "unknown hook event" "matcher '.\*'" "unquoted" "not executable" "missing shebang"; do
    echo "$out" | grep -q "$law" && echo "ok: check2 law detected — $law" || echo "fail: check2 — law not named: $law"
  done
else echo "fail: check2 — broken fixture exited $rc"; fi

# 3 — action.yml: valid YAML, composite, references the doctor, defaults plugin-dir to .
python3 - << 'PY'
import sys
try:
    import yaml
except ImportError:
    print("skip: check3 yaml lib absent here (runs in CI)"); sys.exit(0)
a = yaml.safe_load(open(".github/actions/foundry-doctor/action.yml"))
runs = a.get("runs", {})
ok = (runs.get("using") == "composite"
      and a.get("inputs", {}).get("plugin-dir", {}).get("default") == "."
      and any("doctor.py" in (s.get("run") or "") for s in runs.get("steps", [])))
print(("ok: " if ok else "fail: ") + "check3 action.yml composite + doctor + default plugin-dir")
PY

# 4 — registry: empty renders nothing; fixture entry flows to the window data
python3 - << 'PY'
import json, pathlib, subprocess
d = json.load(open("site/data.json"))
print(("ok: " if d.get("verified") == [] else "fail: ") + "check4a empty registry -> empty data.verified")
reg = pathlib.Path("foundry/verified.json"); orig = reg.read_text()
try:
    reg.write_text(json.dumps({"verified": [{"repo": "octocat/example", "plugin_dir": ".",
                                             "verified": "2026-07-06", "run_url": "https://example.invalid/run/1"}]}))
    subprocess.run(["python3", "tools/build.py"], check=True, capture_output=True)
    d = json.load(open("site/data.json"))
    ok = d["verified"] and d["verified"][0]["repo"] == "octocat/example"
    print(("ok: " if ok else "fail: ") + "check4b fixture entry reaches the window data")
finally:
    reg.write_text(orig)
    subprocess.run(["python3", "tools/build.py"], check=True, capture_output=True)
PY
grep -q 'style="display:none"' site/index.html && grep -q 'id="verified"' site/index.html \
  && echo "ok: check4c verified section ships hidden until it has a first name" \
  || echo "fail: check4c section markup"

# 5 — v12 4.2: badges — empty registry emits nothing; fixture entry emits an SVG
python3 - << 'PY'
import json, pathlib, subprocess, re
assert not pathlib.Path("site/verified").exists() or not list(pathlib.Path("site/verified").glob("*.svg")), "badges exist with empty registry"
print("ok: check5a empty registry -> no badge files")
reg = pathlib.Path("foundry/verified.json"); orig = reg.read_text()
try:
    reg.write_text(json.dumps({"verified": [{"repo": "octo/ex", "plugin_dir": ".", "verified": "2026-07-07", "run_url": "https://example.invalid/1"}]}))
    subprocess.run(["python3", "tools/build.py"], check=True, capture_output=True)
    svg = pathlib.Path("site/verified/octo-ex.svg").read_text()
    assert "verified by the foundry" in svg and "2026-07-07" in svg and "a floor not a guarantee" in svg
    print("ok: check5b fixture entry -> SVG with date + honest-limits title")
finally:
    reg.write_text(orig)
    import shutil; shutil.rmtree("site/verified", ignore_errors=True)
    subprocess.run(["python3", "tools/build.py"], check=True, capture_output=True)
PY
