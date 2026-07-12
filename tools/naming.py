#!/usr/bin/env python3
"""naming.py — the naming ceremony assistant (MASTER P2.5, ADR-031).

A published plugin's `name` is an immutable slug (LOOP.md: names are forever).
Choosing one badly — a collision with an existing slug, or a near-miss that
confuses install commands — is unfixable after users install. This checks a
candidate against every existing slug and obvious collisions BEFORE the name
spreads, and reports clean candidates.

  naming.py check <candidate>          available? or which collision
  naming.py suggest <word> [word...]   filter proposed candidates to the clean ones
Stdlib only. Deterministic.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from lib import parse_front_matter  # noqa: E402

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# reserved: words that would collide with the workshop's own vocabulary/paths
RESERVED = {"foundry", "plugin", "plugins", "marketplace", "claude", "anthropic",
            "tools", "state", "charter", "site", "loop", "orchestrator", "guard"}


def existing_slugs():
    slugs = set()
    mp_path = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
    if os.path.exists(mp_path):
        for p in json.load(open(mp_path, encoding="utf-8")).get("plugins", []):
            slugs.add(p.get("name"))
    recdir = os.path.join(ROOT, "foundry", "records")
    if os.path.isdir(recdir):
        for fn in os.listdir(recdir):
            if fn.endswith(".md"):
                meta, _ = parse_front_matter(open(os.path.join(recdir, fn), encoding="utf-8").read())
                if meta.get("name"):
                    slugs.add(meta["name"])
    return {s for s in slugs if s}


def _norm(s):
    # collapse separators so "todo-ledger" ~ "todoledger" ~ "todo_ledger"
    return re.sub(r"[-_\s]", "", s.lower())


def check(candidate):
    """Return (ok, reason). ok=True means the slug is free + well-formed."""
    c = candidate.strip().lower()
    if not SLUG_RE.match(c):
        return False, f"not a valid slug (kebab-case [a-z0-9-], no leading/trailing dash): {candidate!r}"
    if c in RESERVED:
        return False, f"reserved word (collides with the workshop's vocabulary): {c}"
    slugs = existing_slugs()
    if c in slugs:
        return False, f"exact collision with an existing plugin: {c}"
    norm = _norm(c)
    for s in slugs:
        if _norm(s) == norm:
            return False, f"near-collision with existing slug {s!r} (same letters, different separators)"
    return True, "available — well-formed, no collision"


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) >= 2 and argv[0] == "check":
        ok, reason = check(argv[1])
        print(f"naming: {'✔ ' if ok else '✖ '}{argv[1]} — {reason}")
        return 0 if ok else 1
    if len(argv) >= 2 and argv[0] == "suggest":
        clean = [w for w in argv[1:] if check(w)[0]]
        rejected = [w for w in argv[1:] if not check(w)[0]]
        print(f"naming: clean candidates — {', '.join(clean) or '(none)'}")
        if rejected:
            print(f"naming: rejected — {', '.join(rejected)}")
        return 0
    print("usage: naming.py check <candidate> | suggest <word> [word...]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
