#!/usr/bin/env python3
"""preflight.py — go-live readiness, in one read-only pass (ADR-016 #13).
Prints OK / TODO(operator) per check and a distilled click-list for the human.
Advisory: always exits 0. Never reads or prints secret VALUES — names only."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OK, TODO = "  OK  ", "  TODO(operator)"


def line(status, text):
    print(f"[{status.strip():^16}] {text}")


def main():
    print("PREFLIGHT — Nightshift Foundry go-live readiness\n")

    cfg = json.loads((ROOT / "foundry" / "site-config.json").read_text())
    line(OK if cfg.get("repo") else TODO, f"site-config repo: {cfg.get('repo') or 'unset'}")
    line(OK if cfg.get("pages_url") else TODO, f"site-config pages_url: {cfg.get('pages_url') or 'unset'}")
    line(OK if cfg.get("goatcounter_site") else TODO,
         "goatcounter_site (optional pageviews — OPERATIONS §6): "
         + (cfg.get("goatcounter_site") or "unset; metrics.py records null, never a guess"))
    line(OK if cfg.get("monthly_budget_usd") else TODO,
         "monthly_budget_usd (fuel-gauge cap — mirror LOOP_MONTHLY_BUDGET_USD): "
         + str(cfg.get("monthly_budget_usd") or "unset; gauge renders spend-only"))

    wf = ROOT / ".github" / "workflows"
    expected = ["run-shift.yml", "shipnote.yml", "record-demos.yml"]
    for name in expected:
        line(OK if (wf / name).exists() else TODO, f"workflow present: {name}")

    for tool in ("validate", "build"):
        r = subprocess.run([sys.executable, str(ROOT / "tools" / f"{tool}.py")],
                           capture_output=True, text=True)
        line(OK if r.returncode == 0 else TODO, f"tools/{tool}.py: "
             + (r.stdout.strip().splitlines()[-1] if r.stdout else "no output"))

    funding = (ROOT / ".github" / "FUNDING.yml").read_text() if (ROOT / ".github" / "FUNDING.yml").exists() else ""
    armed = any(l.strip().startswith("github:") for l in funding.splitlines() if not l.strip().startswith("#"))
    line(OK if armed else TODO, "FUNDING.yml sponsor handle (optional — OPERATIONS §8): "
         + ("armed" if armed else "commented template"))

    print("""
Secrets / repo settings this script CANNOT verify — the 15-minute click-list:
  1. Settings → Pages → Source: GitHub Actions                      (OPERATIONS §2)
  2. Settings → Secrets → Actions: ANTHROPIC_API_KEY                (§3)
     (or CLAUDE_CODE_OAUTH_TOKEN; record-demos.yml uses either)
  3. Settings → Variables: LOOP_MONTHLY_BUDGET_USD = your cap       (§3, §7)
  4. Optional: GOATCOUNTER_TOKEN secret + goatcounter_site config   (§6)
  5. Actions tab → run "Run shift" once by hand — first CI shift
     arms METRICS.jsonl, the ledger, and every experiment baseline  (§3, §5)
  6. Push local release tags if any (tag pushes are branch-scoped
     from sessions): git push origin --tags
After step 5, Gate A's 14-day clock is running (ROADMAP.md).""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
