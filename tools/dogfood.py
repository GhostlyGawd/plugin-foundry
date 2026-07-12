#!/usr/bin/env python3
"""dogfood.py — the dogfood report card (MASTER P1.4, ADR-031). MASTER's
"best halo feature": the factory grades itself on eating its own dog food,
backed by evidence, honestly (including the plugins it hasn't used yet).

Evidence is mined only from this repo (growth-honesty law): mentions of a
published plugin in state/JOURNAL.md (the workshop narrating its own use), the
dogfood clause references, and membership in a shipped starter kit. Grades:
  used          — 3+ evidence hits
  lightly-used  — 1–2 hits
  not-yet       — 0 hits (shown honestly, not hidden — that's the point)

Writes foundry/dogfood.json → build.py renders a card. Deterministic. Stdlib.
  dogfood.py grade     recompute the card
  dogfood.py show      print the current grades
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from lib import parse_front_matter  # noqa: E402

OUT = os.path.join(ROOT, "foundry", "dogfood.json")


def published_plugins():
    out = []
    recdir = os.path.join(ROOT, "foundry", "records")
    for fn in sorted(os.listdir(recdir)):
        if not fn.endswith(".md"):
            continue
        meta, _ = parse_front_matter(open(os.path.join(recdir, fn), encoding="utf-8").read())
        if meta.get("stage") == "published" and meta.get("kind", "plugin") == "plugin":
            out.append(meta.get("name", fn[:-3]))
    return out


def kit_members():
    try:
        kits = json.load(open(os.path.join(ROOT, "foundry", "kits.json"), encoding="utf-8"))
        members = set()
        for k in kits.get("kits", []):
            members.update(k.get("plugins", []))
        return members
    except (OSError, ValueError):
        return set()


# Use/friction verbs — the dogfood clause is about USING a shipped plugin as a
# tool of the workshop, not building it. A line must pair the slug with one of
# these to count as dogfood evidence; "built/published/shipped X" does not.
USE_CX = re.compile(
    r"(used|using|use|ran|run|reached for|applied|invoked|dogfood|"
    r"friction|relied on|leaned on)", re.I)
BUILD_CX = re.compile(r"(built|building|published|publish|shipped|scaffold|specced|bumped)", re.I)


def grade(name, journal, kits):
    slug = re.compile(r"\b" + re.escape(name) + r"\b")
    total_mentions = 0
    use_lines = 0
    for line in journal.splitlines():
        if not slug.search(line):
            continue
        total_mentions += 1
        # a genuine dogfood line: names the plugin near use language, and isn't
        # dominated by build language (its own construction entry)
        if USE_CX.search(line) and not BUILD_CX.search(line):
            use_lines += 1
    evidence = []
    if use_lines:
        evidence.append(f"{use_lines} dogfood line(s)")
    if name in kits:
        evidence.append("in a shipped starter kit")
    if total_mentions and not use_lines:
        evidence.append(f"{total_mentions} construction mention(s) — dogfood pending")
    score = use_lines + (1 if name in kits else 0)
    tier = "used" if score >= 3 else "lightly-used" if score >= 1 else "not-yet"
    return {"plugin": name, "grade": tier, "score": score,
            "evidence": evidence, "mentions": total_mentions, "use_lines": use_lines}


def compute():
    journal = ""
    jp = os.path.join(ROOT, "state", "JOURNAL.md")
    if os.path.exists(jp):
        journal = open(jp, encoding="utf-8").read()
    kits = kit_members()
    cards = [grade(n, journal, kits) for n in published_plugins()]
    cards.sort(key=lambda c: (-c["score"], c["plugin"]))
    summary = {t: sum(1 for c in cards if c["grade"] == t)
               for t in ("used", "lightly-used", "not-yet")}
    return {"_law": "Evidence mined only from this repo (growth-honesty). "
                     "not-yet plugins are shown, never hidden — honesty is the feature.",
            "summary": summary, "cards": cards}


def main(argv=None):
    cmd = (argv or sys.argv[1:] or ["grade"])[0]
    data = compute()
    if cmd == "grade":
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
            f.write("\n")
        s = data["summary"]
        print(f"dogfood: graded {len(data['cards'])} plugins — "
              f"{s['used']} used · {s['lightly-used']} lightly · {s['not-yet']} not-yet")
    elif cmd == "show":
        for c in data["cards"]:
            print(f"  [{c['grade']:12s}] {c['plugin']} — {', '.join(c['evidence']) or 'no evidence yet'}")
    else:
        print("usage: dogfood.py grade|show")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
