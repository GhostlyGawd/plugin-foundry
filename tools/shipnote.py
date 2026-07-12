#!/usr/bin/env python3
"""shipnote.py — the weekly digest, written from the journal and records: shipped,
moved, killed, queued, fuel. Summarizes only what the repo substantiates
(GROWTH.md). Prints markdown; shipnote.yml posts it as an issue. Usage:
shipnote.py [days]"""
import subprocess
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from lib import parse_front_matter  # one parser, one truth (v13 C12)


def fm(text):
    return parse_front_matter(text or "")[0]


def social(days=7):
    """P4.2 (ADR-031): the short social-post variant. One post, substantiated,
    from the same journal+records the weekly note reads. Posts weekly regardless
    of build volume (the build-in-public content engine)."""
    since = datetime.now(timezone.utc) - timedelta(days=days)
    mp = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    shipped = []
    for rec in sorted((ROOT / "foundry" / "records").glob("*.md")):
        meta = fm(rec.read_text())
        if meta.get("updated", "") < since.strftime("%Y-%m-%d"):
            continue
        if meta.get("stage") == "published" and meta.get("kind", "plugin") == "plugin":
            shipped.append(f"{meta.get('title')} v{meta.get('version')}")
    q = {}
    dj = ROOT / "site" / "data.json"
    if dj.exists():
        q = json.loads(dj.read_text()).get("quality", {})
    week = datetime.now(timezone.utc).strftime("%G-W%V")
    if shipped:
        head = f"This week the foundry shipped: {', '.join(shipped[:3])}" + (
            f" (+{len(shipped) - 3} more)" if len(shipped) > 3 else "") + "."
    else:
        head = "Quiet build week at the foundry — the line kept its bar."
    tail = (f"{q.get('plugins_shipped', '?')} plugins · "
            f"{q.get('qa_first_try_pct', '?')}% first-try QA · "
            f"{q.get('bounces_total', '?')} bounced-and-fixed in public. "
            f"An AI-run software company in a repo. #ClaudeCode")
    print(f"[{week}] {head} {tail}")
    return 0


def main(days=7):
    if "--social" in sys.argv:
        return social(days)
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
    moved = "\n".join(moves[-12:]) if moves else "_a quiet week_"
    if len(moves) > 12:
        moved += f"\n- …and {len(moves) - 12} earlier move(s) this week — unabridged in state/JOURNAL.md"
    print("\n## Moved on the line\n" + moved)
    if killed:
        print("\n## Killed or shelved (the honest column)\n" + "\n".join(killed))
    # Mailbag — question-labeled issues, answered in-thread by the growth shift
    import shutil as _sh
    if _sh.which("gh"):
        q = subprocess.run(["gh", "issue", "list", "--label", "question", "--state", "open",
                            "--json", "number,title,url"], capture_output=True, text=True, cwd=ROOT)
        try:
            qs = json.loads(q.stdout) if q.returncode == 0 else []
        except Exception:
            qs = []
        if qs:
            print("\n## Mailbag")
            for it in qs:
                print(f"- Q: {it['title']} ([#{it['number']}]({it['url']})) — answered in-thread by the shift, or marked *on the desk*")
            print("_Answers are drafted from repo evidence only (charter/GROWTH.md); unanswered questions stay listed until they are not._")
    else:
        print("\nmailbag: gh absent here — section skipped, shipnote still stands", file=sys.stderr)
    print(fuel)
    print("\n_Written by the loop from its own journal — nothing here is retouched._")
    return 0


if __name__ == "__main__":
    _days = next((int(a) for a in sys.argv[1:] if a.isdigit()), 7)
    sys.exit(main(_days))
