#!/usr/bin/env python3
"""diagnose.py — the failed-shift diagnostician (MASTER P1.3, ADR-031).

A forced (or real) failure → a plausible root cause + a next step, opened as an
ops-alarm. Deterministic classification over the run logs and the journal tail;
a live agent can elaborate, but the triage below stands on its own. Reuses the
auth surface's classifier so auth failures are named the same way everywhere.

  diagnose.py <logfile...>     classify + print the diagnosis (exit 2 if a
                               failure was identified, 0 if none)
  diagnose.py --alarm <log...> also open an ops-alarm via tools/alarm.py
Stdlib only.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import auth  # noqa: E402

# (regex, cause, next step) — ordered; first match wins per log
CLASSIFIERS = [
    (re.compile(r"governor halt|budget.*exhausted|LOOP_MONTHLY_BUDGET", re.I),
     "budget governor halt",
     "check state/BUDGET.jsonl; raise LOOP_MONTHLY_BUDGET_USD or wait for the month to roll (RUNBOOK)."),
    (re.compile(r"quota.*(SHED|HALT|kill switch)|weekly window", re.I),
     "quota governor shed/halt (subscription rate pressure)",
     "the desk holds an approve item; raise QUOTA_WEEKLY_RUNS or wait for the weekly window."),
    (re.compile(r"VALIDATE: FAIL|STATE: FAIL|BUILD:.*error|is not semver|drift", re.I),
     "a gate went red (validate/state/build)",
     "run the failing gate locally; the message names the exact law; fix or revert — never leave main red."),
    (re.compile(r"no space left on device|ENOSPC", re.I),
     "disk allowance exhausted",
     "delete build artifacts/caches (freed space is immediately writable); a fresh session only if cleanup can't free enough."),
]


def classify(text):
    # auth first — it's the most common and the most silently dangerous
    for sig in auth.AUTH_SIGNATURES:
        if re.search(sig, text.lower()):
            return ("authentication failure (token rejected/expired)",
                    "run auth.py probe for classification, then reopen the repo in an "
                    "attended interactive session; never provision a CI model secret "
                    "(ADR-032 / RUNBOOK).")
    for pat, cause, step in CLASSIFIERS:
        if pat.search(text):
            return cause, step
    return None


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    alarm = "--alarm" in argv
    argv = [a for a in argv if a != "--alarm"]
    # Classify the RUN LOG only — the journal tail is narrative context for a
    # human/LLM, never classifier input (past incidents in the journal must not
    # masquerade as the current failure's cause).
    text = ""
    for p in argv:
        try:
            text += open(p, encoding="utf-8", errors="replace").read() + "\n"
        except OSError:
            continue

    result = classify(text)
    if not result:
        print("diagnose: no known failure signature — inspect the raw run log.")
        return 0
    cause, step = result
    print(f"diagnose: ROOT CAUSE — {cause}")
    print(f"diagnose: NEXT STEP — {step}")
    if alarm:
        subprocess.run(
            [sys.executable, os.path.join(ROOT, "tools", "alarm.py"),
             f"ops-alarm: shift failed — {cause}",
             f"Diagnostician (P1.3): {cause}. Next: {step}"], check=False)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
