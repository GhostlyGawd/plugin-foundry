#!/usr/bin/env bash
set -u
python3 - << 'P'
import re, glob
n = 0
for f in glob.glob('foundry/records/*.md'):
    n += len(re.findall(r'Sharpest question', open(f).read()))
got = open('site/saga.html').read().count('<li><b>') - open('site/saga.html').read().count('ADR-') if False else None
import re as R
wall = R.search(r'<ul class="wall">(.*?)</ul>', open('site/saga.html').read(), R.S)
rendered = wall.group(1).count('<li>') if wall else 0
print(('ok: ' if rendered == n and n > 0 else 'fail: ') + f'wall count equals review sources ({rendered}/{n})')
P
