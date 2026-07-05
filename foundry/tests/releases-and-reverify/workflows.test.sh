#!/usr/bin/env bash
set -u
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/release-on-tag.yml'))" && echo "ok: release-on-tag lints" || echo "fail: release-on-tag yaml"
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/qa.yml'))" && echo "ok: qa.yml lints" || echo "fail: qa.yml yaml"
grep -q 'cron: "17 6 \* \* 1"' .github/workflows/qa.yml && echo "ok: weekly cron armed" || echo "fail: cron"
grep -q "github.event_name == 'schedule'" .github/workflows/qa.yml && echo "ok: reverify schedule-guarded" || echo "fail: schedule guard"
grep -q "ops-alarm" .github/workflows/qa.yml && grep -q "ops-alarm" .github/workflows/release-on-tag.yml && echo "ok: both fail to an alarm, never silently" || echo "fail: alarms"
python3 - << 'PY'
import sys; sys.path.insert(0, 'tools')
from restamp import parse_failed, stamp_text
ok = lambda c, m: print(('ok: ' if c else 'fail: ') + m)
out = "  [good-one] ok: fine\n  [bad-one] fail: broke\n  [bad-one] ok: other\n"
ok(parse_failed(out) == {"bad-one"}, "failed-suite parser isolates red suites")
t = "---\nname: x\nverified: 2026-01-01\ncomponents: [skills]\n---\n"
ok("verified: 2026-07-05" in stamp_text(t, "2026-07-05"), "existing stamp refreshes")
t2 = "---\nname: y\ncomponents: [skills]\n---\n"
ok("verified: 2026-07-05\ncomponents:" in stamp_text(t2, "2026-07-05"), "missing stamp inserts before components")
PY
