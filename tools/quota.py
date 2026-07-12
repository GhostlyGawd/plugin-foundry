#!/usr/bin/env python3
"""quota.py — quota governor v2 (MASTER P0.6, ADR-028). Closes G6.

budget.py (ADR-008) governs DOLLARS — correct for API billing. A subscription
has no readable meter, only rate-limit windows; the honest signal until the API
switch is run counts (ADR-031 ruling on MASTER §12 Q3). This governor estimates
weekly-window pressure from the ledger and sheds agents by tier:

    pressure = runs_in_last_168h / QUOTA_WEEKLY_RUNS
    pressure ≥ QUOTA_SHED_LOW  (default 0.60) → shed quota_tier 'low'
    pressure ≥ QUOTA_SHED_HIGH (default 0.85) → shed 'high' too
    'product' NEVER sheds on pressure — the factory ships before it talks.
    pressure ≥ 1.0 → the kill switch: even product pauses TO THE DESK
    (a d-item the operator resolves; raise QUOTA_WEEKLY_RUNS or wait).

The dollar path stays: LOOP_MONTHLY_BUDGET_USD exhausted skips every tier
(ADR-008 is absolute). Decisions are ledgered in state/BUDGET.jsonl as
{"kind": "quota_shed"|"quota_halt"} lines; `report` shows them. Runs are
counted from ledger lines that represent one Claude session: legacy loop
entries (cost_usd/usage present) and {"kind": "quota_run"} marks.

  quota.py check --agent <id>   exit 0 go · 1 skip (fail-closed on unknowns)
  quota.py record --agent <id>  append a run mark (call once per session)
  quota.py report               pressure, tier verdicts, recent decisions

FOUNDRY_NOW (ISO) injects the clock for tests.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import load_agents  # noqa: E402

WINDOW_H = 168  # one week — the subscription's coarse limit window


def _now():
    env = os.environ.get("FOUNDRY_NOW")
    if env:
        return datetime.fromisoformat(env.replace("Z", "+00:00"))
    return datetime.now(timezone.utc)


def _ledger(root):
    return os.path.join(root, "state", "BUDGET.jsonl")


def _entries(root):
    p = _ledger(root)
    if not os.path.exists(p):
        return []
    out = []
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def _parse_ts(e):
    try:
        return datetime.fromisoformat(str(e.get("ts", "")).replace("Z", "+00:00"))
    except ValueError:
        return None


def _is_run(e):
    if e.get("kind") == "quota_run":
        return True
    if e.get("kind"):  # quota_shed / quota_halt marks are not runs
        return False
    return "cost_usd" in e or "usage" in e  # legacy loop ledger lines


def runs_in_window(root, now=None):
    now = now or _now()
    cut = now - timedelta(hours=WINDOW_H)
    n = 0
    for e in _entries(root):
        ts = _parse_ts(e)
        if ts and ts >= cut and _is_run(e):
            n += int(e.get("runs", 1) or 1)
    return n


def pressure(root, now=None):
    cap = float(os.environ.get("QUOTA_WEEKLY_RUNS", "40") or 40)
    if cap <= 0:
        return 0.0, 0, cap
    runs = runs_in_window(root, now)
    return runs / cap, runs, cap


def month_dollars(root, now=None):
    prefix = (now or _now()).strftime("%Y-%m")
    return sum(e.get("cost_usd") or 0 for e in _entries(root)
               if str(e.get("ts", "")).startswith(prefix))


def _append(root, rec):
    rec = {"ts": _now().strftime("%Y-%m-%dT%H:%M:%SZ"), **rec}
    with open(_ledger(root), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def cmd_record(agent, root):
    _append(root, {"kind": "quota_run", "agent": agent})
    print(f"quota: run recorded for {agent}")
    return 0


def cmd_check(agent_id, root):
    # Dollar path first — ADR-008 is absolute when a dollar cap is set.
    cap_usd = os.environ.get("LOOP_MONTHLY_BUDGET_USD", "").strip()
    if cap_usd:
        spent = month_dollars(root)
        if spent >= float(cap_usd):
            _append(root, {"kind": "quota_halt", "agent": agent_id,
                           "why": f"dollar cap ${cap_usd} spent (${spent:.2f})"})
            print(f"quota: HALT {agent_id} — ${spent:.2f} of ${cap_usd} this month (ADR-008)")
            return 1

    errors = []
    agents = {a["id"]: a for a in load_agents(errors, root)}
    agent = agents.get(agent_id)
    if errors or agent is None:
        print(f"quota: SKIP {agent_id} — unknown agent or unlawful registry (fail closed)")
        return 1
    tier = agent["quota_tier"]

    pr, runs, cap = pressure(root)
    shed_low = float(os.environ.get("QUOTA_SHED_LOW", "0.60") or 0.60)
    shed_high = float(os.environ.get("QUOTA_SHED_HIGH", "0.85") or 0.85)

    if pr >= 1.0:
        if tier == "product":
            # The kill switch: product pauses TO THE DESK, never silently.
            import desk
            iid, fresh = desk.add(
                "approve",
                "quota kill switch: product loop past the weekly window",
                f"pressure {pr:.2f} ({runs}/{int(cap)} runs, {WINDOW_H}h window). "
                f"Approve by raising QUOTA_WEEKLY_RUNS (Actions variable) or "
                f"waiting for the window to roll; the loop stays paused until "
                f"pressure < 1.0.",
                agent_id, path=os.path.join(root, "state", "DESK.jsonl"))
            _append(root, {"kind": "quota_halt", "agent": agent_id, "tier": tier,
                           "pressure": round(pr, 3), "desk": iid})
            print(f"quota: HALT {agent_id} (product) — pressure {pr:.2f} ≥ 1.0; "
                  f"desk item {iid} {'queued' if fresh else 'already open'}")
            return 1
        _append(root, {"kind": "quota_shed", "agent": agent_id, "tier": tier,
                       "pressure": round(pr, 3)})
        print(f"quota: SHED {agent_id} ({tier}) — pressure {pr:.2f} ≥ 1.0")
        return 1
    if tier == "low" and pr >= shed_low:
        _append(root, {"kind": "quota_shed", "agent": agent_id, "tier": tier,
                       "pressure": round(pr, 3)})
        print(f"quota: SHED {agent_id} (low) — pressure {pr:.2f} ≥ {shed_low}")
        return 1
    if tier == "high" and pr >= shed_high:
        _append(root, {"kind": "quota_shed", "agent": agent_id, "tier": tier,
                       "pressure": round(pr, 3)})
        print(f"quota: SHED {agent_id} (high) — pressure {pr:.2f} ≥ {shed_high}")
        return 1
    print(f"quota: GO {agent_id} ({tier}) — pressure {pr:.2f} "
          f"({runs}/{int(cap)} runs/{WINDOW_H}h)")
    return 0


def cmd_report(root):
    pr, runs, cap = pressure(root)
    shed_low = float(os.environ.get("QUOTA_SHED_LOW", "0.60") or 0.60)
    shed_high = float(os.environ.get("QUOTA_SHED_HIGH", "0.85") or 0.85)
    print(f"quota: pressure {pr:.2f} — {runs} runs in {WINDOW_H}h of cap {int(cap)}")
    print(f"quota: tiers — product {'PAUSED (desk)' if pr >= 1.0 else 'go'} · "
          f"high {'shed' if pr >= shed_high else 'go'} · "
          f"low {'shed' if pr >= shed_low else 'go'}")
    spent = month_dollars(root)
    cap_usd = os.environ.get("LOOP_MONTHLY_BUDGET_USD", "").strip()
    print(f"quota: dollars — ${spent:.2f} month-to-date"
          + (f" of ${cap_usd} cap" if cap_usd else " (no dollar cap set — subscription mode)"))
    decisions = [e for e in _entries(root) if e.get("kind") in ("quota_shed", "quota_halt")]
    for e in decisions[-10:]:
        print(f"quota:   {e.get('ts')} {e.get('kind')} {e.get('agent')} "
              f"(tier {e.get('tier', '?')}, pressure {e.get('pressure', '?')})")
    if not decisions:
        print("quota:   no shed/halt decisions on the ledger")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="quota.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--agent", required=True)
    c.add_argument("--root", default=".")
    r = sub.add_parser("record")
    r.add_argument("--agent", required=True)
    r.add_argument("--root", default=".")
    rep = sub.add_parser("report")
    rep.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    if args.cmd == "check":
        return cmd_check(args.agent, args.root)
    if args.cmd == "record":
        return cmd_record(args.agent, args.root)
    return cmd_report(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
