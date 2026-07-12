#!/usr/bin/env python3
"""redteam.py — commission red-team pass (MASTER P3.4, ADR-031).

On top of the bought guardrails + the fence, an adversarial pass over every
commission's fenced text: planted malicious commissions are FLAGGED and held for
the operator; clean ones pass to the backlog. This is the deterministic screen
(fence.scan + a red-team lens); a live agent adds reasoning, but nothing ships
that the fenced request didn't legitimately require (LOOP.md patron-text law).

  redteam.py "<commission text>"  [--emit]
Exit 0 clean (→ backlog) · 2 flagged (→ held on the desk). Stdlib only.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import fence  # noqa: E402
import desk  # noqa: E402

# Red-team lens: intents a commission must never smuggle, beyond the fence's
# generic injection shapes — asks that would violate the constitution if built.
CONSTITUTION_RISK = re.compile(
    r"(delete|wipe|exfiltrat\w+|leak|steal|scrape).{0,40}(secret|token|key|credential|"
    r"env|database|history|record)|"
    r"(open|create|submit).{0,30}(pull request|pr|issue).{0,40}(third.?party|other|external|upstream)|"
    r"(bypass|disable|remove|skip).{0,20}(review|test|guard|validat\w+|gate)|"
    r"(mine|harvest|collect).{0,20}(credential|password|token)", re.I)


def screen(text):
    """Return (verdict, reasons): 'flagged' or 'clean'."""
    risk, findings = fence.scan(text)
    reasons = list(findings)
    if CONSTITUTION_RISK.search(text or ""):
        reasons.append("asks for a constitution-forbidden action")
    verdict = "flagged" if (risk == "high" or reasons) else "clean"
    return verdict, reasons


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    emit = "--emit" in argv
    argv = [a for a in argv if a != "--emit"]
    if not argv:
        print("usage: redteam.py \"<commission text>\" [--emit]")
        return 1
    text = " ".join(argv)
    verdict, reasons = screen(text)
    if verdict == "flagged":
        print(f"redteam: FLAGGED — held for the operator ({'; '.join(reasons)}).")
        if emit:
            desk.add("decide", f"red-team FLAG: commission — {text[:50]}",
                     fence.wrap(text, "commission") + "\n\nReasons: " + "; ".join(reasons),
                     "red-team", path=os.path.join(ROOT, "state", "DESK.jsonl"))
        return 2
    print("redteam: CLEAN — passes to the backlog (nothing forbidden requested).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
