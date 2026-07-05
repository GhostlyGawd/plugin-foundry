#!/usr/bin/env python3
"""shipnote.py — the weekly digest, written from the journal and records: shipped,
moved, killed, queued, fuel. Summarizes only what the repo substantiates
(GROWTH.md). Prints markdown; shipnote.yml posts it as an issue. Usage:
shipnote.py [days]"""
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fm(text):
    parts = text.split("---", 2)
    meta = {}
    if len(parts) < 3:
        return meta
    for line in parts[1].strip().splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, _, v = line.partition(":")
            meta[k.strip()] = v.split(" #")[0].strip()
    return meta


def main(days=7):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    journal = (ROOT / "state" / "JOURNAL.md").read_text()
    moves = []
    for it, role, ts, body in re.findall(
            r"^## (i\d+) — ([\w-]+) — ([0-9TZ:\-\.]+)\n(.*?)(?=^## i|\Z)", journal, re.M | re.S):
        try:
            when = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            continue
        if when < since:
            continue
        line = re.search(r"-\s*line:\s*(.+)", body)
        if line and "n/a" not in line.group(1):
            moves.append(f"- {it} ({role}): {line.group(1).strip()}")

    shipped, killed = [], []
    mp = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    for rec in sorted((ROOT / "foundry" / "records").glob("*.md")):
        meta = fm(rec.read_text())
        if meta.get("updated", "") < since.strftime("%Y-%m-%d"):
            continue
        if meta.get("stage") == "published" and meta.get("kind", "plugin") == "plugin":
            shipped.append(f"- **{meta.get('title')}** v{meta.get('version')} — "
                           f"`/plugin install {meta.get('name')}@{mp.get('name', 'foundry')}`")
        if meta.get("stage") in ("deprecated", "shelved"):
            killed.append(f"- {meta.get('title')} → {meta.get('stage')} (reasons on its provenance page)")

    fuel = ""
    try:
        prefix = datetime.now(timezone.utc).strftime("%Y-%m")
        spend = sum((json.loads(l).get("cost_usd") or 0)
                    for l in (ROOT / "state" / "BUDGET.jsonl").read_text().splitlines()
                    if l.strip() and prefix in l)
        fuel = f"\n## Fuel\nMonth-to-date spend: ${spend:.2f} (ledger: state/BUDGET.jsonl)."
    except Exception:  # noqa: BLE001
        pass

    week = datetime.now(timezone.utc).strftime("%G-W%V")
    print(f"# Shipnote {week}\n")
    print("## Shipped\n" + ("\n".join(shipped) if shipped else "_nothing this week — see Moved_"))
    print("\n## Moved on the line\n" + ("\n".join(moves[-12:]) if moves else "_a quiet week_"))
    if killed:
        print("\n## Killed or shelved (the honest column)\n" + "\n".join(killed))
    print(fuel)
    print("\n_Written by the loop from its own journal — nothing here is retouched._")
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 7))
