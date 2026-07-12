#!/usr/bin/env python3
"""commit.py — per-agent commit identity (MASTER P0.3, ADR-026).

Commits staged work as a registered agent: author from
foundry/agents/identities.json, message + an `Agent: <id>` trailer.
`git log --author` then cleanly separates agents (G7 — attribution collapse).
Refuses unknown agents (no manifest / no identity → no pen). Respects any
configured commit signing (never passes --no-gpg-sign).

Usage: commit.py --agent <id> -m "<message>" [--add-all] [--root DIR]
"""
import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import load_agents  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(prog="commit.py")
    ap.add_argument("--agent", required=True)
    ap.add_argument("-m", "--message", required=True)
    ap.add_argument("--add-all", action="store_true")
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)

    errors = []
    ids = {a["id"] for a in load_agents(errors, args.root)}
    if errors:
        print("commit: registry unlawful — refusing to commit:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    if args.agent not in ids:
        print(f"commit: unknown agent '{args.agent}' — no manifest, no pen")
        return 1
    id_path = os.path.join(args.root, "foundry", "agents", "identities.json")
    try:
        identities = json.load(open(id_path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"commit: identities.json unreadable ({e})")
        return 1
    ident = identities.get(args.agent)
    if not isinstance(ident, dict) or not ident.get("name") or not ident.get("email"):
        print(f"commit: no identity for '{args.agent}' in identities.json")
        return 1

    if args.add_all:
        subprocess.run(["git", "-C", args.root, "add", "-A"], check=True)
    msg = args.message.rstrip() + f"\n\nAgent: {args.agent}\n"
    r = subprocess.run(
        ["git", "-C", args.root,
         "-c", f"user.name={ident['name']}",
         "-c", f"user.email={ident['email']}",
         "commit", "-m", msg],
        capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
