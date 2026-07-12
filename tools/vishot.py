#!/usr/bin/env python3
"""vishot.py — visual-regression capture + narration (MASTER P4.3, ADR-031).

The DIFFING is bought (Argos/Percy/Chromatic — hosted, pixel-perfect; config
in argos.config.json, desk-gated). What's built here is the two ends the bought
tool doesn't give you:

  narrate  — the "vision narration" wrapper (the thin novelty layer): a text
             description of what the window CURRENTLY SHOWS, derived from the
             same site/data.json the page renders from. Deterministic, browser-
             free, diffable in a PR — so a reviewer reads what changed on the
             page in words, not just a pixel delta. Written to
             foundry/assets/shots/narration.md.
  shoot    — best-effort PNG capture (Playwright/Chromium) for the bought
             differ to compare. Never required; skips cleanly without a browser.

  vishot.py narrate [--root DIR]
  vishot.py shoot   [--root DIR]     (needs node + playwright + chromium)
Stdlib only for narrate. Deterministic.
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join("foundry", "assets", "shots")
PAGES = ["index.html", "desk.html"]


def _load(root, rel, default):
    p = os.path.join(root, "site", rel)
    if not os.path.exists(p):
        return default
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return default


def narrate(root):
    data = _load(root, "data.json", {})
    quality = _load(root, "quality.json", {})
    recs = data.get("records", [])
    published = [r for r in recs if r.get("stage") == "published"
                 and r.get("kind", "plugin") == "plugin"]
    q = data.get("quality", {})
    theme = (data.get("theme") or {}).get("name") if data.get("theme") else None
    alarms = data.get("alarms", [])
    lines = [
        "# Window narration (vishot.py — what the page currently shows)",
        "",
        f"- Title: **{data.get('phase', '?')} phase**, iteration {data.get('iteration', '?')}",
        f"- Hero counter: {q.get('plugins_shipped', '?')} plugins shipped · "
        f"{q.get('qa_first_try_pct', '?')}% passed QA first try · "
        f"{q.get('bounces_total', '?')} bounces shown · {q.get('iterations', '?')} iterations",
        f"- Shelf: {len(published)} published plugins"
        + (": " + ", ".join(sorted(p.get("name", "?") for p in published)) if published else ""),
        f"- Quality badge message: \"{quality.get('message', '(none)')}\"",
        f"- Theme banner: {theme or '(none)'}",
        f"- Open alarms (amber state): {len(alarms)}",
    ]
    latest = max(published, key=lambda r: str(r.get("updated", "")), default=None)
    if latest:
        lines.append(f"- Latest ship: {latest.get('title')} v{latest.get('version')} "
                     f"({latest.get('updated')})")
    out_dir = os.path.join(root, SHOTS)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "narration.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"vishot: narrated {len(published)} plugins + hero counter → {SHOTS}/narration.md")
    return 0


CAPTURE_JS = r"""
const path = process.argv[2], out = process.argv[3];
let chromium;
for (const p of ['playwright', '/opt/node22/lib/node_modules/playwright']) {
  try { chromium = require(p).chromium; break; } catch (e) {}
}
if (!chromium) { console.error('no-playwright'); process.exit(3); }
(async () => {
  const b = await chromium.launch();
  const page = await b.newPage({ viewport: { width: 1200, height: 900 } });
  await page.goto('file://' + path);
  await page.waitForTimeout(700);
  await page.screenshot({ path: out, fullPage: true });
  await b.close();
  console.log('shot ' + out);
})().catch(e => { console.error(String(e)); process.exit(1); });
"""


def shoot(root):
    out_dir = os.path.join(root, SHOTS)
    os.makedirs(out_dir, exist_ok=True)
    js = os.path.join(out_dir, "_capture.cjs")
    with open(js, "w", encoding="utf-8") as f:
        f.write(CAPTURE_JS)
    took = 0
    for pg in PAGES:
        src = os.path.join(root, "site", pg)
        if not os.path.exists(src):
            continue
        png = os.path.join(out_dir, pg.replace(".html", ".png"))
        try:
            r = subprocess.run(["node", js, src, png], capture_output=True, text=True)
        except FileNotFoundError:
            print("vishot: node not available — skipping capture (narration still ran)")
            os.path.exists(js) and os.remove(js)
            return 0
        if r.returncode == 3:
            print("vishot: no browser available — skipping capture (narration still ran)")
            os.path.exists(js) and os.remove(js)
            return 0
        if r.returncode == 0:
            took += 1
        else:
            print(f"vishot: capture failed for {pg}: {r.stderr.strip()[:120]}")
    os.path.exists(js) and os.remove(js)
    print(f"vishot: captured {took} page screenshot(s) → {SHOTS}/")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="vishot.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("narrate")
    n.add_argument("--root", default=ROOT)
    s = sub.add_parser("shoot")
    s.add_argument("--root", default=ROOT)
    args = ap.parse_args(argv)
    return narrate(args.root) if args.cmd == "narrate" else shoot(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
