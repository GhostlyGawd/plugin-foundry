#!/usr/bin/env python3
"""briefing.py — the per-shift operator briefing (MASTER P1.1, ADR-031).

Every shift, a <30-second read: what just shipped, where the quality number
stands, and the ranked decisions waiting at the desk. Assembled from repo data
(growth-honesty) — a live agent may narrate it, but the substance is real.
Posts to the pinned briefing issue (briefing.yml) or prints markdown.

  briefing.py            print the current briefing
Stdlib only. Deterministic.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import desk  # noqa: E402


def latest_journal_entry():
    jp = os.path.join(ROOT, "state", "JOURNAL.md")
    if not os.path.exists(jp):
        return None
    entries = re.findall(r"^## (i\d+ — [\w-]+ — [0-9TZ:\-.]+)\n(.*?)(?=^## i|\Z)",
                         open(jp, encoding="utf-8").read(), re.M | re.S)
    if not entries:
        return None
    head, body = entries[-1]
    did = re.search(r"-\s*did:\s*(.+)", body)
    return head, (did.group(1).strip()[:200] if did else "")


def main():
    data = {}
    dp = os.path.join(ROOT, "site", "data.json")
    if os.path.exists(dp):
        data = json.load(open(dp, encoding="utf-8"))
    q = data.get("quality", {})
    lines = ["# Shift briefing", ""]

    entry = latest_journal_entry()
    if entry:
        lines += [f"**Last move:** {entry[0]}", f"> {entry[1]}", ""]

    lines += [
        "**The number:** "
        f"{q.get('plugins_shipped', '?')} shipped · "
        f"{q.get('qa_first_try_pct', '?')}% first-try QA · "
        f"{q.get('bounces_total', '?')} bounced · "
        f"{q.get('iterations', '?')} iterations · "
        f"${q.get('api_spend_usd', 0)} API",
        "",
    ]

    ranked = desk.rank(path=os.path.join(ROOT, "state", "DESK.jsonl"))
    if ranked:
        lines.append(f"**The desk — {len(ranked)} open, top {min(3, len(ranked))}:**")
        for score, it in ranked[:3]:
            lines.append(f"- `{it['id']}` ({it.get('kind')}) {it.get('title')}")
        lines.append("Resolve: `python3 tools/desk.py resolve <id> approved|rejected`")
    else:
        lines.append("**The desk is clear.**")

    alarms = data.get("alarms", [])
    if alarms:
        lines += ["", f"⚠️ **{len(alarms)} open ops-alarm(s)** — the window is amber."]

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
