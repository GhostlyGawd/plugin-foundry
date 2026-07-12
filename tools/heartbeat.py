#!/usr/bin/env python3
"""heartbeat.py — agent liveness (MASTER P0.9, ADR-026). Closes G5: a silently
dead agent must not read as health.

`beat <id>` stamps foundry/agents/heartbeats.json; the shared agent wrapper
calls it on every run. `check` compares each ACTIVE registry agent's last beat
against its manifest heartbeat.interval_hours (plus grace) and reports
staleness; `--alarm` raises an ops-alarm via tools/alarm.py. Agents with
status "dormant" (e.g. while the root STOP file stands) are exempt — a paused
factory is quiet, not sick. FOUNDRY_NOW (ISO, tests) overrides the clock.

Exit codes: beat 0/1 · check 0 healthy, 2 stale (scriptable; ops-guard alarms
instead of failing).
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import load_agents  # noqa: E402

GRACE = 1.5  # intervals of slack before an agent counts as stale


def _now():
    env = os.environ.get("FOUNDRY_NOW")
    if env:
        return datetime.fromisoformat(env.replace("Z", "+00:00"))
    return datetime.now(timezone.utc)


def _path(root):
    return os.path.join(root, "foundry", "agents", "heartbeats.json")


def _read(root):
    p = _path(root)
    if not os.path.exists(p):
        return {}
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def beat(agent_id, note, root):
    errors = []
    ids = {a["id"] for a in load_agents(errors, root)}
    if errors or agent_id not in ids:
        print(f"heartbeat: unknown agent '{agent_id}' — no manifest, no beat")
        return 1
    hb = _read(root)
    hb[agent_id] = {"ts": _now().strftime("%Y-%m-%dT%H:%M:%SZ")}
    if note:
        hb[agent_id]["note"] = note
    with open(_path(root), "w", encoding="utf-8") as f:
        json.dump(hb, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"heartbeat: {agent_id} beat at {hb[agent_id]['ts']}")
    return 0


def check(alarm, root):
    errors = []
    agents = load_agents(errors, root)
    if errors:
        for e in errors:
            print(f"heartbeat: ✗ {e}")
        return 2
    hb = _read(root)
    now = _now()
    stale = []
    for a in agents:
        if a.get("status", "active") != "active":
            continue
        interval = a["heartbeat"]["interval_hours"]
        rec = hb.get(a["id"])
        if not rec:
            stale.append((a["id"], "no heartbeat ever recorded"))
            continue
        try:
            ts = datetime.fromisoformat(rec["ts"].replace("Z", "+00:00"))
        except (KeyError, ValueError):
            stale.append((a["id"], "unreadable heartbeat timestamp"))
            continue
        age_h = (now - ts).total_seconds() / 3600
        if age_h > interval * GRACE:
            stale.append((a["id"], f"last beat {age_h:.1f}h ago "
                                   f"(interval {interval}h × {GRACE} grace)"))
    if not stale:
        print(f"heartbeat: OK — {sum(1 for a in agents if a.get('status', 'active') == 'active')} active agent(s) fresh, "
              f"{sum(1 for a in agents if a.get('status', 'active') != 'active')} dormant exempt")
        return 0
    for aid, why in stale:
        print(f"heartbeat: STALE {aid} — {why}")
        if alarm:
            subprocess.run(
                [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "alarm.py"),
                 f"ops-alarm: agent '{aid}' heartbeat stale",
                 f"{why}. A silently dead agent reads as health (G5); "
                 f"check its workflow and manifest (foundry/agents/{aid}/)."],
                check=False)
    return 2


def main(argv=None):
    ap = argparse.ArgumentParser(prog="heartbeat.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("beat")
    b.add_argument("agent")
    b.add_argument("--note", default="")
    b.add_argument("--root", default=".")
    c = sub.add_parser("check")
    c.add_argument("--alarm", action="store_true")
    c.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    if args.cmd == "beat":
        return beat(args.agent, args.note, args.root)
    return check(args.alarm, args.root)


if __name__ == "__main__":
    raise SystemExit(main())
