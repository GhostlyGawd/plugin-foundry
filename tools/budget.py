#!/usr/bin/env python3
"""budget.py — the spend ledger and governor (ADR-008).

  budget.py add <claude-json-output-file>   append cost/usage to state/BUDGET.jsonl
  budget.py check                            exit 1 if month-to-date >= LOOP_MONTHLY_BUDGET_USD
  budget.py report                           month-to-date + cost-per-shipped summary

Unparseable fields record null — the ledger never guesses (GROWTH.md spirit)."""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "state" / "BUDGET.jsonl"


def entries():
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text().splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def month_to_date():
    prefix = datetime.now(timezone.utc).strftime("%Y-%m")
    return sum(e.get("cost_usd") or 0 for e in entries() if str(e.get("ts", "")).startswith(prefix))


def cmd_add(path):
    cost = usage = None
    try:
        data = json.loads(Path(path).read_text())
        if isinstance(data, list):  # stream-json fallback: take the result event
            data = next((d for d in reversed(data) if isinstance(d, dict) and "total_cost_usd" in d), {})
        cost = data.get("total_cost_usd")
        usage = data.get("usage")
    except Exception:  # noqa: BLE001 — null over guess
        pass
    with LEDGER.open("a") as fh:
        fh.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(),
                             "cost_usd": cost, "usage": usage}) + "\n")
    print(f"budget: logged cost_usd={cost}")


def cmd_check():
    cap = os.environ.get("LOOP_MONTHLY_BUDGET_USD", "").strip()
    if not cap:
        print("budget: no LOOP_MONTHLY_BUDGET_USD set — governor idle")
        return 0
    spent = month_to_date()
    if spent >= float(cap):
        print(f"budget: GOVERNOR HALT — ${spent:.2f} of ${cap} spent this month; shift skipped")
        return 1
    print(f"budget: ${spent:.2f} of ${cap} this month — clear to run")
    return 0


def cmd_report():
    spent = month_to_date()
    shipped = len(list((ROOT / ".claude-plugin").glob("marketplace.json")))
    try:
        mp = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        shipped = len(mp.get("plugins", []))
    except Exception:  # noqa: BLE001
        pass
    per = f"${spent / shipped:.2f}" if shipped else "n/a"
    print(f"budget: month-to-date ${spent:.2f} · shipped plugins {shipped} · naive cost/ship {per}")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    sys.exit({"add": lambda: cmd_add(sys.argv[2]), "check": cmd_check, "report": cmd_report}[cmd]())
