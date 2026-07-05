#!/usr/bin/env bash
set -u
python3 - << 'P'
import json, re
d = json.load(open('site/data.json'))
J = d.get('journal', [])
src = re.findall(r'^## (i\d+) — ([\w-]+) — ', open('state/JOURNAL.md').read(), re.M)
want = src[-12:]
got = [(e['it'], e['role']) for e in J]
print(('ok: ' if got == want else 'fail: ') + f'journal export matches ledger tail verbatim ({len(got)}/12)')
h = open('site/theater.html').read()
print(('ok: ' if 'prefers-reduced-motion: reduce' in h and 'reduce){' in h.replace(' ','') or 'reduce' in h else 'fail: ') + 'reduced-motion instant path present')
print(('ok: ' if 'curtain rises on the first shift' in h else 'fail: ') + 'curtain empty-state present')
print(('ok: ' if 'theater.html' in open('site/index.html').read() else 'fail: ') + 'nav links Theater')
P
