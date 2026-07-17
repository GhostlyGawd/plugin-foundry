#!/usr/bin/env bash
set -u
if grep -q 'const SHIFT_ENABLED = false;' site/index.html \
  && grep -q 'model shifts paused · interactive sessions only' site/index.html \
  && ! grep -q 'schedule:' .github/workflows/run-shift.yml; then
  echo "ok: window reports the model shift as paused"
else
  echo "fail: window invents an active model schedule"
fi
