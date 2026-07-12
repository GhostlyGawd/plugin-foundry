#!/usr/bin/env python3
"""guard.py — constitutional enforcement (MASTER P0.5, ADR-027).

Rules on a proposed changeset BEFORE the orchestrator lands it:
  allow — within the agent's capability and the constitution
  desk  — lawful only with the operator's ratification (queued via desk.py)
  block — Article I; never lands, no override path in code

A changeset is a JSON list of {"path": "...", "action": "add|modify|delete"}.
Guard checks paths and actions against charter/CONSTITUTION.md +
charter/AGENTS.md capability scopes; content-level threats are fence.py and
red-team territory, not path law. Fails closed: unknown agent → block.

CLI:
  guard.py --agent <id> --changes <file.json|-> [--queue] [--root DIR]
Exit codes: 0 allow · 3 desk · 4 block (scriptable by the orchestrator).
"""
import argparse
import json
import sys
from fnmatch import fnmatch

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import load_agents  # noqa: E402

# Article I §5 — the law book: the gates, the schemas that define lawfulness,
# the guard itself, the protocol, and the charter. lib.py is included because
# every gate trusts its loader (one parser, one truth).
LAW_BOOK = (
    "tools/validate.py", "tools/guard.py", "tools/validate_state.py",
    "tools/lib.py", "foundry/SCHEMA.md", "foundry/agents/schema.json",
    "LOOP.md", "loop.sh",
)
LAW_BOOK_PREFIXES = ("charter/",)

# Article I §2 — history is append-only or immutable; deleting it is blocked.
NO_DELETE_PREFIXES = ("state/JOURNAL.md", "state/DECISIONS.md", "reviews/",
                      "foundry/records/")

ALLOW, DESK, BLOCK = "allow", "desk", "block"
_RANK = {ALLOW: 0, DESK: 1, BLOCK: 2}


def _is_law_book(path):
    return path in LAW_BOOK or any(path.startswith(p) for p in LAW_BOOK_PREFIXES)


def check(agent_id, changes, root="."):
    """Return (overall_verdict, [(path, verdict, reason), ...])."""
    errors = []
    agents = {a["id"]: a for a in load_agents(errors, root)}
    if errors:
        return BLOCK, [("registry", BLOCK,
                        f"agent registry unlawful: {errors[0]} — guard fails closed")]
    agent = agents.get(agent_id)
    if agent is None:
        return BLOCK, [("*", BLOCK,
                        f"unknown agent '{agent_id}' — no manifest, no pen (Art. IV)")]

    cap = agent["capability"]
    glob = cap[7:] if cap.startswith("writes:") else None
    verdicts = []
    for ch in changes:
        path = ch.get("path", "")
        action = ch.get("action", "modify")
        if not path or path.startswith("/") or ".." in path.split("/"):
            verdicts.append((path or "?", BLOCK, "path escapes the repo"))
            continue
        # Art. I §2 — deleting history
        if action == "delete" and any(path == p or path.startswith(p)
                                      for p in NO_DELETE_PREFIXES):
            verdicts.append((path, BLOCK,
                             "Article I §2: history is append-only; deletion blocked"))
            continue
        # Art. I §5 / Art. II — the law book is human-ratified, every agent
        if _is_law_book(path):
            verdicts.append((path, DESK,
                             "Article I §5: law-book change — operator ratification"))
            continue
        # Art. I §6 — no agent edits its own governing rule
        if path.startswith(f"foundry/agents/{agent_id}/"):
            verdicts.append((path, DESK,
                             "Article I §6: own governing rule — desk decides"))
            continue
        # Capability scope (charter/AGENTS.md)
        if glob is None:
            if cap == "proposes":
                verdicts.append((path, DESK,
                                 "capability 'proposes': lands only with desk approval"))
            else:
                verdicts.append((path, BLOCK,
                                 "capability 'read_only': no changesets at all"))
            continue
        if fnmatch(path, glob):
            verdicts.append((path, ALLOW, f"in scope (writes:{glob})"))
        else:
            verdicts.append((path, BLOCK,
                             f"out of capability scope (writes:{glob})"))
    overall = ALLOW
    for _, v, _r in verdicts:
        if _RANK[v] > _RANK[overall]:
            overall = v
    return overall, verdicts


def main(argv=None):
    ap = argparse.ArgumentParser(prog="guard.py")
    ap.add_argument("--agent", required=True)
    ap.add_argument("--changes", required=True,
                    help="JSON file of [{path, action}] or '-' for stdin")
    ap.add_argument("--queue", action="store_true",
                    help="on 'desk' verdict, queue the item via desk.py")
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)

    raw = sys.stdin.read() if args.changes == "-" else open(args.changes).read()
    try:
        changes = json.loads(raw)
        assert isinstance(changes, list)
    except (ValueError, AssertionError):
        print("guard: changes must be a JSON list of {path, action}")
        return 4

    overall, verdicts = check(args.agent, changes, args.root)
    for path, v, reason in verdicts:
        print(f"guard: {v.upper():5s} {path} — {reason}")
    print(f"guard: VERDICT {overall.upper()} ({args.agent}, {len(changes)} changes)")

    if overall == DESK and args.queue:
        import desk
        desk_paths = [p for p, v, _ in verdicts if v == DESK]
        title = f"ratify: {args.agent} → {', '.join(desk_paths[:3])}" + (
            "…" if len(desk_paths) > 3 else "")
        body = "\n".join(f"{v.upper()} {p} — {r}" for p, v, r in verdicts)
        ledger = os.path.join(args.root, "state", "DESK.jsonl")
        iid, fresh = desk.add("ratify", title, body, args.agent, path=ledger)
        print(f"guard: desk item {iid} ({'queued' if fresh else 'already open'})")

    return {ALLOW: 0, DESK: 3, BLOCK: 4}[overall]


if __name__ == "__main__":
    raise SystemExit(main())
