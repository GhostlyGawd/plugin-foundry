#!/usr/bin/env python3
"""validate_state.py — the shared-state validator (MASTER P0.4, ADR-026).

Twenty agents sharing one repo means state/ and foundry/*.json are the nervous
system: one malformed line and downstream tools mis-read silently. This gate
checks every shared file against its real shape with pointed messages. Missing
optional files are fine; a present-but-broken file never is.

Runs in CI (gates.yml) and as the orchestrator's pre-commit gate (P0.7).
Stdlib only. Usage: validate_state.py [--root DIR]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import load_agents  # noqa: E402

PHASES = ("bootstrap", "grow")
DESK_STATUSES = ("open", "approved", "rejected")
DESK_KINDS = ("ratify", "approve", "decide", "alarm")


def _load(path, errors, label, kind=dict):
    if not os.path.exists(path):
        return None
    try:
        v = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        errors.append(f"{label}: unreadable JSON ({e})")
        return None
    if not isinstance(v, kind):
        errors.append(f"{label}: expected {kind.__name__}, got {type(v).__name__}")
        return None
    return v


def _jsonl(path, errors, label, check_line):
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except ValueError as e:
                errors.append(f"{label}:{n}: malformed JSONL line ({e})")
                continue
            if not isinstance(rec, dict):
                errors.append(f"{label}:{n}: line is not an object")
                continue
            check_line(rec, f"{label}:{n}", errors)


def _num_or_null(rec, keys, label, errors):
    for k in keys:
        if k in rec and rec[k] is not None and not isinstance(rec[k], (int, float)):
            errors.append(f"{label}: '{k}' must be a number or null (honest-null law)")


def check_state_json(root, errors):
    p = os.path.join(root, "state", "STATE.json")
    if not os.path.exists(p):
        errors.append("state/STATE.json: missing — the loop has no memory")
        return
    s = _load(p, errors, "STATE.json")
    if s is None:
        return
    for k, t in (("schema_version", int), ("codename", str), ("name", str),
                 ("iteration", int), ("phase", str), ("role_queue", list),
                 ("notes", str)):
        if k not in s:
            errors.append(f"STATE.json: missing '{k}'")
        elif not isinstance(s[k], t):
            errors.append(f"STATE.json: '{k}' must be {t.__name__}")
    if isinstance(s.get("iteration"), int) and s["iteration"] < 0:
        errors.append("STATE.json: iteration must be >= 0")
    if s.get("phase") not in PHASES:
        errors.append(f"STATE.json: phase must be one of {PHASES}")
    if isinstance(s.get("role_queue"), list) and not all(
            isinstance(r, str) and r for r in s["role_queue"]):
        errors.append("STATE.json: role_queue entries must be non-empty strings")
    th = s.get("theme")
    if th is not None and (not isinstance(th, dict) or "name" not in th):
        errors.append("STATE.json: theme, when set, is an object with a 'name'")


def check_budget(root, errors):
    def line(rec, label, errs):
        if "ts" not in rec or not isinstance(rec["ts"], str):
            errs.append(f"{label}: missing string 'ts'")
        _num_or_null(rec, ("cost_usd",), label, errs)
    _jsonl(os.path.join(root, "state", "BUDGET.jsonl"), errors,
           "state/BUDGET.jsonl", line)


def check_metrics(root, errors):
    def line(rec, label, errs):
        if "ts" not in rec or not isinstance(rec["ts"], str):
            errs.append(f"{label}: missing string 'ts'")
        _num_or_null(rec, ("stars", "watchers", "forks", "views_14d",
                           "uniques_14d", "clones_14d", "open_ideas",
                           "idea_votes_total", "open_commissions",
                           "pageviews_total"), label, errs)
    _jsonl(os.path.join(root, "state", "METRICS.jsonl"), errors,
           "state/METRICS.jsonl", line)


def check_desk(root, errors):
    first = {}

    def line(rec, label, errs):
        iid = rec.get("id")
        if not isinstance(iid, str) or not iid.startswith("d-"):
            errs.append(f"{label}: 'id' must be a 'd-…' string")
            return
        if "status" in rec and rec["status"] not in DESK_STATUSES:
            errs.append(f"{label}: status must be one of {DESK_STATUSES}")
        if iid not in first:
            first[iid] = True
            for k in ("kind", "title", "ts"):
                if k not in rec:
                    errs.append(f"{label}: first line for {iid} missing '{k}'")
            if rec.get("kind") is not None and rec.get("kind") not in DESK_KINDS:
                errs.append(f"{label}: kind must be one of {DESK_KINDS}")
    _jsonl(os.path.join(root, "state", "DESK.jsonl"), errors,
           "state/DESK.jsonl", line)


def check_foundry_json(root, errors):
    fx = os.path.join(root, "foundry")
    votes = _load(os.path.join(fx, "votes.json"), errors, "foundry/votes.json")
    if votes is not None:
        for k, v in votes.items():
            if not isinstance(v, dict) or "title" not in v or not isinstance(
                    v.get("votes", 0), int):
                errors.append(f"foundry/votes.json: entry {k!r} needs title + int votes")
    ver = _load(os.path.join(fx, "verified.json"), errors, "foundry/verified.json")
    if ver is not None and not isinstance(ver.get("verified"), list):
        errors.append("foundry/verified.json: 'verified' must be a list")
    _load(os.path.join(fx, "reports.json"), errors, "foundry/reports.json")
    kits = _load(os.path.join(fx, "kits.json"), errors, "foundry/kits.json")
    if kits is not None:
        for i, kit in enumerate(kits.get("kits", [])):
            if not isinstance(kit, dict) or "id" not in kit or "name" not in kit:
                errors.append(f"foundry/kits.json: kits[{i}] needs id + name")
    alarms = _load(os.path.join(fx, "alarms.json"), errors,
                   "foundry/alarms.json", list)
    if alarms is not None:
        for i, a in enumerate(alarms):
            if not isinstance(a, dict) or "title" not in a:
                errors.append(f"foundry/alarms.json: [{i}] needs a title")
    net = _load(os.path.join(fx, "network.json"), errors, "foundry/network.json")
    if net is not None and not isinstance(net.get("network"), list):
        errors.append("foundry/network.json: 'network' must be a list")


def check_agents_state(root, errors):
    ag = os.path.join(root, "foundry", "agents")
    if not os.path.isdir(ag):
        return
    # manifests lawful + registry in sync (same loader the gates trust)
    agents = load_agents(errors, root)
    reg = _load(os.path.join(ag, "registry.json"), errors,
                "foundry/agents/registry.json")
    if reg is not None:
        disk = [a["id"] for a in agents]
        listed = [a.get("id") for a in reg.get("agents", [])]
        if disk != listed:
            errors.append(f"foundry/agents/registry.json: drift — disk {disk} "
                          f"vs registry {listed} (run python3 tools/build.py)")
    ids = _load(os.path.join(ag, "identities.json"), errors,
                "foundry/agents/identities.json")
    if ids is not None:
        for a in agents:
            ident = ids.get(a["id"])
            if not isinstance(ident, dict) or not ident.get("name") or not ident.get("email"):
                errors.append(f"foundry/agents/identities.json: no identity for "
                              f"'{a['id']}' (P0.3: every agent commits as itself)")
    hb = _load(os.path.join(ag, "heartbeats.json"), errors,
               "foundry/agents/heartbeats.json")
    if hb is not None:
        for k, v in hb.items():
            if k.startswith("_"):
                continue
            if not isinstance(v, dict) or "ts" not in v:
                errors.append(f"foundry/agents/heartbeats.json: '{k}' needs a 'ts'")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="validate_state.py")
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    errors = []
    check_state_json(args.root, errors)
    check_budget(args.root, errors)
    check_metrics(args.root, errors)
    check_desk(args.root, errors)
    check_foundry_json(args.root, errors)
    check_agents_state(args.root, errors)
    if errors:
        print(f"STATE: FAIL — {len(errors)} problem(s)")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print("STATE: OK — shared state is well-formed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
