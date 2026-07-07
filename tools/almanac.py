#!/usr/bin/env python3
"""almanac — the monthly state-of-the-shift, written from ledgers only.
Usage: python3 tools/almanac.py [YYYY-MM]   (defaults to current month)"""
import collections, datetime, html, json, pathlib, re, subprocess, sys

from lib import parse_front_matter  # one parser, one truth (v13 C12)

ROOT = pathlib.Path(__file__).resolve().parents[1]

def front(p):
    return parse_front_matter(p.read_text())[0]

def main(month=None):
    month = month or datetime.date.today().strftime("%Y-%m")
    j = (ROOT / "state" / "JOURNAL.md").read_text()
    entries = re.findall(r"^## (i\d+) — ([\w-]+) — ([0-9T:\-\.Z]+)", j, re.M)
    total = len(entries)
    as_of = entries[-1][0] if entries else "i0"
    this_month = [(i, r) for i, r, ts in entries if ts.startswith(month) and i != "i0"]
    genesis_note = " (the i0 genesis stamp sits outside the count)" if any(i == "i0" and ts.startswith(month) for i, r, ts in entries) else ""

    roles = collections.Counter(r for _, r in this_month)
    ships, kills = [], []
    for p in sorted((ROOT / "foundry" / "records").glob("*.md")):
        m = front(p)
        if m.get("updated", "").startswith(month):
            if m.get("stage") == "published":
                ships.append(m.get("title", m.get("name")))
            if m.get("stage") in ("shelved", "deprecated"):
                kills.append(m.get("title", m.get("name")))
    adrs = len(re.findall(r"^## ADR-", (ROOT / "state" / "DECISIONS.md").read_text(), re.M))
    bpath = ROOT / "state" / "BUDGET.jsonl"
    if bpath.exists() and bpath.read_text().strip():
        rows = [json.loads(l) for l in bpath.read_text().splitlines() if l.strip()]
        spend = sum(r.get("usd", 0) for r in rows if str(r.get("ts", "")).startswith(month))
        budget_line = f"ledgered spend this month: ${spend:.2f}" + (
            f" · ${spend / len(ships):.2f} per ship" if ships and spend else "")
    else:
        budget_line = "no cost ledger yet — the operator has not armed BUDGET.jsonl; no number is invented in its place"
    qa = subprocess.run(["bash", "tools/qa.sh"], capture_output=True, text=True, cwd=ROOT)
    qa_tail = (qa.stdout.strip().splitlines() or ["qa: unavailable"])[-1]
    adir = ROOT / "site" / "almanac"
    months = sorted({p.stem for p in adir.glob("2*.html")} | {month}) if adir.exists() else [month]
    edition = months.index(month)
    role_html = "".join(f"<li>{html.escape(r)} — {n} iteration{'s' if n != 1 else ''}</li>"
                        for r, n in roles.most_common())
    ship_html = "".join(f"<li>{html.escape(s)}</li>" for s in ships) or "<li>none this month</li>"
    kill_html = "".join(f"<li>{html.escape(k)}</li>" for k in kills) or "<li>none — nothing was shelved</li>"
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Almanac — {month}</title>
<style>body{{background:#F3ECDA;color:#2C2820;font:15px/1.7 Georgia,serif;max-width:680px;margin:0 auto;padding:28px 16px 64px}}
h1{{font-size:20px;letter-spacing:.1em;text-transform:uppercase;border-bottom:3px double #2C2820;padding-bottom:8px}}
h2{{font-size:14px;letter-spacing:.12em;text-transform:uppercase;margin-top:26px}}
.note{{font-size:12.5px;opacity:.75}} a{{color:#7A4A12}} ul{{padding-left:20px}}</style></head><body>
<h1>The Almanac · Edition {edition:03d} — {month}</h1>
<p class="note">written by the machine about itself, from ledgers only · <a href="../index.html">back to the window</a></p>
<h2>The month in iterations</h2>
<p>{len(this_month)} iteration{'s' if len(this_month) != 1 else ''} this month ({total} lifetime), as of {as_of}{genesis_note}. By role:</p>
<ul>{role_html or '<li>none yet</li>'}</ul>
<h2>Ships</h2><ul>{ship_html}</ul>
<h2>Shelved &amp; deprecated</h2><ul>{kill_html}</ul>
<h2>Governance</h2><p>{adrs} ADRs on the books, append-only.</p>
<h2>The money</h2><p>{html.escape(budget_line)}</p>
<h2>The gates, right now</h2><p><code>{html.escape(qa_tail)}</code></p>
<footer class="note">Every number above has a source file; anything the ledgers cannot answer says so out loud.</footer>
</body></html>"""
    out = ROOT / "site" / "almanac"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{month}.html").write_text(page)
    eds = sorted(p.name for p in out.glob("2*.html"))
    idx = "".join(f'<li><a href="{e}">{e[:-5]}</a></li>' for e in reversed(eds))
    (out / "index.html").write_text(
        f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Almanac — editions</title><style>body{{background:#F3ECDA;color:#2C2820;font:15px/1.7 Georgia,serif;max-width:680px;margin:0 auto;padding:28px 16px}}</style></head>
<body><h1>The Almanac</h1><p>monthly state-of-the-shift, machine-written from ledgers · <a href="../index.html">window</a></p><ul>{idx}</ul></body></html>""")
    print(f"almanac: edition {edition:03d} for {month} — {len(this_month)} iterations, {len(ships)} ships")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
