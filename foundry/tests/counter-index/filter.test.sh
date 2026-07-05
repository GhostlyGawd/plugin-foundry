#!/usr/bin/env bash
set -u
command -v node >/dev/null 2>&1 || { echo "skip: node absent here (filter fn shipped; unit runs in CI)"; exit 0; }
F=$(sed -n '/\/\*FILTER-START\*\//,/\/\*FILTER-END\*\//p' site/index.html)
[ -n "$F" ] || { echo "fail: filter markers missing from built window"; exit 0; }
node - << NODE
$F
const E = [
 {name:'commit-craft', title:'Commit Craft', one_liner:'guard', tags:['git','hook'], category:'workflow', components:['skills','hooks'], stage:'published'},
 {name:'env-doctor', title:'Env Doctor', one_liner:'diagnose env', tags:['doctor'], category:'quality', components:['skills'], stage:'published'},
];
const eq=(a,b,m)=>console.log((JSON.stringify(a)===JSON.stringify(b)?'ok: ':'fail: ')+m);
eq(filterCards('', null, E).length, 2, 'no filter shows all');
eq(filterCards('doctor', null, E).map(e=>e.name), ['env-doctor'], 'text match on one_liner+tags');
eq(filterCards('', 'git', E).map(e=>e.name), ['commit-craft'], 'tag chip filters');
eq(filterCards('craft', 'doctor', E).length, 0, 'text+tag combine (AND)');
eq(filterCards('zzz', null, E).length, 0, 'no-match empties');
NODE
