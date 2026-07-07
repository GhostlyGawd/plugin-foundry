#!/usr/bin/env python3
"""pings — tell suggesters their idea moved. Pure diff core; CLI reads HEAD~1 vs
HEAD. DRY_RUN (default) prints; CI passes --send to use gh. One comment per issue
per shift, fail-soft always."""
import json, pathlib, re, subprocess, sys

from lib import parse_front_matter  # one parser, one truth (v13 C12)

ROOT = pathlib.Path(__file__).resolve().parents[1]

def front(text):
    return parse_front_matter(text or "")[0]

def diff(old, new):
    """old/new: {name: {stage, suggested_in, title}} → [(issue, body)], capped
    to one comment per issue per run."""
    out, seen = [], set()
    for name, cur in sorted(new.items()):
        issue = cur.get("suggested_in")
        if not issue or issue in seen:
            continue
        prev = old.get(name)
        if prev and prev.get("stage") == cur.get("stage"):
            continue
        stage = cur.get("stage", "?")
        title = cur.get("title", name)
        if prev is None:
            line = f"your idea just got a record on the line — **{title}** enters at `{stage}`."
        elif stage == "published":
            line = f"**{title}** shipped. It moved `{prev['stage']}` → `published` this shift."
        else:
            line = f"**{title}** moved down the line: `{prev['stage']}` → `{stage}`."
        body = (f"📮 from the foundry floor — {line}\n\n"
                f"Paper trail: `site/p/{name}.html` on the window. "
                f"Every stage change lands in an append-only ledger; this comment was sent by the shift that did the work.")
        out.append((issue, body))
        seen.add(issue)
    return out

def snapshot(rev=None):
    snap = {}
    for p in sorted((ROOT / "foundry" / "records").glob("*.md")):
        if rev:
            r = subprocess.run(["git", "show", f"{rev}:foundry/records/{p.name}"],
                               capture_output=True, text=True, cwd=ROOT)
            if r.returncode != 0:
                continue
            meta = front(r.stdout)
        else:
            meta = front(p.read_text())
        if meta.get("name"):
            snap[meta["name"]] = {"stage": meta.get("stage"),
                                  "suggested_in": meta.get("suggested_in"),
                                  "title": meta.get("title", meta["name"])}
    return snap

def main(argv):
    send = "--send" in argv
    pings = diff(snapshot("HEAD~1"), snapshot())
    if not pings:
        print("pings: nothing moved for a suggester this shift")
        return 0
    for issue, body in pings:
        if send:
            r = subprocess.run(["gh", "issue", "comment", str(issue), "--body", body],
                               capture_output=True, text=True, cwd=ROOT)
            print(f"pings: #{issue} " + ("sent" if r.returncode == 0 else f"FAILED soft ({r.returncode})"))
        else:
            print(f"pings DRY_RUN → #{issue}:\n{body}\n")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
