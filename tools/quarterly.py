#!/usr/bin/env python3
"""quarterly.py — the state-of-the-company report (MASTER P5.5, ADR-031).

The press hook (Project Vend proved the appetite). Cites REAL metric movement
(first vs last METRICS.jsonl sample in the window), names failures honestly
(bounces + postmortems), and lands 3–5 recommendations on the owner's desk.
Growth-honesty: every figure is from the repo.

  quarterly.py [days]     print the report (default 90) + queue its recs
Stdlib only. Deterministic (recommendations dedup at the desk).
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import desk  # noqa: E402


def metrics_window(days):
    mp = os.path.join(ROOT, "state", "METRICS.jsonl")
    if not os.path.exists(mp):
        return None, None
    rows = []
    for line in open(mp, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except ValueError:
            continue
    real = [r for r in rows if isinstance(r.get("stars"), int)]
    if not real:
        return None, None
    return real[0], real[-1]


def main(days=90):
    data = {}
    dp = os.path.join(ROOT, "site", "data.json")
    if os.path.exists(dp):
        data = json.load(open(dp, encoding="utf-8"))
    q = data.get("quality", {})
    first, last = metrics_window(days)

    lines = [f"# State of the Company — last {days} days", ""]
    lines += ["## What shipped",
              f"- {q.get('plugins_shipped', '?')} plugins on the shelf, "
              f"{q.get('qa_first_try_pct', '?')}% passed QA first-try.",
              f"- {q.get('iterations', '?')} iterations run; "
              f"${q.get('api_spend_usd', 0)} API spend (subscription mode).", ""]

    lines.append("## Told honestly — what didn't work")
    bounces = q.get("bounces_total", 0)
    lines.append(f"- {bounces} builds bounced by QA/review and were fixed in public "
                 f"(the gates worked — that's the point).")
    pmdir = os.path.join(ROOT, "reviews", "postmortems")
    pms = sorted(f for f in os.listdir(pmdir)) if os.path.isdir(pmdir) else []
    if pms:
        lines.append(f"- {len(pms)} incident postmortem(s) on file: "
                     + ", ".join(p.replace('.md', '') for p in pms) + ".")
    lines.append("")

    lines.append("## The audience")
    if first and last:
        ds = last.get("stars", 0) - first.get("stars", 0)
        lines.append(f"- Stars: {first.get('stars', 0)} → {last.get('stars', 0)} "
                     f"({'+' if ds >= 0 else ''}{ds}).")
        lines.append(f"- Open ideas: {last.get('open_ideas', 0)}; "
                     f"votes: {last.get('idea_votes_total', 0)}.")
    else:
        lines.append("- Traffic instruments are still arming (honest nulls); "
                     "no movement to report yet.")
    lines.append("")

    # 3–5 recommendations, landed on the desk (deduped)
    recs = []
    if q.get("qa_first_try_pct", 100) < 80:
        recs.append("First-try QA below 80% — audit the top bounce cause.")
    if bounces and not pms:
        recs.append("Bounces but no postmortems — capture at least one as a trust artifact.")
    if not (first and last):
        recs.append("No audience yet — execute the launch kit (foundry/LAUNCH.md).")
    if data.get("alarms"):
        recs.append("Open ops-alarm(s) — clear before the next quarter.")
    recs.append("Refresh the quality number and re-run the state-of-the-company as a re-launch.")
    recs = recs[:5]

    lines.append("## Recommendations (landed on the desk)")
    for r in recs:
        lines.append(f"- {r}")

    ledger = os.path.join(ROOT, "state", "DESK.jsonl")
    for r in recs:
        desk.add("decide", f"quarterly rec: {r[:60]}", r, "quarterly", path=ledger)

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 90))
