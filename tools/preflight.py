#!/usr/bin/env python3
"""preflight.py — go-live readiness, in one read-only pass (ADR-016 #13;
--issue + tag-drift v11 #10/#11, ADR-019).
Prints OK / TODO(operator) per check and a distilled click-list for the human.
`--issue` renders the same facts as a GitHub-checkbox markdown body and, when
the `gh` CLI is available, opens or updates a single `ops: go-live checklist`
issue (label ops-golive) — fail-soft: without gh it just prints the markdown.
Advisory: always exits 0. Never reads or prints secret VALUES — names only."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OK, TODO = "  OK  ", "  TODO(operator)"

CLICKS = [
    "Settings → Pages → Source: GitHub Actions (OPERATIONS §2)",
    "Settings → Secrets → Actions: project-scoped OPENAI_API_KEY (§3; Codex workflows only)",
    "Settings → Variables: LOOP_MONTHLY_BUDGET_USD = your cap (§3, §7)",
    "Optional: GOATCOUNTER_TOKEN secret + goatcounter_site config (§6)",
    "Actions tab → run \"Run shift\" once; remove STOP in a reviewed PR only after the proposed shift PR is green (§3, §5)",
    "Push local release tags if any (tag pushes are branch-scoped from sessions): git push origin --tags",
]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)


def unpushed_tags():
    """Local release tags absent from the remote (v11 #11) — the silent way
    releases never get cut. Returns (tags, note); tags is None on network
    trouble so the check reports itself as skipped, never as green."""
    local = set(run(["git", "tag", "--list", "*-v*"]).stdout.split())
    r = run(["git", "ls-remote", "--tags", "origin"])
    if r.returncode != 0:
        return None, "could not reach the remote — drift check skipped, not green"
    remote = {line.rsplit("refs/tags/", 1)[1].removesuffix("^{}")
              for line in r.stdout.splitlines() if "refs/tags/" in line}
    return sorted(local - remote), ""


def collect():
    """Every check as (ok: bool, text: str)."""
    checks = []
    cfg = json.loads((ROOT / "foundry" / "site-config.json").read_text())
    checks.append((bool(cfg.get("repo")), f"site-config repo: {cfg.get('repo') or 'unset'}"))
    checks.append((bool(cfg.get("pages_url")), f"site-config pages_url: {cfg.get('pages_url') or 'unset'}"))
    checks.append((bool(cfg.get("goatcounter_site")),
                   "goatcounter_site (optional pageviews — OPERATIONS §6): "
                   + (cfg.get("goatcounter_site") or "unset; metrics.py records null, never a guess")))
    checks.append((bool(cfg.get("monthly_budget_usd")),
                   "monthly_budget_usd (fuel-gauge cap — mirror LOOP_MONTHLY_BUDGET_USD): "
                   + str(cfg.get("monthly_budget_usd") or "unset; gauge renders spend-only")))

    wf = ROOT / ".github" / "workflows"
    for name in ("run-shift.yml", "shipnote.yml", "record-demos.yml"):
        checks.append(((wf / name).exists(), f"workflow present: {name}"))

    for tool in ("validate", "build"):
        r = run([sys.executable, str(ROOT / "tools" / f"{tool}.py")])
        checks.append((r.returncode == 0, f"tools/{tool}.py: "
                       + (r.stdout.strip().splitlines()[-1] if r.stdout else "no output")))

    funding_path = ROOT / ".github" / "FUNDING.yml"
    funding = funding_path.read_text() if funding_path.exists() else ""
    armed = any(l.strip().startswith("github:") for l in funding.splitlines()
                if not l.strip().startswith("#"))
    checks.append((armed, "FUNDING.yml sponsor handle (optional — OPERATIONS §8): "
                   + ("armed" if armed else "commented template")))

    tags, note = unpushed_tags()
    if tags is None:
        checks.append((False, f"release-tag drift: {note}"))
    elif tags:
        shown = ", ".join(tags[:5]) + (" …" if len(tags) > 5 else "")
        checks.append((False, f"release-tag drift: {len(tags)} local tag(s) NOT on the remote "
                              f"({shown}) — releases never cut until `git push origin --tags`"))
    else:
        checks.append((True, "release-tag drift: none — every local release tag is on the remote"))
    return checks


def render_terminal(checks):
    print("PREFLIGHT — Nightshift Foundry go-live readiness\n")
    for ok, text in checks:
        print(f"[{(OK if ok else TODO).strip():^16}] {text}")
    print("\nSecrets / repo settings this script CANNOT verify — the 15-minute click-list:")
    for i, click in enumerate(CLICKS, 1):
        print(f"  {i}. {click}")
    print("After step 5, Gate A's 14-day clock is running (ROADMAP.md).")


def render_markdown(checks):
    lines = ["# ops: go-live checklist", "",
             "Auto-rendered by `tools/preflight.py --issue` — machine-verifiable "
             "state below is checked for you; the click-list is yours.", "",
             "## Verified by the script"]
    lines += [f"- [{'x' if ok else ' '}] {text}" for ok, text in checks]
    lines += ["", "## The 15-minute click-list (only you can tick these)"]
    lines += [f"- [ ] {c}" for c in CLICKS]
    lines += ["", "_After the first manual shift, Gate A's 14-day clock is running (ROADMAP.md)._"]
    return "\n".join(lines)


def sync_issue(body):
    """Open or update the single ops-golive issue. Fail-soft everywhere."""
    if not shutil.which("gh"):
        print("\n(gh CLI not available here — paste the markdown above into an issue yourself)")
        return
    r = run(["gh", "issue", "list", "--label", "ops-golive", "--state", "open",
             "--json", "number", "--jq", ".[0].number"])
    num = r.stdout.strip() if r.returncode == 0 else ""
    if num:
        r = run(["gh", "issue", "edit", num, "--body", body])
        print(f"\nupdated issue #{num}" if r.returncode == 0
              else f"\ncould not update issue #{num}: {r.stderr.strip()[:120]}")
    else:
        r = run(["gh", "issue", "create", "--title", "ops: go-live checklist",
                 "--label", "ops-golive", "--body", body])
        print(f"\nopened {r.stdout.strip()}" if r.returncode == 0
              else f"\ncould not open the issue: {r.stderr.strip()[:120]}")


def main():
    checks = collect()
    if "--issue" in sys.argv:
        body = render_markdown(checks)
        print(body)
        sync_issue(body)
    else:
        render_terminal(checks)
    return 0


if __name__ == "__main__":
    sys.exit(main())
