#!/usr/bin/env bash
set -u
python3 - << 'PY'
import re, pathlib
h = pathlib.Path('site/almanac/2026-07.html').read_text()
j = open('state/JOURNAL.md').read()
month = len(re.findall(r'^## i\d+ — [\w-]+ — 2026-07', j, re.M))
m = re.search(r'(\d+) iterations? this month', h)
print(('ok: ' if m and int(m.group(1)) == month else 'fail: ') + f'iteration count matches the ledger ({m.group(1) if m else "?"}/{month})')
led = pathlib.Path('state/BUDGET.jsonl')
absent = (not led.exists()) or (not led.read_text().strip())
honest = 'no cost ledger yet' in h
print(('ok: ' if honest == absent else 'fail: ') + 'money section honest about the ledger state')
print(('ok: ' if pathlib.Path('site/almanac/index.html').exists() else 'fail: ') + 'editions index exists')
print(('ok: ' if 'almanac/index.html' in open('site/index.html').read() else 'fail: ') + 'nav links the Almanac')
PY
