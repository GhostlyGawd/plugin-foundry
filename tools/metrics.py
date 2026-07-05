#!/usr/bin/env python3
"""metrics.py — the growth instruments. Runs at the top of every shift.

Appends one honest snapshot to state/METRICS.jsonl and writes foundry/votes.json
(open `idea` issues with their 👍 counts). Real signals only; anything unreachable
records null, never a guess (charter/GROWTH.md). Commits its own change so loop
iterations can read fresh numbers. Stdlib + gh CLI; degrades to a no-op locally."""
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "state" / "METRICS.jsonl"
VOTES = ROOT / "foundry" / "votes.json"


def gh_api(path):
    try:
        out = subprocess.run(["gh", "api", path], capture_output=True, text=True, check=True).stdout
        return json.loads(out)
    except (FileNotFoundError, subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def goatcounter(cfg):
    """Optional privacy-respecting pageviews. Operator wires site + token per
    GoatCounter's current API docs (OPERATIONS.md § 6); any failure -> null."""
    site = cfg.get("goatcounter_site") or ""
    token = os.environ.get("GOATCOUNTER_TOKEN", "")
    if not site or not token:
        return None
    try:
        req = urllib.request.Request(
            f"https://{site}.goatcounter.com/api/v0/stats/total",
            headers={"Authorization": f"Bearer {token}"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read()).get("total")
    except Exception:  # noqa: BLE001 — instrument absence is not an error
        return None


def main():
    cfg = json.loads((ROOT / "foundry" / "site-config.json").read_text())
    repo = os.environ.get("GITHUB_REPOSITORY") or cfg.get("repo") or ""
    if not repo:
        print("metrics: no repo configured; nothing to measure")
        return 0

    info = gh_api(f"repos/{repo}") or {}
    views = gh_api(f"repos/{repo}/traffic/views") or {}
    clones = gh_api(f"repos/{repo}/traffic/clones") or {}
    ideas = gh_api(f"repos/{repo}/issues?labels=idea&state=open&per_page=100") or []
    commissions = gh_api(f"repos/{repo}/issues?labels=commission&state=open&per_page=100") or []

    reports_raw = gh_api(f"repos/{repo}/issues?labels=field-report&state=all&per_page=100") or []
    reports = {}
    for issue in reports_raw:
        if "pull_request" in issue:
            continue
        mtch = None
        for line in (issue.get("body") or "").splitlines():
            if line.strip() and not line.startswith("#"):
                mtch = line.strip().split()[0].strip("`").lower()
                break
        key = mtch or "unattributed"
        reports.setdefault(key, []).append(
            {"title": issue.get("title", ""), "url": issue.get("html_url", ""),
             "author": (issue.get("user") or {}).get("login", "")})
    (ROOT / "foundry" / "reports.json").write_text(json.dumps(reports, indent=1))

    alarms_raw = gh_api(f"repos/{repo}/issues?labels=ops-alarm&state=open&per_page=50") or []
    alarms = [{"title": i.get("title", ""), "url": i.get("html_url", "")}
              for i in alarms_raw if "pull_request" not in i]
    (ROOT / "foundry" / "alarms.json").write_text(json.dumps(alarms, indent=1))

    votes = {}
    for issue in ideas:
        if "pull_request" in issue:
            continue
        votes[str(issue["number"])] = {
            "title": issue.get("title", ""),
            "votes": (issue.get("reactions") or {}).get("+1", 0),
            "url": issue.get("html_url", ""),
        }
    VOTES.write_text(json.dumps(
        dict(sorted(votes.items(), key=lambda kv: -kv[1]["votes"])), indent=1))

    snapshot = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "stars": info.get("stargazers_count"),
        "watchers": info.get("subscribers_count"),
        "forks": info.get("forks_count"),
        "views_14d": views.get("count"),
        "uniques_14d": views.get("uniques"),
        "clones_14d": clones.get("count"),
        "open_ideas": len(votes),
        "idea_votes_total": sum(v["votes"] for v in votes.values()),
        "open_commissions": len([i for i in commissions if "pull_request" not in i]),
        "pageviews_total": goatcounter(cfg),
        "field_reports": sum(len(v) for v in reports.values()),
        "open_alarms": len(alarms),
    }
    with LEDGER.open("a") as fh:
        fh.write(json.dumps(snapshot) + "\n")

    try:
        subprocess.run(["git", "add", str(LEDGER), str(VOTES),
                        str(ROOT / "foundry" / "reports.json"),
                        str(ROOT / "foundry" / "alarms.json")], check=True, capture_output=True)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if diff.returncode != 0:
            subprocess.run(
                ["git", "-c", "user.name=foundry-metrics",
                 "-c", "user.email=foundry-metrics@users.noreply.github.com",
                 "commit", "-m", "metrics: shift snapshot"],
                check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pass  # local runs without a repo context are fine
    print(f"metrics: snapshot appended — stars={snapshot['stars']} views14d={snapshot['views_14d']} "
          f"votes={snapshot['idea_votes_total']} commissions={snapshot['open_commissions']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
