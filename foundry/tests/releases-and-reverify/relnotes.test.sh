#!/usr/bin/env bash
set -u
python3 - << 'PY'
import sys; sys.path.insert(0, 'tools')
from relnotes import extract
ok = lambda c, m: print(('ok: ' if c else 'fail: ') + m)
fx = "# Changelog\n\n## 0.2.0 — later\n- newer thing\n\n## 0.1.0 — 2026-07-05\n- first thing\n- second thing\n\n## 0.0.1 — draft\n- ancient\n"
s = extract(fx, "0.1.0")
ok(s is not None and "first thing" in s and "second thing" in s, "extracts the requested section")
ok("newer thing" not in s and "ancient" not in s, "excludes every other version")
ok(extract(fx, "9.9.9") is None, "absent version returns none (release refuses)")
real = open('plugins/commit-craft/CHANGELOG.md').read()
r = extract(real, "0.1.0")
ok(r is not None and "0.1.0" in r, "real commit-craft 0.1.0 extracts")
PY
python3 tools/relnotes.py plugins/commit-craft/CHANGELOG.md 9.9.9 >/dev/null 2>&1 && echo "fail: missing version should exit 1" || echo "ok: CLI exits 1 on missing version"
