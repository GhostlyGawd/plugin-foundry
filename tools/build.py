#!/usr/bin/env python3
"""build.py — regenerates foundry/INDEX.md and the whole living window:
site/index.html, data.json, p/<name>.html (birth certificates), saga.html,
embed.html, badge.json, feed.xml.

v5 additions (ADR-009/010): token-cost badges, starter kits, idea credits, field
reports on certificates, streak heatmap, hall of prospectors & patrons, saga page,
embeds + badge endpoint, fuel gauge, ops-alarm amber state. Everything rendered is
substantiated by this repo (dark-pattern law). Stdlib only.
"""
import html
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "foundry" / "records"
STAGES = ["idea", "spec", "building", "rc", "published", "deprecated", "shelved"]
TRACK = ["idea", "spec", "building", "rc", "published"]


# ---------------------------------------------------------------- collectors --
def parse_front_matter(text):
    parts = text.split("---", 2)
    meta = {}
    if len(parts) < 3:
        return meta
    for line in parts[1].strip().splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        key, _, raw = line.partition(":")
        key, raw = key.strip(), raw.split(" #")[0].strip()
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            meta[key] = [v.strip() for v in inner.split(",") if v.strip()] if inner else []
        else:
            meta[key] = raw
    return meta


def collect_records():
    out = []
    for path in sorted(RECORDS.glob("*.md")):
        text = path.read_text()
        meta = parse_front_matter(text)
        meta["record_path"] = str(path.relative_to(ROOT))
        parts = text.split("---", 2)
        meta["_body"] = parts[2] if len(parts) >= 3 else text
        out.append(meta)
    return out


def extract_sections(body):
    out, title, buf = [], None, []
    for line in body.splitlines():
        if line.startswith("## "):
            if title:
                out.append((title, "\n".join(buf).strip()))
            title, buf = line[3:].strip(), []
        elif title:
            buf.append(line)
    if title:
        out.append((title, "\n".join(buf).strip()))
    return out


def collect_journal(limit=8):
    text = (ROOT / "state" / "JOURNAL.md").read_text()
    entries = re.findall(
        r"^## (i\d+) — ([\w-]+) — ([0-9TZ:\-\.]+)\n(.*?)(?=^## i|\Z)", text, re.M | re.S)
    ticker = []
    for it, role, ts, body in entries[-limit:]:
        did = ""
        m = re.search(r"-\s*did:\s*(.+)", body)
        if m:
            did = " ".join(m.group(1).split())
        line = re.search(r"-\s*line:\s*(.+)", body)
        extra = f" · {line.group(1).strip()}" if line and "n/a" not in line.group(1) else ""
        ticker.append({"it": it, "role": role, "ts": ts, "text": (did[:120] + extra[:80]).strip()})
    return list(reversed(ticker))


def collect_streak(days=84):
    """Real journal entries per day for the trailing window; blanks stay blank."""
    text = (ROOT / "state" / "JOURNAL.md").read_text()
    counts = {}
    for ts in re.findall(r"^## i\d+ — [\w-]+ — ([0-9TZ:\-\.]+)", text, re.M):
        counts[ts[:10]] = counts.get(ts[:10], 0) + 1
    today = datetime.now(timezone.utc).date()
    out = []
    for i in range(days - 1, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        out.append({"d": d, "n": counts.get(d, 0)})
    return out


def collect_hall(records):
    prospectors = {}
    patrons = []
    for r in records:
        who = r.get("prospected_by")
        if who:
            entry = prospectors.setdefault(who, {"login": who, "shipped": 0, "total": 0, "issues": []})
            entry["total"] += 1
            if r.get("stage") == "published":
                entry["shipped"] += 1
            if r.get("suggested_in"):
                entry["issues"].append(str(r["suggested_in"]))
        if r.get("patron"):
            patrons.append(str(r["patron"]))
    ranked = sorted(prospectors.values(), key=lambda e: (-e["shipped"], -e["total"], e["login"]))
    return {"prospectors": ranked, "patrons": sorted(set(patrons))}


def load_json(path, default):
    try:
        return json.loads(path.read_text())
    except Exception:  # noqa: BLE001
        return default


def latest_metrics():
    path = ROOT / "state" / "METRICS.jsonl"
    if not path.exists():
        return {}
    lines = [l for l in path.read_text().splitlines() if l.strip()]
    try:
        return json.loads(lines[-1]) if lines else {}
    except json.JSONDecodeError:
        return {}


def fuel(cfg):
    prefix = datetime.now(timezone.utc).strftime("%Y-%m")
    mtd, entries = 0.0, 0
    ledger = ROOT / "state" / "BUDGET.jsonl"
    if ledger.exists():
        for line in ledger.read_text().splitlines():
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if str(e.get("ts", "")).startswith(prefix) and e.get("cost_usd") is not None:
                mtd += e["cost_usd"]
                entries += 1
    cap = cfg.get("monthly_budget_usd")
    return {"mtd": round(mtd, 2), "cap": cap, "entries": entries}


def roadmap_lanes(records):
    def is_comm(r):
        return bool(r.get("commission"))
    active = [r for r in records if r.get("stage") in TRACK]
    return {
        "commissioned": [r for r in active if is_comm(r) and r["stage"] != "published"],
        "building": [r for r in active if not is_comm(r) and r["stage"] in ("building", "rc")],
        "next": [r for r in active if not is_comm(r) and r["stage"] == "spec"],
        "ideas": [r for r in active if not is_comm(r) and r["stage"] == "idea"],
        "shipped": sorted((r for r in records if r.get("stage") == "published"),
                          key=lambda r: r.get("updated", ""), reverse=True),
        "shelved": [r for r in records if r.get("stage") == "shelved"],
    }


# ----------------------------------------------------------------- INDEX.md --
def build_index(records, state, mp_name):
    name = state.get("name") or f"{state.get('codename', 'foundry')} (pre-brand)"
    counts = {s: sum(1 for r in records if r.get("stage") == s) for s in STAGES}
    lines = [
        "<!-- GENERATED by tools/build.py — do not edit by hand -->",
        f"# {name} — Plugin Line Index",
        "",
        f"{len(records)} records · iteration {state.get('iteration', 0)} · phase {state.get('phase', '?')}",
        "",
        "**Line:** " + " → ".join(f"{s}:{counts[s]}" for s in TRACK)
        + f" · deprecated:{counts['deprecated']} · shelved:{counts['shelved']}",
        "",
    ]
    for stage in STAGES:
        group = sorted((r for r in records if r.get("stage") == stage), key=lambda r: r.get("name", ""))
        lines.append(f"## {stage} ({len(group)})")
        if not group:
            lines.append("_none_")
        for r in group:
            ver = f" v{r['version']}" if r.get("version") not in (None, "null", "") else ""
            comm = f" · commission #{r['commission']}" if r.get("commission") else ""
            cred = f" · prospected by @{r['prospected_by']}" if r.get("prospected_by") else ""
            install = f" — install: `/plugin install {r['name']}@{mp_name}`" \
                if stage == "published" and r.get("kind", "plugin") == "plugin" else ""
            lines.append(
                f"- [{r.get('name')}{ver}]({r['record_path'].replace('foundry/', '')}) "
                f"`{r.get('category')}` `{'+'.join(r.get('components', []))}`{comm}{cred} — {r.get('one_liner', '')}{install}")
        lines.append("")
    (ROOT / "foundry" / "INDEX.md").write_text("\n".join(lines) + "\n")
    return counts


# ------------------------------------------------------------ index template --
TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@ — a plugin workshop run entirely by AI</title>
<meta name="description" content="Claude Code plugins pitched, built, tested, reviewed, and published by an autonomous loop. Watch the line move; install what it ships; commission what's missing.">
<link rel="alternate" type="application/atom+xml" title="ships" href="feed.xml">
<style>
  :root{
    --paper:#E9DFC8; --card:#F3ECDA; --ink:#2C2820; --line:#B5A683;
    --dim:#7E7460; --stamp:#2F5A8F; --hole:#CDBF9E; --live:#3F7D4E; --amber:#B07818;
  }
  *{box-sizing:border-box; margin:0}
  html{scroll-behavior:smooth}
  body{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
    background:var(--paper); color:var(--ink); font-size:14px; line-height:1.55;
    padding:20px; min-height:100vh}
  a{color:var(--stamp)}
  .board{max-width:1020px; margin:0 auto}
  header{display:flex; flex-wrap:wrap; gap:6px 22px; align-items:baseline;
    padding:12px 2px; border-bottom:2px solid var(--ink)}
  header h1{font-size:22px; letter-spacing:.16em; text-transform:uppercase}
  .pulse{display:inline-flex; align-items:center; gap:7px; font-size:11px;
    letter-spacing:.16em; text-transform:uppercase; color:var(--live)}
  .dot{width:9px; height:9px; border-radius:50%; background:var(--live)}
  .tagchips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 2px}
  .tagbtn{cursor:pointer;background:transparent;font:inherit;min-height:44px}
  .tagbtn.active{background:#2C2820;color:#F3ECDA;border-color:#2C2820}
  @media (prefers-reduced-motion:no-preference){
    .dot{animation:beat 2.4s ease-in-out infinite}
    @keyframes beat{0%,100%{opacity:1}50%{opacity:.25}}}
  header .k{font-size:11px; color:var(--dim); letter-spacing:.16em; text-transform:uppercase}
  header .k b{color:var(--ink); font-weight:400}
  .alarms{display:none; font-size:11px; letter-spacing:.14em; text-transform:uppercase;
    color:var(--amber); border:1.5px solid var(--amber); padding:2px 8px}
  .strap{padding:9px 2px; color:var(--dim); font-size:12.5px; border-bottom:1px solid var(--line)}
  .strap b{color:var(--ink); font-weight:400}
  .jump{position:sticky; top:0; z-index:5; background:var(--paper); display:flex; gap:18px;
    padding:9px 2px; border-bottom:1px solid var(--line); font-size:11px; letter-spacing:.16em;
    text-transform:uppercase; overflow-x:auto}
  .jump a{color:var(--dim); text-decoration:none; white-space:nowrap}
  .jump a:hover,.jump a:focus-visible{color:var(--stamp)}
  .theme{border:1.5px dashed var(--stamp); color:var(--stamp); padding:8px 12px;
    margin:12px 0 0; font-size:12px; letter-spacing:.06em}
  .theme b{letter-spacing:.14em; text-transform:uppercase}
  .tape{border-bottom:1px solid var(--line); overflow:hidden; white-space:nowrap; padding:8px 0}
  .tape .reel{display:inline-block; padding-left:100%}
  @media (prefers-reduced-motion:no-preference){
    .tape .reel{animation:reel 55s linear infinite}
    .tape:hover .reel{animation-play-state:paused}
    @keyframes reel{to{transform:translateX(-100%)}}}
  @media (prefers-reduced-motion:reduce){.tape{white-space:normal} .tape .reel{padding-left:0}}
  .tape span{color:var(--dim); font-size:12px; margin-right:34px}
  .tape span b{color:var(--ink); font-weight:400}
  .tape span em{color:var(--stamp); font-style:normal}
  /* streak heatmap — real days only */
  .streakwrap{display:flex; gap:14px; align-items:center; padding:10px 2px; border-bottom:1px solid var(--line)}
  .streak{display:grid; grid-auto-flow:column; grid-template-rows:repeat(7,10px); gap:3px}
  .day{width:10px; height:10px; background:var(--card); border:1px solid var(--hole)}
  .day.n1{background:#C9CDA4; border-color:#B5A683}
  .day.n2{background:#8FA86B; border-color:#7E9757}
  .day.n3{background:#4F7D3F; border-color:#3F6A31}
  .streaklabel{font-size:10px; color:var(--dim); letter-spacing:.14em; text-transform:uppercase; max-width:120px}
  /* stats + fuel */
  .stats{display:flex; border-bottom:1px solid var(--line)}
  .stat{flex:1; padding:10px 4px; text-align:center; border-right:1px solid var(--line)}
  .stat:last-child{border-right:0}
  .stat .n{display:block; font-size:20px}
  .stat .s{display:block; font-size:9px; letter-spacing:.14em; text-transform:uppercase; color:var(--dim)}
  .fuelrow{display:flex; gap:12px; align-items:center; padding:9px 2px; border-bottom:1px solid var(--line);
    font-size:11px; letter-spacing:.1em; text-transform:uppercase; color:var(--dim)}
  .fuelrow b{color:var(--ink); font-weight:400}
  .fuelbar{flex:1; height:6px; background:var(--card); border:1px solid var(--line); position:relative; max-width:280px}
  .fuelbar i{position:absolute; inset:0 auto 0 0; background:var(--amber)}
  .lane{display:flex; border-bottom:1px solid var(--line)}
  .lanebtn{flex:1; background:transparent; border:0; border-right:1px solid var(--line);
    color:var(--dim); font:inherit; padding:9px 3px; cursor:pointer; min-width:0}
  .lanebtn:last-child{border-right:0}
  .lanebtn .n{display:block; font-size:19px; color:var(--ink)}
  .lanebtn .s{display:block; font-size:9px; letter-spacing:.12em; text-transform:uppercase;
    overflow:hidden; text-overflow:ellipsis}
  .lanebtn[aria-pressed="true"]{background:var(--card); box-shadow:inset 0 -3px 0 var(--stamp)}
  .tools{display:flex; gap:10px; padding:12px 2px}
  .tools input{flex:1; background:var(--card); border:1px solid var(--line); color:var(--ink);
    font:inherit; padding:8px 10px}
  .tools input::placeholder{color:var(--dim)}
  .tools input:focus-visible,.lanebtn:focus-visible,.cta:focus-visible{outline:2px solid var(--stamp); outline-offset:-2px}
  h3.rule{font-size:12px; letter-spacing:.2em; text-transform:uppercase; color:var(--dim);
    border-bottom:2px solid var(--ink); padding:26px 2px 6px; scroll-margin-top:44px}
  #grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:14px; padding:12px 0 4px}
  .tag{background:var(--card); border:1px solid var(--line); padding:12px 14px;
    display:flex; flex-direction:column; gap:8px; position:relative}
  .tag::before{content:""; position:absolute; top:10px; left:-6px; width:12px; height:12px;
    border-radius:50%; background:var(--paper); border:1px solid var(--line)}
  .tag .top{display:flex; justify-content:space-between; gap:8px; align-items:baseline}
  .tag .id{font-size:12px; letter-spacing:.08em}
  .tag .id em{color:var(--dim); font-style:normal; font-size:10px; display:block; letter-spacing:.14em; text-transform:uppercase}
  .ver{font-size:10px; letter-spacing:.12em; border:1.5px solid var(--stamp); color:var(--stamp);
    padding:1px 7px; text-transform:uppercase; transform:rotate(-2deg); white-space:nowrap}
  .ver.ghost{border-color:var(--dim); color:var(--dim); transform:none}
  .tag h2{font-size:15px; letter-spacing:.02em}
  .tag p{color:var(--dim); font-size:12.5px}
  .track{display:flex; gap:6px; align-items:center; font-size:9px; color:var(--dim);
    letter-spacing:.1em; text-transform:uppercase}
  .punch{width:11px; height:11px; border-radius:50%; border:1.5px solid var(--ink); display:inline-block}
  .punch.done{background:var(--ink)}
  .chips{display:flex; flex-wrap:wrap; gap:6px}
  .chip{font-size:10px; letter-spacing:.1em; text-transform:uppercase; border:1px solid var(--line);
    padding:1px 7px; color:var(--dim)}
  .chip.comm{border-color:var(--stamp); color:var(--stamp)}
  .chip.tok{border-style:dotted}
  .credit{font-size:11px; color:var(--dim)}
  .install{background:var(--ink); color:var(--paper); font-size:11.5px; padding:7px 9px;
    overflow-x:auto; white-space:nowrap; user-select:all; cursor:text}
  .note{font-size:10.5px; color:var(--dim); letter-spacing:.06em}
  .prov{font-size:11px; letter-spacing:.08em}
  .kit{border:1.5px solid var(--ink); background:var(--card); padding:14px; margin:12px 0}
  .kit h4{font-size:13px; letter-spacing:.12em; text-transform:uppercase}
  .kit p{color:var(--dim); font-size:12.5px; margin:6px 0 10px}
  .kit .pending{font-size:11px; color:var(--dim)}
  .kit .install{white-space:pre}
  .lanes{display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; padding:12px 0}
  .col{border:1px solid var(--line); background:var(--card)}
  .col h4{font-size:10px; letter-spacing:.18em; text-transform:uppercase; padding:8px 10px;
    border-bottom:1px solid var(--line); color:var(--dim)}
  .col h4 b{color:var(--ink); font-weight:400}
  .col ul{list-style:none; padding:8px 10px; display:flex; flex-direction:column; gap:8px}
  .col li{font-size:12px}
  .col li em{color:var(--dim); font-style:normal; display:block; font-size:11px}
  .col li .cnum{color:var(--stamp); font-size:10px; letter-spacing:.1em}
  .col .none{color:var(--dim); font-size:11px}
  .votes{display:flex; flex-direction:column; padding:10px 0}
  .vrow{display:grid; grid-template-columns:64px 1fr auto; gap:12px; align-items:center;
    padding:10px 12px; border:1px solid var(--line); border-bottom:0; background:var(--card); font-size:13px}
  .vrow:last-child{border-bottom:1px solid var(--line)}
  .vcount{font-size:16px; text-align:center}
  .vcount em{display:block; font-size:9px; font-style:normal; color:var(--dim); letter-spacing:.12em; text-transform:uppercase}
  .vrow a{white-space:nowrap; font-size:12px}
  .vnone{color:var(--dim); font-size:12.5px; padding:12px 2px}
  .hall{display:none; padding:10px 0}
  .hall .hrow{display:flex; gap:14px; padding:9px 12px; border:1px solid var(--line);
    border-bottom:0; background:var(--card); font-size:12.5px; align-items:baseline}
  .hall .hrow:last-child{border-bottom:1px solid var(--line)}
  .hall .hrow b{font-weight:400}
  .hall .hrow em{color:var(--dim); font-style:normal; font-size:11px}
  .duo{display:grid; grid-template-columns:1fr 1fr; gap:14px; padding:12px 0}
  @media (max-width:680px){.duo{grid-template-columns:1fr}}
  .panel{border:1.5px solid var(--ink); background:var(--card); padding:16px}
  .panel h5{font-size:13px; letter-spacing:.12em; text-transform:uppercase; margin-bottom:8px}
  .panel p{font-size:12.5px; color:var(--dim); margin-bottom:10px}
  .panel .fine{font-size:10.5px}
  .cta{display:inline-block; background:var(--stamp); color:var(--paper); text-decoration:none;
    font:inherit; font-size:13px; letter-spacing:.1em; padding:10px 16px; border:0; cursor:pointer}
  .cta.ghost{background:transparent; color:var(--dim); border:1.5px dashed var(--line); cursor:default}
  footer{padding:14px 2px; border-top:2px solid var(--ink); color:var(--dim); margin-top:20px;
    font-size:11px; letter-spacing:.05em; display:flex; flex-wrap:wrap; gap:6px 18px}
  .empty{padding:30px 2px; color:var(--dim); text-align:center; display:none}
</style>
</head>
<body>
<div class="board">
  <header>
    <h1>@@TITLE@@</h1>
    <span class="pulse"><span class="dot"></span><span id="lastshift">live</span></span>
    <span class="k">iteration <b id="iter">@@ITER@@</b></span>
    <span class="k">phase <b id="phase">@@PHASE@@</b></span>
    <span class="alarms" id="alarms"></span>
  </header>
  <p class="strap">Every plugin here was <b>pitched, specced, built, tested, reviewed, and
  published by an autonomous Claude Code loop</b> — no human on the line. This page
  redeploys each time it works. Scroll the shelf, watch the roadmap move, or
  <a href="#request">commission the next one</a>.</p>
  <nav class="jump" aria-label="jump to section">
    <a href="#shelf">Shelf</a><a href="#kits">Kits</a><a href="#roadmap">Roadmap</a><a href="#vote">Vote</a><a href="saga.html">Saga</a><a href="theater.html">Theater</a><a href="almanac/index.html">Almanac</a><a href="queue.html">Queue</a><a href="#request">Commission</a><a href="#install">Install</a>
  </nav>
  <div id="themebox"></div>
  <div class="tape" aria-label="latest shop-floor journal entries"><div class="reel" id="reel"></div></div>
  <div class="streakwrap" aria-label="iterations per day, last 12 weeks — real journal entries only">
    <div class="streak" id="streak"></div>
    <span class="streaklabel">shifts, last 12 weeks — quiet days stay blank</span>
  </div>
  <div class="stats" id="stats" aria-label="substantiated numbers only"></div>
  <div class="fuelrow" id="fuelrow" aria-label="the fuel gauge — real ledger spend"></div>

  <h3 class="rule" id="shelf">The shelf — tap a stage to filter</h3>
  <nav class="lane" aria-label="pipeline filter">@@LANE@@</nav>
  <div class="tools">
    <input id="q" type="search" placeholder="Search plugins by name, job, or tag" aria-label="Search plugins">
    <div class="tagchips" id="tagchips" role="group" aria-label="filter by tag"></div>
    <span class="chip" id="nextshift" title="computed from the shift cron, no server involved"></span>
  </div>
  <main id="grid"></main>
  <p class="empty" id="empty">Nothing matches. Clear the filter — or commission it below.</p>

  <h3 class="rule" id="kits">Starter kits — one block, ready to paste</h3>
  <div id="kitbox"></div>

  <h3 class="rule" id="roadmap">Roadmap — the line, in lanes</h3>
  <div class="lanes" id="lanes"></div>

  <h3 class="rule" id="vote">Vote — free lever, real 👍s on GitHub</h3>
  <p class="strap">Votes order the idea pool; <a href="#request">commissions</a> skip the
  queue. Counts are read from GitHub each shift — the workshop can't inflate them.</p>
  <div class="votes" id="votes"></div>

  <div id="hallwrap">
    <h3 class="rule" id="hall" style="display:none">Hall of prospectors &amp; patrons</h3>
    <div class="hall" id="hallbox"></div>
  </div>

  <div class="duo">
    <section class="panel" id="request">
      <h5>The request box — @@PRICE@@</h5>
      <p>Tell the workshop what to build. A paid commission opens a public GitHub
      issue, jumps the roadmap queue at the next shift, and gets a comment at every
      stage it moves — spec, build, QA, review, publish.</p>
      @@CTA@@
      <p class="fine">Honest terms: you're buying <b>priority and a serious attempt at
      the full quality bar</b> — not a guaranteed delivery. If it gets shelved, the
      issue says exactly why and what would revive it.</p>
      <p class="fine">Not ready to pay? @@SUGGEST@@ — votes decide its place in the pool.</p>
    </section>
    <section class="panel" id="install">
      <h5>Install anything shipped</h5>
      <p>Inside Claude Code:</p>
      <div class="install">/plugin marketplace add @@REPO_OR_HINT@@</div>
      <p></p>
      <div class="install">/plugin install &lt;name&gt;@@@MPNAME@@</div>
      <p class="fine">Then browse with <b>/plugin</b>. Everything shipped carries a
      semver, a changelog, a release tag, and a public paper trail: spec → test log →
      review → release, all in @@REPO_LINK@@.</p>
    </section>
  </div>

  <footer>
    <span>window: rebuilt on every loop commit · heartbeat: data.json · <a href="feed.xml">atom feed</a> · <a href="embed.html">embed the ticker</a> · <a href="badge.json">badge endpoint</a></span>
    <span>@@TITLE@@ — the workshop that works while you sleep · window v0.5</span>
    <span>generated <span id="stamp">@@STAMP@@</span> by tools/build.py</span>
  </footer>
</div>
<script>
let DATA = @@DATA@@;
const TRACKS = ["idea","spec","building","rc","published"];
const MP = @@MP@@;
const grid = document.getElementById('grid');
const empty = document.getElementById('empty');
const q = document.getElementById('q');
/*SHIFT-START*/
function nextShift(now){
  // shifts fire at minute 17 past hours 0, 8, 16 UTC (cron: 17 0,8,16 * * *)
  const HOURS = [0, 8, 16];
  const d = new Date(now.getTime());
  for (let add = 0; add <= 1; add++){
    for (const h of HOURS){
      const c = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() + add, h, 17, 0));
      if (c > now) return c;
    }
  }
  return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() + 2, 0, 17, 0));
}
/*SHIFT-END*/
function renderNextShift(){
  const el = document.getElementById('nextshift');
  if (!el) return;
  const n = nextShift(new Date());
  const ms = n - new Date();
  const h = Math.floor(ms / 3600000), m = Math.floor((ms % 3600000) / 60000);
  el.textContent = 'next shift in ~' + (h ? h + 'h ' : '') + m + 'm (' +
    String(n.getUTCHours()).padStart(2,'0') + ':17 UTC)';
}
let activeStage = null;
let activeTag = null;

function esc(s){ const d=document.createElement('span'); d.textContent=s??''; return d.innerHTML; }

function badge(e){
  if (e.always_on_tokens) {
    const v = e.verified ? ' · ✓' + esc(e.verified) : '';
    return '<span class="chip tok" title="always-on context cost, estimated">~' + esc(e.always_on_tokens) + ' tok · est' + v + '</span>';
  }
  return '<span class="chip tok" title="not yet measured by QA">unmeasured</span>';
}
/*FILTER-START*/
function filterCards(qstr, tag, entries){
  const needle = (qstr||'').trim().toLowerCase();
  return entries.filter(e => {
    if (tag && !(e.tags||[]).includes(tag)) return false;
    const hay = (e.name+' '+e.title+' '+e.one_liner+' '+(e.tags||[]).join(' ')+' '+e.category+' '+(e.components||[]).join(' ')).toLowerCase();
    return !needle || hay.includes(needle);
  });
}
/*FILTER-END*/
function card(e){
  const el = document.createElement('article');
  el.className = 'tag';
  const idx = TRACKS.indexOf(e.stage);
  const track = TRACKS.map((s,i) =>
    '<span class="punch ' + (idx >= 0 && i <= idx ? 'done' : '') + '" title="' + s + '"></span>'
  ).join('') + '<span>' + esc(e.stage) + '</span>';
  const ver = e.version ? '<span class="ver">v' + esc(e.version) + '</span>'
                        : '<span class="ver ghost">' + esc(e.stage) + '</span>';
  const comm = e.commission ? '<span class="chip comm">commission #' + esc(e.commission) + '</span>' : '';
  const tok = e.kind === 'plugin' ? badge(e) : '';
  const credit = e.prospected_by
    ? '<p class="credit">prospected by @' + esc(e.prospected_by) +
      (e.suggested_in && DATA.repo ? ' (<a href="https://github.com/' + DATA.repo + '/issues/' + esc(e.suggested_in) + '">#' + esc(e.suggested_in) + '</a>)' : '') + '</p>'
    : '';
  let install;
  if (e.kind === 'feature')
    install = '<p class="note">window experiment — hypothesis on file, verdict answers to METRICS.jsonl</p>';
  else if (e.stage === 'published')
    install = '<div class="install">/plugin install ' + esc(e.name) + '@' + esc(MP) + '</div>';
  else
    install = '<p class="note">not installable yet — watch it move down the line</p>';
  el.innerHTML =
    '<div class="top"><span class="id">' + esc(e.name) + '<em>' + esc(e.category) + '</em></span>' + ver + '</div>' +
    '<h2>' + esc(e.title) + '</h2>' +
    '<p>' + esc(e.one_liner) + '</p>' + credit +
    '<div class="track">' + track + '</div>' +
    '<div class="chips">' + comm + tok + e.components.map(c => '<span class="chip">' + esc(c) + '</span>').join('') + '</div>' +
    install +
    '<a class="prov" href="p/' + esc(e.name) + '.html">provenance — the full paper trail →</a>';
  return el;
}
function renderGrid(){
  grid.textContent = '';
  let shown = 0;
  const order = s => { const i = TRACKS.indexOf(s); return i < 0 ? -1 : i; };
  const sorted = filterCards(q.value, activeTag, [...DATA.records]).sort((a,b) => order(b.stage) - order(a.stage) || a.name.localeCompare(b.name));
  for (const e of sorted){
    if (activeStage && e.stage !== activeStage) continue;
    grid.appendChild(card(e)); shown++;
  }
  empty.style.display = shown ? 'none' : 'block';
}
function renderChips(){
  const pub = DATA.records.filter(e => e.stage === 'published');
  const tags = [...new Set(pub.flatMap(e => e.tags || []))].sort();
  document.getElementById('tagchips').innerHTML = tags.map(t =>
    '<button class="chip tagbtn' + (activeTag === t ? ' active' : '') + '" aria-pressed="' + (activeTag === t) + '" data-tag="' + esc(t) + '">' + esc(t) + '</button>'
  ).join('');
  for (const btn of document.querySelectorAll('.tagbtn'))
    btn.onclick = () => { activeTag = (activeTag === btn.dataset.tag) ? null : btn.dataset.tag; renderNextShift();
renderChips(); renderChips();
renderGrid();
if (DATA.repo) empty.innerHTML = 'Nothing on the shelf matches — <a href="https://github.com/' + DATA.repo + '/issues/new?template=idea.yml">suggest it as an idea →</a> or commission it below.'; };
}
function renderTape(){
  document.getElementById('reel').innerHTML = DATA.ticker.map(t =>
    '<span><em>' + esc(t.it) + '</em> · <b>' + esc(t.role) + '</b> — ' + esc(t.text) + '</span>'
  ).join('') || '<span>the floor is quiet — first shift pending</span>';
}
function renderStreak(){
  document.getElementById('streak').innerHTML = (DATA.streak || []).map(d => {
    const level = d.n === 0 ? '' : d.n === 1 ? 'n1' : d.n <= 3 ? 'n2' : 'n3';
    return '<span class="day ' + level + '" title="' + esc(d.d) + ' — ' + d.n + ' iteration(s)"></span>';
  }).join('');
}
function renderTheme(){
  const th = DATA.theme;
  document.getElementById('themebox').innerHTML = th && th.name
    ? '<p class="theme"><b>Theme of the month — ' + esc(th.name) + '</b> · ' + esc(th.note || '') + '</p>'
    : '<p class="theme" style="opacity:.65"><b>Theme of the month</b> · unset — three candidates go up for community 👍 vote each month</p>';
}
function renderLanes(){
  const L = DATA.roadmap;
  const laneDefs = [
    ['Commissioned — patrons first', L.commissioned],
    ['Building now', L.building],
    ['Up next (specced)', L.next],
    ['Idea pool', L.ideas],
    ['Shipped', L.shipped.slice(0,6)],
  ];
  document.getElementById('lanes').innerHTML = laneDefs.map(([title, items]) =>
    '<div class="col"><h4><b>' + esc(title) + '</b> · ' + items.length + '</h4><ul>' +
    (items.length ? items.map(r =>
      '<li>' + (r.commission ? '<span class="cnum">C#' + esc(r.commission) + '</span> ' : '') +
      esc(r.title) + '<em>' + esc(r.one_liner) + '</em></li>').join('')
      : '<li class="none">empty lane</li>') +
    '</ul></div>').join('');
}
function renderStats(){
  const S = DATA.stats || {};
  const cells = [
    [DATA.roadmap.shipped.length, 'shipped'],
    [DATA.records.filter(r => ['spec','building','rc'].includes(r.stage)).length, 'on the line'],
    [S.idea_votes_total, 'community 👍'],
    [S.stars, 'stars'],
  ];
  document.getElementById('stats').innerHTML = cells.map(([n, label]) =>
    '<div class="stat"><span class="n">' + (n === null || n === undefined ? '—' : n) +
    '</span><span class="s">' + label + '</span></div>').join('');
}
function renderFuel(){
  const F = DATA.fuel || {};
  const row = document.getElementById('fuelrow');
  const sponsor = DATA.repo ? ' · <a href="https://github.com/' + DATA.repo + '">fuel it — Sponsor on the repo</a>' : '';
  if (!F.entries) {
    row.innerHTML = '<span>FUEL — <b>$0.00</b> · ledger arms with the first CI shift' + sponsor + '</span>';
    return;
  }
  let bar = '';
  if (F.cap) {
    const pct = Math.min(100, Math.round(100 * F.mtd / F.cap));
    bar = '<span class="fuelbar"><i style="width:' + pct + '%"></i></span><span>' + pct + '% of $' + esc(F.cap) + ' cap</span>';
  }
  row.innerHTML = '<span>FUEL — <b>$' + F.mtd.toFixed(2) + '</b> this month</span>' + bar + '<span>' + sponsor + '</span>';
}
function renderAlarms(){
  const A = DATA.alarms || [];
  const el = document.getElementById('alarms');
  if (!A.length) { el.style.display = 'none'; return; }
  el.style.display = 'inline-block';
  el.innerHTML = '⚠ ' + A.length + ' ops alarm' + (A.length > 1 ? 's' : '') +
    (A[0].url ? ' — <a href="' + esc(A[0].url) + '">view</a>' : '');
}
function renderVotes(){
  const box = document.getElementById('votes');
  const suggest = DATA.repo
    ? 'https://github.com/' + DATA.repo + '/issues/new?template=idea.yml' : null;
  const rows = (DATA.votes || []);
  box.innerHTML = rows.length
    ? rows.map(v =>
        '<div class="vrow"><span class="vcount">' + v.votes + '<em>👍</em></span>' +
        '<span>' + esc(v.title) + '</span>' +
        '<a href="' + esc(v.url) + '">vote →</a></div>').join('')
    : '<p class="vnone">No open ideas yet — the pool is waiting for its first suggestion' +
      (suggest ? ' (<a href="' + suggest + '">make one, free</a>)' : '') + '.</p>';
}
function renderKits(){
  const box = document.getElementById('kitbox');
  const kits = DATA.kits || [];
  box.innerHTML = kits.length ? kits.map(k => {
    const ready = k.members.filter(m => m.published);
    const pending = k.members.filter(m => !m.published);
    const block = ready.map(m => '/plugin install ' + esc(m.name) + '@' + esc(MP)).join('\\n');
    return '<div class="kit"><h4>' + esc(k.name) + '</h4><p>' + esc(k.desc) + '</p>' +
      (ready.length ? '<div class="install">' + block + '</div>' : '<p class="pending">nothing installable yet</p>') +
      (pending.length ? '<p class="pending">+ ' + pending.map(m => esc(m.title) + ' (' + esc(m.stage) + ')').join(', ') + ' — finishing on the line</p>' : '') +
      '</div>';
  }).join('') : '<p class="vnone">Kits open once the maintainer curates the first bundle.</p>';
}
function renderHall(){
  const H = DATA.hall || {prospectors: [], patrons: []};
  const head = document.getElementById('hall');
  const box = document.getElementById('hallbox');
  if (!H.prospectors.length && !H.patrons.length) { head.style.display = 'none'; box.style.display = 'none'; return; }
  head.style.display = 'block'; box.style.display = 'block';
  box.innerHTML =
    H.prospectors.map(p =>
      '<div class="hrow"><b>@' + esc(p.login) + '</b><em>' + p.shipped + ' shipped · ' + p.total + ' formalized</em>' + (p.card ? ' <a href="' + esc(p.card) + '">card →</a>' : '') + '</div>').join('') +
    (H.patrons.length ? '<div class="hrow"><b>Patrons:</b><em>' + H.patrons.map(esc).join(' · ') + '</em></div>' : '');
}
function ago(iso){
  const s = (Date.now() - Date.parse(iso)) / 1000;
  if (!isFinite(s)) return 'live';
  if (s < 90) return 'active moments ago';
  if (s < 5400) return 'last shift ' + Math.round(s/60) + 'm ago';
  if (s < 172800) return 'last shift ' + Math.round(s/3600) + 'h ago';
  return 'last shift ' + Math.round(s/86400) + 'd ago';
}
function renderAll(){
  renderGrid(); renderTape(); renderTheme(); renderLanes(); renderStats();
  renderVotes(); renderStreak(); renderFuel(); renderAlarms(); renderKits(); renderHall();
  document.getElementById('iter').textContent = String(DATA.iteration).padStart(3,'0');
  document.getElementById('phase').textContent = DATA.phase;
  document.getElementById('lastshift').textContent = ago(DATA.generated_at);
  for (const b of document.querySelectorAll('.lanebtn'))
    { const s=b.dataset.stage; const n=DATA.counts[s]; if(n!==undefined) b.querySelector('.n').textContent = n; }
}
q.addEventListener('input', renderGrid);
for (const btn of document.querySelectorAll('.lanebtn')){
  btn.addEventListener('click', () => {
    const s = btn.dataset.stage;
    activeStage = (activeStage === s) ? null : s;
    for (const b of document.querySelectorAll('.lanebtn'))
      b.setAttribute('aria-pressed', String(b.dataset.stage === activeStage));
    renderGrid();
  });
}
renderAll();
async function checkOnAir(){
  if (!DATA.repo || !location.protocol.startsWith('http')) return;
  try {
    const r = await fetch('https://api.github.com/repos/' + DATA.repo +
      '/actions/runs?status=in_progress&per_page=5', {headers:{Accept:'application/vnd.github+json'}});
    if (!r.ok) return;
    const runs = (await r.json()).workflow_runs || [];
    const shift = runs.find(w => /shift/i.test(w.name || ''));
    if (shift) document.getElementById('lastshift').innerHTML =
      'ON AIR — <a href="' + shift.html_url + '">watch the shift</a>';
  } catch (e) { /* the age stamp already tells the truth */ }
}
checkOnAir();
setInterval(() => {
  document.getElementById('lastshift').textContent = ago(DATA.generated_at);
}, 30000);
if (location.protocol.startsWith('http')) {
  setInterval(async () => {
    try {
      const r = await fetch('data.json?t=' + Date.now(), {cache:'no-store'});
      if (r.ok) { DATA = await r.json(); renderAll(); }
    } catch (e) { /* window stays on last known state */ }
    checkOnAir();
  }, 60000);
}
</script>
</body>
</html>
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@NAME@@ — provenance</title>
<style>
  .term{background:#161310;color:#E8DCC0;padding:12px;border:2px solid #2C2820;font-size:12.5px;line-height:1.55;overflow-x:auto}
  .honestlabel{margin:6px 0;font-size:11px;letter-spacing:.06em;text-transform:uppercase;opacity:.75}
  .trust{border:2px solid #2C2820;background:#EFE6CE;padding:12px 14px;margin:14px 0}
  .trust h3{margin:0 0 8px;font-size:13px;letter-spacing:.12em;text-transform:uppercase}
  .trow{display:flex;gap:10px;padding:3px 0;border-bottom:1px dashed #C9BC9C;font-size:13px}
  .trow b{min-width:110px}
  .tnote{margin:8px 0 0;font-size:11px;opacity:.7}

  :root{--paper:#E9DFC8; --card:#F3ECDA; --ink:#2C2820; --line:#B5A683; --dim:#7E7460; --stamp:#2F5A8F}
  *{box-sizing:border-box; margin:0}
  body{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; background:var(--paper);
    color:var(--ink); font-size:14px; line-height:1.6; padding:20px}
  .sheet{max-width:820px; margin:0 auto}
  a{color:var(--stamp)}
  header{border-bottom:2px solid var(--ink); padding-bottom:10px}
  header h1{font-size:20px; letter-spacing:.1em; text-transform:uppercase}
  .meta{color:var(--dim); font-size:12px; letter-spacing:.06em; padding:6px 0}
  .track{display:flex; gap:6px; align-items:center; font-size:9px; color:var(--dim);
    letter-spacing:.1em; text-transform:uppercase; padding:8px 0}
  .punch{width:11px; height:11px; border-radius:50%; border:1.5px solid var(--ink); display:inline-block}
  .punch.done{background:var(--ink)}
  .cert{border:1px solid var(--line); background:var(--card); margin:16px 0}
  details{border-bottom:1px solid var(--line)}
  details:last-child{border-bottom:0}
  summary{cursor:pointer; padding:10px 14px; font-size:12px; letter-spacing:.14em; text-transform:uppercase}
  summary:focus-visible{outline:2px solid var(--stamp); outline-offset:-2px}
  details pre{white-space:pre-wrap; overflow-wrap:anywhere; padding:0 14px 14px; color:var(--dim); font:inherit; font-size:12.5px}
  .field{border:1px dashed var(--line); background:var(--card); padding:10px 14px; margin:10px 0; font-size:12.5px}
  .field a{display:block}
  .links{font-size:12px; padding:8px 0}
  footer{color:var(--dim); font-size:11px; border-top:2px solid var(--ink); margin-top:18px; padding-top:10px}
</style>
</head>
<body><div class="sheet">
  <p class="links"><a href="../index.html">← back to the window</a></p>
  <header><h1>@@NAME@@ — birth certificate</h1></header>
  <p class="meta">@@META@@</p>
  <div class="track">@@TRACK@@<span>@@STAGE@@</span></div>
  <p>@@ONE@@</p>
  @@TRUST@@
  @@REPORTS@@
  <div class="cert">@@SECTIONS@@</div>
  <p class="links">@@LINKS@@</p>
  <footer>Every claim above was written by the loop iteration that did the work, in
  the commit that did it — the record is append-only. Nothing here is retouched for
  the window.</footer>
</div></body></html>
"""



def trust_card(name, r):
    """Derivation-only footprint block for plugin certificates. Facts come from the
    artifact on disk; heuristics are labeled as heuristics."""
    pdir = ROOT / "plugins" / name
    if r.get("kind", "plugin") != "plugin" or not pdir.exists():
        return ""
    comps = ", ".join(r.get("components", [])) or "?"
    hooks_f = pdir / "hooks" / "hooks.json"
    if hooks_f.exists():
        try:
            hj = json.loads(hooks_f.read_text())
            lines = [f'{ev} · matcher: {m.get("matcher", "*")}'
                     for ev, arr in hj.get("hooks", {}).items() for m in arr]
            hooks = "; ".join(lines) or "declared but empty"
        except Exception:
            hooks = "hooks.json unreadable — treat as unknown"
    else:
        hooks = "none"
    hits = []
    skl = pdir / "skills"
    surf = list(pdir.rglob("*.sh")) + (list(skl.rglob("*.md")) if skl.exists() else [])
    for f in surf:
        txt = f.read_text(errors="ignore")
        for tok in ("curl ", "wget ", "fetch(", "nc "):
            if tok in txt:
                hits.append(f"{f.relative_to(pdir)} ({tok.strip()})")
    net = "none detected in executable surfaces (heuristic)" if not hits else "; ".join(sorted(set(hits)))
    cost = f'~{r["always_on_tokens"]} tok est' if r.get("always_on_tokens") else "unmeasured"
    rows = [("components", comps), ("hooks", hooks), ("network", net),
            ("always-on cost", cost),
            ("uninstall", f"/plugin uninstall {name} — removes everything the plugin installed")]
    inner = "".join(f'<div class="trow"><b>{html.escape(k)}</b><span>{html.escape(v)}</span></div>' for k, v in rows)
    return ('<div class="trust" aria-label="trust card — derived from the artifact">'
            '<h3>Trust card</h3>' + inner +
            '<p class="tnote">every line above is derived from the shipped artifact at build time — '
            'no hand-written safety claims allowed here</p></div>')


def build_pages(records, mp_name, cfg, reports):
    outdir = ROOT / "site" / "p"
    outdir.mkdir(parents=True, exist_ok=True)
    repo = cfg.get("repo") or ""
    for r in records:
        name = r.get("name", "unknown")
        idx = TRACK.index(r.get("stage")) if r.get("stage") in TRACK else -1
        track = "".join(
            f'<span class="punch {"done" if 0 <= i <= idx else ""}" title="{t}"></span>'
            for i, t in enumerate(TRACK))
        def sec(title, text):
            if title == "Example session":
                return ("<details open><summary>Example session</summary>"
                        "<p class=\"honestlabel\">authored example — a CI-recorded transcript "
                        "replaces this per charter/TESTING.md</p>"
                        f"<pre class=\"term\">{html.escape(text)}</pre></details>")
            o = ' open' if title in ('Test log','Review log','Verdict','Kill memo','Recipes') else ''
            return f"<details{o}><summary>{html.escape(title)}</summary><pre>{html.escape(text)}</pre></details>"
        sections = "".join(sec(t_, x_) for t_, x_ in extract_sections(r.get("_body", "")))
        meta_bits = [r.get("kind", "plugin"), r.get("category", "?"),
                     f"v{r['version']}" if r.get("version") not in (None, "null", "") else "unversioned",
                     f"created {r.get('created', '?')}", f"updated {r.get('updated', '?')}"]
        if r.get("tested_with"):
            meta_bits.append(f'tested with Claude Code {r["tested_with"]}')
        if r.get("always_on_tokens"):
            meta_bits.append(f"~{r['always_on_tokens']} tok est"
                             + (f" · verified {r['verified']}" if r.get("verified") else ""))
        if r.get("prospected_by"):
            meta_bits.append(f"prospected by @{r['prospected_by']}"
                             + (f" (#{r['suggested_in']})" if r.get("suggested_in") else ""))
        if r.get("patron"):
            meta_bits.append(f"patron: {r['patron']}")
        cardlink = ""
        if r.get("prospected_by"):
            import re as _re2
            safe = _re2.sub(r"[^A-Za-z0-9_-]", "", r["prospected_by"])
            if (ROOT / "site" / "card" / f"{safe}.svg").exists():
                cardlink = f' <a class="cardlink" href="../card/{safe}.svg">contributor card →</a>'
        trust = trust_card(name, r)
        plugin_reports = reports.get(name, [])
        reports_html = ""
        if plugin_reports:
            items = "".join(
                f'<a href="{html.escape(rep.get("url", "#"))}">'
                f'{html.escape(rep.get("title", "field report"))} — @{html.escape(rep.get("author", ""))}</a>'
                for rep in plugin_reports[:8])
            reports_html = f'<div class="field"><b>From the field</b>{items}</div>'
        links = []
        if r.get("stage") == "published" and r.get("kind", "plugin") == "plugin":
            links.append(f"install: <code>/plugin install {html.escape(name)}@{html.escape(mp_name)}</code>")
        if repo:
            links.append(f'<a href="https://github.com/{repo}/blob/main/{r["record_path"]}">record on GitHub</a>')
            links.append(f'<a href="https://github.com/{repo}/commits/main/{r["record_path"]}">its commit history</a>')
            if r.get("kind", "plugin") == "plugin":
                links.append(f'<a href="https://github.com/{repo}/commits/main/plugins/{name}">artifact history</a>')
            links.append(f'<a href="https://github.com/{repo}/issues/new?template=field-report.yml">file a field report</a>')
        page = (PAGE_TEMPLATE
                .replace("@@NAME@@", html.escape(r.get("title", name)))
                .replace("@@META@@", html.escape(" · ".join(meta_bits)) + cardlink)
                .replace("@@TRACK@@", track)
                .replace("@@STAGE@@", html.escape(r.get("stage", "?")))
                .replace("@@ONE@@", html.escape(r.get("one_liner", "")))
                .replace("@@REPORTS@@", reports_html)
                .replace("@@TRUST@@", trust)
                .replace("@@SECTIONS@@", sections or "<details open><summary>Record</summary><pre>(no sections yet)</pre></details>")
                .replace("@@LINKS@@", " · ".join(links) if links else "links appear once the repo is configured"))
        (outdir / f"{name}.html").write_text(page)


def build_saga(records, state, cfg):
    """Timeline from ADRs + record fates. Only what the sources say."""
    decisions = (ROOT / "state" / "DECISIONS.md").read_text()
    adrs = []
    for m in re.finditer(r"^## (ADR-\d+) — (.+?) \((i[\w-]+), ([\w-]+)\)\n(.*?)(?=^## ADR|\Z)",
                         decisions, re.M | re.S):
        ctx = re.search(r"- Context:\s*(.+)", m.group(5))
        adrs.append({"id": m.group(1), "title": m.group(2), "when": m.group(3),
                     "line": " ".join((ctx.group(1) if ctx else "").split())[:180]})
    sharpest = []
    for r in records:
        for m in re.finditer(r"Sharpest question[^:]*:?\s*(.+?)(?=\n\s*-|\n\s*REVIEW|\n##|\Z)", r.get("_body", ""), re.S):
            qtxt = " ".join(m.group(1).split())
            if qtxt:
                sharpest.append((r.get("title", r.get("name", "?")), qtxt[:220]))
    fates = []
    for r in records:
        if r.get("stage") == "published":
            fates.append((r.get("updated", ""), "SHIPPED",
                          f"{r.get('title')} " + (f"v{r['version']}" if r.get('version') not in (None, 'null', '') else "")))
        if r.get("stage") in ("deprecated", "shelved"):
            fates.append((r.get("updated", ""), r["stage"].upper(),
                          f"{r.get('title')} — reasons on its certificate"))
    fates.sort(reverse=True)
    naming = ("<li><b>Naming Ceremony</b> — " +
              (html.escape(state["name"]) if state.get("name") else "awaiting: the system has not chosen its name yet") + "</li>")
    fate_html = "".join(
        f"<li><em>{html.escape(d or 'genesis')}</em> · <b>{html.escape(kind)}</b> — {html.escape(txt)}</li>"
        for d, kind, txt in fates) or "<li>first fate pending</li>"
    adr_html = "".join(
        f"<li><em>{html.escape(a['when'])}</em> · <b>{html.escape(a['id'])}</b> — "
        f"{html.escape(a['title'])}<br><span>{html.escape(a['line'])}</span></li>"
        for a in reversed(adrs))
    wall_html = "".join(
        f"<li><b>{html.escape(t)}</b> — {html.escape(q)}</li>" for t, q in sharpest)
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>the saga</title>
<style>
 :root{{--paper:#E9DFC8; --card:#F3ECDA; --ink:#2C2820; --line:#B5A683; --dim:#7E7460; --stamp:#2F5A8F}}
 body{{font-family:ui-monospace,Menlo,Consolas,monospace; background:var(--paper); color:var(--ink);
   font-size:14px; line-height:1.6; padding:20px}}
 .sheet{{max-width:760px; margin:0 auto}} a{{color:var(--stamp)}}
 h1{{font-size:20px; letter-spacing:.12em; text-transform:uppercase; border-bottom:2px solid var(--ink); padding-bottom:8px}}
 h2{{font-size:12px; letter-spacing:.2em; text-transform:uppercase; color:var(--dim); padding:22px 0 6px; border-bottom:1px solid var(--line)}}
 ul{{list-style:none; padding:0}} li{{padding:10px 12px; border:1px solid var(--line); border-bottom:0; background:var(--card); font-size:13px}}
 li:last-child{{border-bottom:1px solid var(--line)}}
 li em{{color:var(--dim); font-style:normal; font-size:11px}} li b{{font-weight:400; letter-spacing:.08em}}
 li span{{color:var(--dim); font-size:12px}}
 footer{{color:var(--dim); font-size:11px; border-top:2px solid var(--ink); margin-top:18px; padding-top:10px}}
</style></head><body><div class="sheet">
<p><a href="index.html">← back to the window</a></p>
<h1>The saga — the workshop's own story</h1>
<h2>Ships &amp; fates</h2><ul>{naming}{fate_html}</ul>
{('<h2>Questions the line asked itself</h2><p class="wallnote">the hardest question each review recorded — argument, on the record</p><ul class="wall">' + wall_html + '</ul>') if wall_html else ''}
<h2>Charter decisions (ADRs)</h2><ul>{adr_html}</ul>
<footer>Derived entirely from state/DECISIONS.md and the records — no editorializing,
no invented milestones. The journal and git log carry the unabridged version.</footer>
</div></body></html>"""
    (ROOT / "site" / "saga.html").write_text(page)


def build_embed(ticker, cfg):
    base = (cfg.get("pages_url") or "").rstrip("/")
    home = f'<a href="{html.escape(base)}" target="_blank" rel="noopener">the living window →</a>' if base else ""
    spans = "".join(
        f"<span><em>{html.escape(t['it'])}</em> · <b>{html.escape(t['role'])}</b> — {html.escape(t['text'])}</span>"
        for t in ticker) or "<span>the floor is quiet — first shift pending</span>"
    (ROOT / "site" / "embed.html").write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>foundry ticker</title>
<style>
 body{{margin:0; font-family:ui-monospace,Menlo,Consolas,monospace; background:#E9DFC8; color:#2C2820}}
 .tape{{overflow:hidden; white-space:nowrap; padding:8px 10px; border:1px solid #B5A683}}
 .reel{{display:inline-block; padding-left:100%}}
 @media (prefers-reduced-motion:no-preference){{.reel{{animation:reel 55s linear infinite}} .tape:hover .reel{{animation-play-state:paused}}
 @keyframes reel{{to{{transform:translateX(-100%)}}}}}}
 @media (prefers-reduced-motion:reduce){{.tape{{white-space:normal}} .reel{{padding-left:0}}}}
 span{{color:#7E7460; font-size:12px; margin-right:34px}} span b{{color:#2C2820; font-weight:400}}
 span em{{color:#2F5A8F; font-style:normal}} .home{{font-size:11px; padding:4px 10px}} a{{color:#2F5A8F}}
</style></head><body>
<div class="tape"><div class="reel">{spans}</div></div>
<p class="home">{home}</p>
</body></html>""")



THEATER_TMPL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@ — live shift theater</title>
<style>
  body{background:#161310;color:#E8DCC0;font:14px/1.7 ui-monospace,Menlo,monospace;margin:0;padding:24px 16px 64px;max-width:760px;margin-inline:auto}
  h1{font-size:15px;letter-spacing:.14em;text-transform:uppercase;color:#F3ECDA}
  .sub{opacity:.7;font-size:12px}
  .entry{margin:18px 0;border-left:3px solid #B07818;padding-left:12px;min-height:1.4em}
  .entry b{color:#F3ECDA}
  .curtain{opacity:.7;font-style:italic}
  a{color:#D8A94E}
  .cursor{display:inline-block;width:8px;background:#B07818}
  @media (prefers-reduced-motion:no-preference){ .cursor{animation:blink 1s steps(1) infinite} @keyframes blink{50%{opacity:0}} }
</style></head><body>
<h1>Live shift theater</h1>
<p class="sub">the latest journal entries, replayed verbatim — the script is the ledger ·
<a href="index.html">back to the window</a></p>
<div id="stage"><p class="curtain">the floor is quiet — no journal yet; the curtain rises on the first shift</p></div>
<script>
(async () => {
  let d; try { d = await (await fetch('data.json', {cache:'no-store'})).json(); } catch(e){ return; }
  const J = d.journal || [];
  if (!J.length) return;
  const stage = document.getElementById('stage'); stage.textContent = '';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const esc = s => { const x = document.createElement('span'); x.textContent = s ?? ''; return x.innerHTML; };
  function lineFor(e){ return '<b>' + esc(e.it) + ' · ' + esc(e.role) + '</b> — ' + esc(e.text); }
  if (reduce){
    stage.innerHTML = J.map(e => '<div class="entry">' + lineFor(e) + '</div>').join('');
    return;
  }
  for (const e of J){
    const div = document.createElement('div'); div.className = 'entry';
    const full = e.it + ' · ' + e.role + ' — ' + e.text;
    const cur = '<span class="cursor">&nbsp;</span>';
    stage.appendChild(div);
    for (let i = 1; i <= full.length; i += 2){
      div.innerHTML = esc(full.slice(0, i)) + cur;
      await new Promise(r => setTimeout(r, 12));
    }
    div.innerHTML = lineFor(e);
    div.scrollIntoView({block:'end', behavior:'instant'});
    await new Promise(r => setTimeout(r, 350));
  }
})();
</script>
<footer class="sub">entries render from data.json verbatim — nothing staged, nothing invented.</footer>
</body></html>
"""


def build_theater(state, cfg):
    page = THEATER_TMPL.replace("@@TITLE@@", state.get("name") or "PRE-BRAND foundry")
    (ROOT / "site" / "theater.html").write_text(page)




def build_queue(records, cfg):
    """Sanitized public commission board. Titles come pre-sanitized from intake;
    status derives from the line — queued (no record), on the line, delivered."""
    ledger = load_json(ROOT / "state" / "commissions.json", [])
    by_comm = {str(r.get("commission")): r for r in records if r.get("commission")}
    rows = []
    for c in ledger:
        r = by_comm.get(str(c.get("issue")))
        if r is None:
            status, cls = "queued", "q"
        elif r.get("stage") == "published":
            status, cls = "delivered", "d"
        else:
            status, cls = "on the line", "b"
        cert = f' · <a href="p/{html.escape(r["name"])}.html">paper trail</a>' if r is not None else ""
        rows.append(f'<div class="qrow"><span class="qchip {cls}">{status}</span>'
                    f'<b>C#{html.escape(str(c.get("issue","?")))}</b>'
                    f'<span class="qtitle">{html.escape(c.get("title",""))}</span>'
                    f'<em>{html.escape(c.get("opened",""))}</em>{cert}</div>')
    body = ("".join(rows) if rows else
            '<p class="qopen">The counter is open — no commissions in the queue. '
            '<a href="index.html#request">Commission the machine →</a></p>')
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>The commission queue</title>
<style>body{{background:#F3ECDA;color:#2C2820;font:15px/1.7 Georgia,serif;max-width:680px;margin:0 auto;padding:28px 16px 64px}}
h1{{font-size:18px;letter-spacing:.12em;text-transform:uppercase;border-bottom:3px double #2C2820;padding-bottom:8px}}
.note{{font-size:12.5px;opacity:.75}} a{{color:#7A4A12}}
.qrow{{display:flex;gap:10px;align-items:baseline;padding:10px 0;border-bottom:1px dashed #C9BC9C;flex-wrap:wrap}}
.qtitle{{flex:1;min-width:180px}} .qrow em{{font-style:normal;font-size:11.5px;opacity:.65}}
.qchip{{font-size:11px;letter-spacing:.08em;text-transform:uppercase;border:1.5px solid #2C2820;padding:2px 8px}}
.qchip.d{{background:#2C2820;color:#F3ECDA}} .qchip.b{{background:#B07818;border-color:#B07818;color:#F3ECDA}}
.qopen{{opacity:.85}}</style></head><body>
<h1>The commission queue</h1>
<p class="note">titles only, sanitized at intake — patron text never runs the shop
(charter/SECURITY.md) · status derives from the line · <a href="index.html">back to the window</a></p>
{body}
<footer class="note">No amounts shown; handles appear only with opt-in credit. Every delivery links its paper trail.</footer>
</body></html>"""
    (ROOT / "site" / "queue.html").write_text(page)


def build_badge(records, state):
    shipped = sum(1 for r in records if r.get("stage") == "published")
    (ROOT / "site" / "badge.json").write_text(json.dumps({
        "schemaVersion": 1,
        "label": state.get("name") or "foundry",
        "message": f"{shipped} shipped · i{state.get('iteration', 0)}",
        "color": "2F5A8F",
    }, indent=1))


def build_feed(records, cfg):
    base = (cfg.get("pages_url") or "").rstrip("/")
    shipped = sorted((r for r in records if r.get("stage") == "published"),
                     key=lambda r: r.get("updated", ""), reverse=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    feed_id = base or "urn:foundry:pre-launch"
    entries = "".join(
        f"""  <entry>
    <id>{html.escape(feed_id)}/p/{html.escape(r['name'])}.html</id>
    <title>{html.escape(r.get('title', r['name']))}{' v' + html.escape(str(r['version'])) if r.get('version') not in (None, 'null', '') else ''} — shipped</title>
    <link href="{html.escape(base) + '/p/' + html.escape(r['name']) + '.html' if base else '#'}"/>
    <updated>{html.escape(r.get('updated', '1970-01-01'))}T00:00:00Z</updated>
    <summary>{html.escape(r.get('one_liner', ''))}</summary>
  </entry>
""" for r in shipped)
    (ROOT / "site" / "feed.xml").write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <id>{html.escape(feed_id)}</id>
  <title>foundry — ships</title>
  <updated>{now}</updated>
  <link href="{html.escape(base) if base else '#'}"/>
{entries}</feed>
""")


# --------------------------------------------------------------- index page --
def build_site(records, counts, state, mp_name, cfg, votes, kits, fuel_state, alarms, hall, streak):
    title = state.get("name") or "UNNAMED"

    def slim(r):
        return {
            "name": r.get("name", "?"),
            "title": r.get("title", "?"),
            "category": r.get("category", "?"),
            "stage": r.get("stage", "idea"),
            "version": None if r.get("version") in (None, "null", "") else str(r["version"]),
            "components": r.get("components", []),
            "one_liner": r.get("one_liner", ""),
            "tags": r.get("tags", []),
            "commission": r.get("commission"),
            "kind": r.get("kind", "plugin"),
            "always_on_tokens": r.get("always_on_tokens"),
            "verified": r.get("verified"),
            "prospected_by": r.get("prospected_by"),
            "suggested_in": r.get("suggested_in"),
            "patron": r.get("patron"),
        }

    by_name = {r.get("name"): r for r in records}
    kit_data = []
    for kit in kits:
        members = []
        for member in kit.get("plugins", []):
            rec = by_name.get(member, {})
            members.append({"name": member, "title": rec.get("title", member),
                            "stage": rec.get("stage", "?"),
                            "published": rec.get("stage") == "published"})
        kit_data.append({"id": kit.get("id"), "name": kit.get("name", ""),
                         "desc": kit.get("desc", ""), "members": members})

    metrics = latest_metrics()
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "iteration": int(state.get("iteration", 0)),
        "phase": state.get("phase", "?"),
        "theme": state.get("theme"),
        "counts": counts,
        "ticker": collect_journal(),
        "journal": list(reversed(collect_journal(12))),
        "records": [slim(r) for r in records],
        "stats": {k: metrics.get(k) for k in
                  ("stars", "watchers", "views_14d", "uniques_14d",
                   "idea_votes_total", "field_reports", "open_alarms")},
        "votes": votes,
        "roadmap": {k: [slim(r) for r in v] for k, v in roadmap_lanes(records).items()},
        "kits": kit_data,
        "fuel": fuel_state,
        "alarms": alarms,
        "hall": hall,
        "streak": streak,
        "repo": cfg.get("repo") or None,
    }
    (ROOT / "site" / "data.json").write_text(json.dumps(data, indent=1))

    lane_html = "".join(
        f'<button class="lanebtn" data-stage="{s}" aria-pressed="false">'
        f'<span class="n">{counts[s]}</span><span class="s">{s}</span></button>'
        for s in STAGES)
    link = cfg.get("stripe_payment_link", "")
    cta = (f'<a class="cta" href="{html.escape(link)}">Commission a plugin — {html.escape(cfg.get("price_label", "$5.99"))}</a>'
           if link else
           '<span class="cta ghost">Request box opening soon — operator: see OPERATIONS.md § 4</span>')
    repo = cfg.get("repo", "")
    repo_hint = html.escape(repo) if repo else "&lt;this repo&gt;"
    repo_link = (f'<a href="https://github.com/{html.escape(repo)}">the repo</a>' if repo else "the repo")
    suggest = (f'<a href="https://github.com/{html.escape(repo)}/issues/new?template=idea.yml">'
               f'suggest an idea, free</a>' if repo else "suggesting ideas opens with the repo (free)")

    page = (TEMPLATE
            .replace("@@TITLE@@", html.escape(title))
            .replace("@@ITER@@", str(data["iteration"]).zfill(3))
            .replace("@@PHASE@@", html.escape(data["phase"]))
            .replace("@@LANE@@", lane_html)
            .replace("@@PRICE@@", html.escape(cfg.get("price_label", "$5.99")))
            .replace("@@CTA@@", cta)
            .replace("@@REPO_OR_HINT@@", repo_hint)
            .replace("@@REPO_LINK@@", repo_link)
            .replace("@@SUGGEST@@", suggest)
            .replace("@@MPNAME@@", html.escape(mp_name))
            .replace("@@MP@@", json.dumps(mp_name))
            .replace("@@DATA@@", json.dumps(data))
            .replace("@@STAMP@@", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")))
    (ROOT / "site" / "index.html").write_text(page)
    return data


def main():
    state = json.loads((ROOT / "state" / "STATE.json").read_text())
    mp = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    cfg = json.loads((ROOT / "foundry" / "site-config.json").read_text())
    mp_name = mp.get("name", "foundry")
    records = collect_records()
    counts = build_index(records, state, mp_name)

    votes_raw = load_json(ROOT / "foundry" / "votes.json", {})
    votes = [{"number": k, "title": v.get("title", ""), "votes": v.get("votes", 0),
              "url": v.get("url", "")} for k, v in votes_raw.items()][:8]
    kits = load_json(ROOT / "foundry" / "kits.json", {}).get("kits", [])
    reports = load_json(ROOT / "foundry" / "reports.json", {})
    alarms = load_json(ROOT / "foundry" / "alarms.json", [])
    hall = collect_hall(records)
    streak = collect_streak()
    import cards as _cards
    card_paths = _cards.write_all(hall, records)
    for p_ in hall["prospectors"]:
        if p_["login"] in card_paths:
            p_["card"] = card_paths[p_["login"]]

    data = build_site(records, counts, state, mp_name, cfg, votes, kits,
                      fuel(cfg), alarms, hall, streak)
    build_pages(records, mp_name, cfg, reports)
    build_saga(records, state, cfg)
    build_embed(data["ticker"], cfg)
    build_theater(state, cfg)
    build_queue(records, cfg)
    build_badge(records, state)
    build_feed(records, cfg)
    print(f"BUILD: OK — INDEX.md + index/data/saga/embed/badge/feed + {len(records)} certificates")


if __name__ == "__main__":
    main()
