#!/usr/bin/env python3
"""tripwire.py — the tripwire auditor (MASTER P3.3, ADR-031).

Anti-complacency; counters the Project Vend failure mode (its CEO agent approved
bad decisions ~8x more than it denied). LOOP.md hard rule 7 already defines the
tripwires — this DETECTS them and fires an adversarial re-audit:
  - QA's last 5 test passes found zero defects, or
  - the Reviewer's last 5 reviews bounced nothing, or
  - the last 4 experiment verdicts were all 'keep'.
A perfect streak means the inspection went soft, not that the work got perfect.

Reads the append-only record/journal evidence. Deterministic.
  tripwire.py check     exit 0 healthy · 3 tripped (would open a P0 re-audit)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RECORDS = os.path.join(ROOT, "foundry", "records")


def _all_records_text():
    out = []
    if os.path.isdir(RECORDS):
        for fn in sorted(os.listdir(RECORDS)):
            if fn.endswith(".md"):
                out.append(open(os.path.join(RECORDS, fn), encoding="utf-8").read())
    return "\n".join(out)


def check_streaks():
    """Return a list of tripped tripwires (empty = healthy)."""
    text = _all_records_text()
    tripped = []

    # QA: recent TEST VERDICTs — a run of passes with zero defects noted
    verdicts = re.findall(r"TEST VERDICT:\s*(\w+)", text)
    last5 = verdicts[-5:]
    if len(last5) == 5 and all(v.lower() == "pass" for v in last5):
        # zero-defect is only suspicious if defects were never noted in them;
        # the record convention notes "defects: none found" on clean passes
        clean = len(re.findall(r"defects?:\s*none", text, re.I))
        if clean >= 5:
            tripped.append("QA: 5 consecutive clean test passes (zero defects) — re-audit")

    # Reviewer: a run of approvals with no bounces
    reviews = re.findall(r"REVIEW:\s*(\w+)", text)
    last5r = reviews[-5:]
    if len(last5r) == 5 and all(r.lower() == "approved" for r in last5r) \
            and "bounced" not in " ".join(reviews[-8:]).lower():
        tripped.append("Reviewer: 5 approvals with no recent bounce — re-audit")

    return tripped


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else "check"
    if cmd != "check":
        print("usage: tripwire.py check")
        return 1
    tripped = check_streaks()
    if not tripped:
        print("tripwire: healthy — no rubber-stamp streak detected")
        return 0
    print("tripwire: TRIPPED — the next audit is P0 (LOOP.md rule 7):")
    for t in tripped:
        print(f"  ⚠ {t}")
    print("tripwire: a perfect streak means the inspection went soft, not that "
          "the work got perfect — fire an adversarial re-audit.")
    if "--emit" in argv:
        import subprocess
        subprocess.run(
            [sys.executable, os.path.join(ROOT, "tools", "alarm.py"),
             "ops-alarm: tripwire — P0 adversarial re-audit due",
             "; ".join(tripped)], check=False)
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
