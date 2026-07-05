#!/usr/bin/env bash
set -u
ok=1
for p in plugin-smith fork-a-foundry commit-craft session-recap env-doctor pr-narrator; do
  grep -q 'class="term"' "site/p/$p.html" && grep -q 'authored example' "site/p/$p.html" || { echo "fail: $p missing terminal or label"; ok=0; }
done
[ $ok -eq 1 ] && echo "ok: all 6 published plugins render labeled terminal sessions"
grep -q 'class="term"' site/p/community-voting.html && echo "fail: feature grew a terminal" || echo "ok: records without the section render nothing extra"
