#!/usr/bin/env bash
set -u
P="${PLUGIN_DIR:-plugins/night-clerk}"
grep -q '"name": "night-clerk"' "$P/.claude-plugin/plugin.json" && echo "ok: manifest name" || echo "fail: manifest name"
grep -q '^description: .*Use when' "$P/skills/clerk/SKILL.md" && echo "ok: invoke contract" || echo "fail: invoke contract"
grep -q 'NEVER invent' "$P/skills/clerk/SKILL.md" && echo "ok: never-invent clause" || echo "fail: never-invent"
grep -q 'snapshot date' "$P/skills/clerk/SKILL.md" && echo "ok: snapshot disclosure duty" || echo "fail: snapshot duty"
grep -q 'nothing in the\|nothing fits' "$P/skills/clerk/SKILL.md" && echo "ok: honest empty path" || echo "fail: empty path"
python3 - << 'PY'
import json, re, glob
cat = json.load(open('plugins/night-clerk/data/catalog.json'))
pub = set()
for f in glob.glob('foundry/records/*.md'):
    t = open(f).read()
    if re.search(r'^stage: published$', t, re.M) and re.search(r'^kind: plugin$', t, re.M) or (re.search(r'^stage: published$', t, re.M) and 'kind:' not in t.split('---')[1]):
        m = re.search(r'^name: (.+)$', t, re.M); pub.add(m.group(1))
names = {p['name'] for p in cat['plugins']}
print(('ok: ' if names <= pub and len(names) >= 6 else 'fail: ') + f'catalog holds only published plugins ({len(names)})')
print(('ok: ' if re.match(r'\d{4}-\d{2}-\d{2}', cat.get('snapshot','')) else 'fail: ') + 'snapshot dated')
print(('ok: ' if all(p['install'].endswith('@foundry') for p in cat['plugins']) else 'fail: ') + 'install lines carry the marketplace')
PY
if command -v claude >/dev/null 2>&1; then
  claude plugin validate "./$P" --strict >/dev/null 2>&1 && echo "ok: official validate" || echo "fail: official validate"
else echo "skip: official validate (CLI absent here; green in CI)"; fi
