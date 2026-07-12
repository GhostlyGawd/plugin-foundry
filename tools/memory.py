#!/usr/bin/env python3
"""memory.py — the factory brain (MASTER P5.1, ADR-031). Long-term lessons,
injected into agents so the org stops relearning what it already knows.

BUY-shaped: a MEMORY_BACKEND seam can route to Mem0/Zep (desk-gated — they
bill/host). The floor and default is a local, curated store. The one piece
MASTER says to keep in-house is the discipline, and it's the whole design:

  DEDUP-ON-WRITE, never append-everything. A near-duplicate lesson is REFUSED,
  not stacked — the documented failure mode of memory frameworks is staleness
  and context-bloat from appending everything (pain theme #9). The store stays
  small and true: one lesson per real insight.

Store: foundry/memory.jsonl — {id, ts, lesson, tags, source}. Append-only file,
but writes are gated by a similarity check so duplicates never enter.

  memory.py add "<lesson>" [--tags a,b] [--source ref] [--force]
  memory.py recall "<query>" [--k N]      relevant lessons, scored
  memory.py list
Deterministic recall (token-overlap). Stdlib only. FOUNDRY_NOW injects the clock.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "foundry", "memory.jsonl")
DUP_THRESHOLD = 0.6   # Jaccard over word-sets above this = the same lesson


def _now():
    env = os.environ.get("FOUNDRY_NOW")
    if env:
        return datetime.fromisoformat(env.replace("Z", "+00:00"))
    return datetime.now(timezone.utc)


def _words(text):
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def _jaccard(a, b):
    wa, wb = _words(a), _words(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def read_all(path=STORE):
    out = []
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def nearest(lesson, path=STORE):
    """Return (best_score, item) of the closest existing lesson, or (0, None)."""
    best, best_item = 0.0, None
    for it in read_all(path):
        s = _jaccard(lesson, it.get("lesson", ""))
        if s > best:
            best, best_item = s, it
    return best, best_item


def add(lesson, tags=None, source="", force=False, path=STORE):
    """Dedup-on-write. Returns (id_or_None, status)."""
    lesson = (lesson or "").strip()
    if not lesson:
        return None, "empty"
    # backend seam: a real Mem0/Zep adapter would own dedup+store; we still
    # gate here so the discipline holds regardless of backend.
    backend = os.environ.get("MEMORY_BACKEND", "local").strip() or "local"
    if backend != "local":
        try:
            mod = __import__(f"memory_{backend}")
            return mod.add(lesson, tags, source)
        except Exception:  # noqa: BLE001 — fall back to the local floor
            print(f"memory: backend '{backend}' unavailable — local store used",
                  file=sys.stderr)
    score, dup = nearest(lesson, path)
    if dup and score >= DUP_THRESHOLD and not force:
        return dup["id"], f"refused-duplicate (of {dup['id']}, {score:.2f} overlap)"
    items = read_all(path)
    iid = f"m-{len(items) + 1:03d}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"id": iid, "ts": _now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "lesson": lesson, "tags": tags or [],
                            "source": source}, ensure_ascii=False) + "\n")
    return iid, "added"


def recall(query, k=3, path=STORE):
    """Deterministic relevance: token overlap, ties broken by recency (id)."""
    scored = []
    for it in read_all(path):
        s = _jaccard(query, it.get("lesson", "") + " " + " ".join(it.get("tags", [])))
        if s > 0:
            scored.append((round(s, 3), it))
    # score desc, ties broken by id asc — one deterministic order
    scored.sort(key=lambda t: (-t[0], t[1]["id"]))
    return scored[:k]


def main(argv=None):
    ap = argparse.ArgumentParser(prog="memory.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("lesson")
    a.add_argument("--tags", default="")
    a.add_argument("--source", default="")
    a.add_argument("--force", action="store_true")
    r = sub.add_parser("recall")
    r.add_argument("query")
    r.add_argument("--k", type=int, default=3)
    sub.add_parser("list")
    args = ap.parse_args(argv)

    if args.cmd == "add":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        iid, status = add(args.lesson, tags, args.source, args.force)
        print(f"memory: {status}" + (f" — {iid}" if iid else ""))
        return 0 if status in ("added",) or status.startswith("refused") else 1
    if args.cmd == "recall":
        hits = recall(args.query, args.k)
        if not hits:
            print("memory: no relevant lesson")
        for s, it in hits:
            print(f"memory: [{s}] {it['id']} — {it['lesson']}"
                  + (f"  ({','.join(it['tags'])})" if it.get("tags") else ""))
        return 0
    for it in read_all():
        print(f"{it['id']} — {it['lesson']}"
              + (f"  [{','.join(it.get('tags', []))}]" if it.get("tags") else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
