#!/usr/bin/env python3
"""desk.py — the owner's desk, minimal Stage 0 primitive (MASTER P0.5→P0.8).

One ranked queue for every decision a human must make. This iteration ships the
ledger + dedup (guard.py routes ratification items here); ranking, pinned-issue
sync, and the site card land with ADR-029. Stdlib only.

Ledger: state/DESK.jsonl — append-only JSONL. Each line:
  {"id": "d-0001", "ts": "...", "kind": "ratify|approve|decide|alarm",
   "title": "...", "body": "...", "agent": "<source-agent>",
   "status": "open|approved|rejected", "resolution": "...", "refs": [...]}
Status changes append a resolution line (same id, status set) — the latest
line for an id wins; history is never rewritten.

CLI:
  desk.py add --kind ratify --title T [--body B] [--agent A] [--ref R ...]
  desk.py list [--open]
  desk.py resolve <id> approved|rejected [--note N]
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "state", "DESK.jsonl")


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_items(path=LEDGER):
    """Fold the ledger: latest line per id wins. Returns ordered dict id->item."""
    items = {}
    if not os.path.exists(path):
        return items
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                print(f"desk: WARNING malformed line {n} skipped", file=sys.stderr)
                continue
            iid = rec.get("id")
            if not iid:
                continue
            items[iid] = {**items.get(iid, {}), **rec}
    return items


def _append(rec, path=LEDGER):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def add(kind, title, body="", agent="", refs=None, path=LEDGER):
    """Queue an item. Dedup: an OPEN item with the same (kind, title) is
    returned instead of duplicated — the anti-firehose floor."""
    items = read_items(path)
    for it in items.values():
        if (it.get("kind"), it.get("title")) == (kind, title) and it.get("status") == "open":
            return it["id"], False
    iid = f"d-{len(items) + 1:04d}"
    _append({"id": iid, "ts": _now(), "kind": kind, "title": title,
             "body": body, "agent": agent, "status": "open",
             "refs": refs or []}, path)
    return iid, True


def resolve(iid, status, note="", path=LEDGER):
    items = read_items(path)
    if iid not in items:
        raise SystemExit(f"desk: no item {iid}")
    if status not in ("approved", "rejected"):
        raise SystemExit("desk: resolution must be approved|rejected")
    _append({"id": iid, "ts": _now(), "status": status, "resolution": note}, path)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="desk.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--kind", required=True,
                   choices=["ratify", "approve", "decide", "alarm"])
    a.add_argument("--title", required=True)
    a.add_argument("--body", default="")
    a.add_argument("--agent", default="")
    a.add_argument("--ref", action="append", default=[])
    ls = sub.add_parser("list")
    ls.add_argument("--open", action="store_true")
    r = sub.add_parser("resolve")
    r.add_argument("id")
    r.add_argument("status", choices=["approved", "rejected"])
    r.add_argument("--note", default="")
    args = ap.parse_args(argv)

    if args.cmd == "add":
        iid, fresh = add(args.kind, args.title, args.body, args.agent, args.ref)
        print(f"desk: {'queued' if fresh else 'already open'} {iid} [{args.kind}] {args.title}")
    elif args.cmd == "list":
        for it in read_items().values():
            if args.open and it.get("status") != "open":
                continue
            print(f"{it['id']} [{it.get('status')}] ({it.get('kind')}) "
                  f"{it.get('title')}" + (f" — {it.get('agent')}" if it.get("agent") else ""))
    elif args.cmd == "resolve":
        resolve(args.id, args.status, args.note)
        print(f"desk: {args.id} → {args.status}")


if __name__ == "__main__":
    main()
