#!/usr/bin/env python3
"""ask.py — ask-the-factory (MASTER P1.2, ADR-031). "Talk to the company."

Natural-language query → a SOURCED answer over the workshop's own history
(JOURNAL, DECISIONS, records, reviews). This is the retrieval half — deterministic
and testable; a live agent narrates the top hits into prose. Every hit carries its
source, so the answer can never be an ungrounded claim (growth-honesty).

  ask.py "why did session-recap bounce?"  [--k N]
Ranks passages by query-term overlap; ties broken by source order. Stdlib only.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOURCES = [
    ("JOURNAL", os.path.join(ROOT, "state", "JOURNAL.md"), r"^## (i\d+ — [\w-]+ — \S+)"),
    ("DECISIONS", os.path.join(ROOT, "state", "DECISIONS.md"), r"^## (ADR-\d+.*)"),
]


def _passages():
    """Yield (source_label, heading, text) across the history files + records."""
    for label, path, hdr in SOURCES:
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        parts = re.split(hdr, text, flags=re.M)
        # parts = [pre, head1, body1, head2, body2, ...]
        for i in range(1, len(parts), 2):
            yield label, parts[i].strip(), parts[i + 1] if i + 1 < len(parts) else ""
    recdir = os.path.join(ROOT, "foundry", "records")
    if os.path.isdir(recdir):
        for fn in sorted(os.listdir(recdir)):
            if fn.endswith(".md"):
                yield "record", fn[:-3], open(os.path.join(recdir, fn), encoding="utf-8").read()


def _words(t):
    return set(re.findall(r"[a-z0-9]+", t.lower()))


STOP = _words("the a an of to and in for on is it why did was how what when where "
              "does do with that this last week from")


def answer(query, k=3):
    qw = _words(query) - STOP
    scored = []
    for i, (label, head, body) in enumerate(_passages()):
        bw = _words(head + " " + body)
        overlap = len(qw & bw)
        if overlap:
            scored.append((overlap, i, label, head, body))
    scored.sort(key=lambda t: (-t[0], t[1]))
    return scored[:k]


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: ask.py \"<question>\" [--k N]")
        return 1
    k = 3
    if "--k" in argv:
        i = argv.index("--k")
        k = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    query = " ".join(argv)
    hits = answer(query, k)
    if not hits:
        print("ask: no sourced answer in the history for that query.")
        return 0
    print(f"ask: {len(hits)} sourced passage(s) for “{query}”:\n")
    for overlap, _i, label, head, body in hits:
        snippet = re.sub(r"\s+", " ", body).strip()[:220]
        print(f"— [{label}] {head}  (relevance {overlap})")
        print(f"  {snippet}…\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
