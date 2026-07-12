#!/usr/bin/env python3
"""steer.py — steer-by-issue (MASTER P2.2, ADR-031). "Run my company from my phone."

A one-sentence steering issue → a valid backlog item. But a sentence that touches
the LAW BOOK (protocol, charter, validator, schema, constitution) must NOT become
a silent backlog item — it routes to the owner's desk for ratification. This is
the deterministic classifier + emitter; the text is fenced UNTRUSTED first (it
arrives from an issue).

  steer.py "add a plugin that lints yaml"            → backlog item
  steer.py "change the validator to allow X"         → desk (rule-touching)
Prints the classification + the emitted item. Stdlib only.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import fence  # noqa: E402
import desk  # noqa: E402

# Law-book / rule-touching signals — a match routes to the desk, not the backlog.
RULE_CX = re.compile(
    r"\b(loop\.md|loop\.sh|charter|validat\w*|schema|constitution|guard|"
    r"protocol|the rule|governing|two-iteration|quality bar|test(ing)? bar|"
    r"orchestrat\w*|law book|semver law|version law)\b", re.I)


def classify(sentence):
    risk, findings = fence.scan(sentence)
    fenced = fence.wrap(sentence, source="steer-issue")
    rule_touching = bool(RULE_CX.search(sentence))
    if risk == "high":
        # a steering sentence that scans high is held for the red-team, not obeyed
        return "flagged", fenced, findings
    return ("desk" if rule_touching else "backlog"), fenced, findings


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    emit = "--emit" in argv
    argv = [a for a in argv if a != "--emit"]
    if not argv:
        print("usage: steer.py \"<one-sentence steer>\" [--emit]")
        return 1
    sentence = " ".join(argv)
    verdict, fenced, findings = classify(sentence)

    if verdict == "flagged":
        print(f"steer: FLAGGED — the steer scanned high-risk ({', '.join(findings)}); "
              f"held for the red-team, not actioned.")
        return 2
    if verdict == "desk":
        print("steer: RULE-TOUCHING → the owner's desk (ratification, not a silent backlog item).")
        if emit:
            iid, fresh = desk.add("ratify", f"steer (rule-touching): {sentence[:60]}",
                                  fenced, "steer-by-issue",
                                  path=os.path.join(ROOT, "state", "DESK.jsonl"))
            print(f"steer: desk item {iid} ({'queued' if fresh else 'already open'})")
    else:
        print("steer: BACKLOG → a normal Idea-inbox item (fenced, UNTRUSTED).")
        if emit:
            print("steer: (emit to the outbox → orchestrator lands it in BACKLOG § Idea inbox)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
