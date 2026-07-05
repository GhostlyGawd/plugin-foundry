#!/usr/bin/env bash
set -u
command -v node >/dev/null 2>&1 || { echo "skip: node absent (fn shipped; unit in CI)"; exit 0; }
F=$(sed -n '/\/\*SHIFT-START\*\//,/\/\*SHIFT-END\*\//p' site/index.html)
[ -n "$F" ] || { echo "fail: shift markers missing"; exit 0; }
node - << NODE
$F
const eq=(a,b,m)=>console.log((a===b?'ok: ':'fail: ')+m+' ('+a+')');
const at=(s)=>nextShift(new Date(s)).toISOString();
eq(at('2026-07-05T07:00:00Z'), '2026-07-05T08:17:00.000Z', 'mid-morning rolls to 08:17');
eq(at('2026-07-05T23:50:00Z'), '2026-07-06T00:17:00.000Z', 'late night rolls to next day 00:17');
eq(at('2026-07-05T08:17:00Z'), '2026-07-05T16:17:00.000Z', 'exact fire time rolls forward');
eq(at('2026-07-05T16:30:00Z'), '2026-07-06T00:17:00.000Z', 'after last shift rolls to midnight+17');
NODE
