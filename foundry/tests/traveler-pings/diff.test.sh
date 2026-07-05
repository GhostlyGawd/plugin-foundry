#!/usr/bin/env bash
set -u
python3 - << 'PY'
import sys; sys.path.insert(0, 'tools')
from pings import diff
old = {"a": {"stage": "spec", "suggested_in": "7", "title": "A"},
       "b": {"stage": "rc",   "suggested_in": "8", "title": "B"},
       "c": {"stage": "spec", "suggested_in": None, "title": "C"}}
new = {"a": {"stage": "building", "suggested_in": "7", "title": "A"},
       "b": {"stage": "published", "suggested_in": "8", "title": "B"},
       "c": {"stage": "rc", "suggested_in": None, "title": "C"},
       "d": {"stage": "idea", "suggested_in": "9", "title": "D"},
       "e": {"stage": "spec", "suggested_in": "7", "title": "E"}}
p = dict(diff(old, new))
ok = lambda c, m: print(('ok: ' if c else 'fail: ') + m)
ok('7' in p and 'spec` → `building' in p['7'], 'stage-up pings the issue')
ok('8' in p and 'shipped' in p['8'], 'publish gets the shipped telegram')
ok('9' in p and 'enters at `idea' in p['9'], 'newly created record pings')
ok(set(p.keys()) == {'7','8','9'}, 'no-issue records stay silent')
ok(len([1 for i,_ in diff(old,new) if i=='7']) == 1, 'one comment per issue per shift (e suppressed)')
ok(diff(new, new) == [], 'no change, no noise')
PY
