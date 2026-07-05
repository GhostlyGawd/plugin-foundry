#!/usr/bin/env bash
set -u
python3 - << 'P'
h = open('site/index.html').read()
ok = True
i = 0
while True:
    i = h.find('animation:', i + 1)
    if i < 0: break
    if 'no-preference' not in h[max(0, i-400):i]:
        ok = False
print(('ok: ' if ok else 'fail: ') + 'every animation sits under a reduced-motion guard')
print(('ok: ' if 'prefers-reduced-motion:reduce' in h else 'fail: ') + 'reduce fallback present')
print(('ok: ' if 'aria-pressed' in h else 'fail: ') + 'chips expose aria-pressed')
P
