#!/usr/bin/env bash
set -u
python3 - << 'PY'
import subprocess, pathlib, re, json
rec = pathlib.Path('foundry/records/counter-index.md')
orig = rec.read_text()
try:
    fx = orig.replace('created: 2026-07-05', 'created: 2026-07-05\nprospected_by: test-owl\nsuggested_in: 99', 1)
    rec.write_text(fx)
    subprocess.run(['python3','tools/build.py'], check=True, capture_output=True)
    svg = pathlib.Path('site/card/test-owl.svg')
    ok = svg.exists()
    t = svg.read_text() if ok else ''
    print(('ok: ' if ok else 'fail: ') + 'fixture prospector yields a card')
    print(('ok: ' if '@test-owl' in t and '1 prospect' in t and 'since 2026-07-05' in t else 'fail: ') + 'counts + since derive from records')
    ext = ('href="http' in t) or ('<image' in t) or ('url(' in t) or ('@import' in t)
    print(('ok: ' if not ext and 'font-family' in t else 'fail: ') + 'self-contained SVG (no external fetches)')
    print(('ok: ' if 'contributor card →' in open('site/p/counter-index.html').read() else 'fail: ') + 'certificate links the card')
finally:
    rec.write_text(orig)
    subprocess.run(['python3','tools/build.py'], check=True, capture_output=True)
empty = not pathlib.Path('site/card').exists() or not list(pathlib.Path('site/card').glob('*.svg'))
print(('ok: ' if empty else 'fail: ') + 'empty hall renders nothing')
PY
