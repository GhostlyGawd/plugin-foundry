#!/usr/bin/env python3
"""build.py — regenerates foundry/INDEX.md and the whole living window:
site/index.html, data.json, p/<name>.html (birth certificates), saga.html,
embed.html, badge.json, feed.xml, and deterministic host-native plugin ZIPs.

v5 additions (ADR-009/010): token-cost badges, starter kits, idea credits, field
reports on certificates, streak heatmap, hall of prospectors & patrons, saga page,
embeds + badge endpoint, fuel gauge, ops-alarm amber state. Everything rendered is
substantiated by this repo (dark-pattern law). Stdlib only.
"""
import base64
import hashlib
import html
import json
import shutil
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "foundry" / "records"
STAGES = ["idea", "spec", "building", "rc", "published", "deprecated", "shelved"]
TRACK = ["idea", "spec", "building", "rc", "published"]


# ---------------------------------------------------------------- collectors --
from lib import parse_front_matter  # noqa: E402 — one parser, one truth (v10 #8)


def collect_records():
    out = []
    for path in sorted(RECORDS.glob("*.md")):
        text = path.read_text()
        meta, body = parse_front_matter(text)
        # Public links and generated Markdown must be platform-independent.
        # ``str(Path)`` emits backslashes on Windows, which corrupts GitHub URLs.
        meta["record_path"] = path.relative_to(ROOT).as_posix()
        meta["_body"] = body
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
    # Breakers (adversarial-qa-bounties): confirmed finds are exactly the
    # `found_by: <handle>` lines in shipped changelogs — credit derived from the
    # artifact, never hand-tallied. Empty until the first confirmed break.
    breakers = {}
    for log in sorted((ROOT / "plugins").glob("*/CHANGELOG.md")):
        for m in re.finditer(r"^\s*-?\s*found_by:\s*@?([\w-]+)", log.read_text(), re.M):
            b = breakers.setdefault(m.group(1), {"login": m.group(1), "finds": 0, "plugins": set()})
            b["finds"] += 1
            b["plugins"].add(log.parent.name)
    ranked_b = [{**b, "plugins": sorted(b["plugins"])}
                for b in sorted(breakers.values(), key=lambda e: (-e["finds"], e["login"]))]
    return {"prospectors": ranked, "patrons": sorted(set(patrons)), "breakers": ranked_b}


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
<title>@@TITLE@@ — free, tested plugins for coding agents</title>
<meta name="description" content="Free plugins for Claude Code, Codex, Gemini CLI, Cursor, and GitHub Copilot — clean commits, test nudges, environment checks, and more. Built, tested, reviewed, and shipped by an autonomous AI workshop.">
@@OG@@
<link rel="alternate" type="application/atom+xml" title="ships" href="feed.xml">
<style>
  :root{
    --paper:#EFE7D3; --card:#F7F1E1; --card2:#F1E8D2; --ink:#2B2620; --soft:#4A4235;
    --line:#C9B896; --hair:#DED0B1; --dim:#796F58; --stamp:#2F5A8F; --live:#3F7D4E;
    --amber:#B07818; --ember:#B0451B; --ember-ink:#FFF6EC; --hole:#CDBF9E;
    --sans:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
    --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
    --wrap:1140px; --shadow:0 1px 2px rgba(43,38,32,.05),0 10px 30px -16px rgba(43,38,32,.28);
  }
  @media (prefers-color-scheme: dark){:root{
    --paper:#161310; --card:#211D16; --card2:#1B1811; --ink:#ECE1C6; --soft:#C9BB99;
    --line:#463D2D; --hair:#2E281E; --dim:#9C8F73; --stamp:#8FB0DC; --live:#6FB07E;
    --amber:#D19A3D; --ember:#E07C44; --ember-ink:#1B1006; --hole:#332D23;
    --shadow:0 1px 2px rgba(0,0,0,.35),0 12px 34px -18px rgba(0,0,0,.7);
  }}
  *{box-sizing:border-box; margin:0}
  html{scroll-behavior:smooth}
  section[id]{scroll-margin-top:72px}
  body{font-family:var(--sans); background:var(--paper); color:var(--ink);
    font-size:16px; line-height:1.62; -webkit-font-smoothing:antialiased}
  a{color:var(--stamp); text-decoration:none}
  a:hover{text-decoration:underline}
  h1,h2,h3{line-height:1.18; letter-spacing:-.01em}
  .wrap{max-width:var(--wrap); margin:0 auto; padding:0 22px}
  .mono{font-family:var(--mono)}
  .skip{position:absolute; left:-9999px; top:0; background:var(--ink); color:var(--paper); padding:10px 14px; z-index:20}
  .skip:focus{left:8px; top:8px}
  :focus-visible{outline:2px solid var(--stamp); outline-offset:2px}

  /* buttons */
  .btn{display:inline-flex; align-items:center; gap:.5em; font:inherit; font-weight:600;
    background:var(--ember); color:var(--ember-ink); border:1.5px solid var(--ember);
    padding:11px 20px; border-radius:9px; cursor:pointer; text-decoration:none; white-space:nowrap}
  .btn:hover{text-decoration:none; filter:brightness(1.05)}
  .btn-lg{padding:14px 26px; font-size:16.5px}
  .btn-sm{padding:8px 15px; font-size:14px}
  .btn-ghost{background:transparent; color:var(--ink); border-color:var(--line)}
  .btn-ghost:hover{border-color:var(--ink); filter:none}

  /* header */
  header.site{position:sticky; top:0; z-index:10; background:color-mix(in srgb, var(--paper) 88%, transparent);
    backdrop-filter:saturate(1.1) blur(8px); border-bottom:1px solid var(--hair)}
  .bar{display:flex; align-items:center; gap:20px; padding:11px 22px}
  .brand{display:flex; align-items:baseline; gap:8px; color:var(--ink); font-family:var(--mono);
    letter-spacing:.12em; font-size:14px; font-weight:600}
  .brand:hover{text-decoration:none}
  .brand .mark2{color:var(--ember)}
  .brand .glyph{color:var(--ember)}
  .mainnav{display:flex; gap:20px; margin-left:auto; font-size:14.5px; font-weight:500}
  .mainnav a{color:var(--soft)}
  .mainnav a:hover{color:var(--ink)}
  .bar .btn{margin-left:4px}
  @media (max-width:820px){ .mainnav{display:none} .bar .btn{margin-left:auto} }

  /* hero */
  .hero{padding:64px 0 20px; max-width:900px}
  .eyebrow{display:flex; align-items:center; gap:10px; flex-wrap:wrap; font-size:12.5px; font-weight:600;
    letter-spacing:.1em; text-transform:uppercase; color:var(--dim); margin-bottom:18px}
  .pulse{display:inline-flex; align-items:center; gap:7px; color:var(--live)}
  .dot{width:9px; height:9px; border-radius:50%; background:var(--live)}
  @media (prefers-reduced-motion:no-preference){
    .dot{animation:beat 2.4s ease-in-out infinite}
    @keyframes beat{0%,100%{opacity:1}50%{opacity:.2}}}
  h1{font-size:clamp(30px,5vw,50px); font-weight:800; letter-spacing:-.02em}
  h1 .hot{color:var(--ember)}
  .lede{font-size:clamp(17px,2.2vw,20px); color:var(--soft); margin-top:22px; max-width:44ch}
  .lede b{color:var(--ink); font-weight:650}
  .cta-row{display:flex; flex-wrap:wrap; gap:12px; margin-top:30px}
  .proof{list-style:none; padding:0; margin:38px 0 8px; display:flex; flex-wrap:wrap; gap:14px 34px;
    border-top:1px solid var(--hair); padding-top:22px}
  .proof li{font-size:14px; color:var(--dim)}
  .proof b{display:block; font-size:26px; color:var(--ink); font-weight:800; letter-spacing:-.02em; line-height:1.1}
  .hostline{display:flex; flex-wrap:wrap; gap:8px; margin-top:24px}
  .hostpill{display:inline-flex; align-items:center; gap:7px; padding:6px 10px; border:1px solid var(--line);
    border-radius:999px; background:var(--card); color:var(--soft); font-size:12.5px; font-weight:650}
  .hostpill::before{content:""; width:6px; height:6px; border-radius:50%; background:var(--live)}

  /* bands */
  .band{padding:56px 0; border-top:1px solid var(--hair)}
  .band.alt{background:var(--card2)}
  .sec-title{font-size:clamp(23px,3.3vw,32px); font-weight:750; letter-spacing:-.02em}
  .sec-lede{color:var(--soft); font-size:17px; margin-top:10px; max-width:64ch}
  .sub-title{font-size:15px; font-weight:700; letter-spacing:.02em; text-transform:uppercase;
    color:var(--dim); margin:34px 0 12px}

  /* learn */
  .learn-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:18px; margin-top:30px}
  .explain{background:var(--card); border:1px solid var(--line); border-radius:14px; padding:22px 22px 24px; box-shadow:var(--shadow)}
  .explain .num{display:inline-grid; place-items:center; width:32px; height:32px; border-radius:9px;
    background:var(--ember); color:var(--ember-ink); font-weight:800; font-size:16px; margin-bottom:12px}
  .explain h3{font-size:18px; font-weight:700; margin-bottom:7px}
  .explain p{color:var(--soft); font-size:15px}
  .ba{margin-top:26px; background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px 22px}
  .ba-h{font-size:15px; color:var(--dim); margin-bottom:14px}
  .ba-h b{color:var(--ink)}
  .ba-row{display:flex; align-items:center; gap:16px; flex-wrap:wrap}
  .ba-col{flex:1; min-width:220px}
  .ba-col .tagl{display:block; font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:var(--dim); margin-bottom:6px}
  .ba-col code{font-family:var(--mono); font-size:13.5px; display:block; padding:10px 12px; border-radius:8px;
    background:var(--card2); border:1px solid var(--hair)}
  .ba-col.after code{border-color:var(--live); color:var(--ink)}
  .ba-col.before code{color:var(--dim)}
  .ba-note{display:block; font-size:12.5px; color:var(--dim); margin-top:7px}
  .ba-arrow{color:var(--ember); font-size:22px; font-weight:700}
  @media (max-width:560px){ .ba-arrow{transform:rotate(90deg)} }

  /* steps */
  .host-picker{margin:28px 0 20px; padding:18px; border:1px solid var(--line); border-radius:14px;
    background:var(--card); box-shadow:var(--shadow)}
  .host-label{font-family:var(--mono); font-size:11px; letter-spacing:.11em; text-transform:uppercase;
    color:var(--dim); margin-bottom:10px}
  .hostbuttons{display:flex; flex-wrap:wrap; gap:8px}
  .hostbtn{font:inherit; font-size:13.5px; font-weight:650; color:var(--soft); background:var(--paper);
    border:1px solid var(--line); border-radius:9px; padding:9px 13px; cursor:pointer}
  .hostbtn:hover{border-color:var(--ink); color:var(--ink)}
  .hostbtn[aria-pressed="true"]{background:var(--ink); border-color:var(--ink); color:var(--paper)}
  .hoststatus{font-size:13px; color:var(--dim); margin-top:10px}
  .guide-head{display:flex; align-items:flex-start; justify-content:space-between; gap:18px; flex-wrap:wrap;
    margin-top:24px}
  .guide-head h3{font-size:20px; margin-top:3px}
  .guide-head p{color:var(--soft); max-width:64ch; margin-top:6px}
  .guide-kicker{font-family:var(--mono); color:var(--ember); font-size:11px; letter-spacing:.1em; text-transform:uppercase}
  .steps{list-style:none; padding:0; margin:32px 0 0; display:grid; gap:16px}
  .steps li{display:flex; gap:18px; align-items:flex-start; background:var(--card); border:1px solid var(--line);
    border-radius:14px; padding:22px; box-shadow:var(--shadow); min-width:0}
  .step-n{flex:none; display:inline-grid; place-items:center; width:38px; height:38px; border-radius:10px;
    background:var(--ink); color:var(--paper); font-weight:800; font-size:18px; font-family:var(--mono)}
  .steps li>div{flex:1; min-width:0}
  .steps h3{font-size:18px; font-weight:700}
  .steps p{color:var(--soft); font-size:15px; margin:5px 0 10px}
  .reassure{font-size:13.5px; color:var(--dim)}
  .reassure code, .steps code{font-family:var(--mono); font-size:.92em; background:var(--card2); padding:1px 6px; border-radius:5px; border:1px solid var(--hair)}

  /* install blocks (copyable) */
  .install{font-family:var(--mono); font-size:14px; background:var(--ink); color:var(--paper);
    padding:12px 14px; border-radius:9px; overflow-x:auto; white-space:nowrap; user-select:all; cursor:copy;
    position:relative; margin:6px 0; max-width:100%}
  .install:hover{filter:brightness(1.08)}
  .install[data-copied]::after{content:"copied ✓"; position:absolute; right:10px; top:50%; transform:translateY(-50%);
    font-size:11px; letter-spacing:.06em; background:var(--live); color:#fff; padding:2px 8px; border-radius:5px}
  .install.note{cursor:text; user-select:text; white-space:normal}
  .install.note:hover{filter:none}
  .download{display:inline-flex; align-items:center; justify-content:center; min-height:36px; padding:7px 11px;
    border:1px solid var(--stamp); border-radius:8px; color:var(--stamp); font-size:12.5px; font-weight:700}
  .download:hover{background:color-mix(in srgb,var(--stamp) 9%,transparent); text-decoration:none}
  .package-row{display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap}
  .active-host{font-family:var(--mono); font-size:11px; color:var(--dim); letter-spacing:.04em}

  /* shelf tools + chips */
  .tools{margin-top:26px}
  .tools input{width:100%; font:inherit; font-size:16px; background:var(--card); border:1.5px solid var(--line);
    color:var(--ink); padding:14px 16px; border-radius:11px}
  .tools input::placeholder{color:var(--dim)}
  .chiprow{display:flex; flex-wrap:wrap; gap:8px; margin-top:16px}
  .chiprow.tagrow{margin-top:10px}
  .chip{font-family:var(--sans); font-size:12.5px; letter-spacing:.02em; border:1px solid var(--line);
    padding:4px 11px; border-radius:999px; color:var(--soft); background:var(--card)}
  button.chip{cursor:pointer; min-height:34px}
  .chip.cat.active,.chip.tagbtn.active{background:var(--ink); color:var(--paper); border-color:var(--ink)}
  .chip.comp{font-family:var(--mono); text-transform:lowercase; border-style:solid; color:var(--dim)}
  .chip.tok{font-family:var(--mono); border-style:dotted; color:var(--dim)}
  .chip.tok.stale{opacity:.5}
  .chip.comm{border-color:var(--ember); color:var(--ember)}

  /* category sections + cards */
  #grid{margin-top:26px; display:flex; flex-direction:column; gap:34px}
  .cathead{display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; padding-bottom:12px; border-bottom:2px solid var(--ink)}
  .cathead h3{font-size:19px; font-weight:750}
  .cathead span{font-size:13.5px; color:var(--dim)}
  .cardgrid{display:grid; grid-template-columns:repeat(auto-fill,minmax(310px,1fr)); gap:18px; margin-top:18px}
  .card{background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px; min-width:0;
    display:flex; flex-direction:column; gap:11px; box-shadow:var(--shadow); transition:transform .16s ease, box-shadow .16s ease}
  .card:hover{transform:translateY(-3px); box-shadow:0 2px 4px rgba(43,38,32,.06),0 18px 40px -20px rgba(43,38,32,.4)}
  .card-top{display:flex; justify-content:space-between; align-items:baseline; gap:10px}
  .card-top h3{font-size:18.5px; font-weight:750}
  .ver{font-family:var(--mono); font-size:11px; letter-spacing:.04em; border:1px solid var(--live); color:var(--live);
    padding:1px 8px; border-radius:999px; white-space:nowrap}
  .card-cat{font-size:11.5px; letter-spacing:.1em; text-transform:uppercase; color:var(--dim); margin-top:-4px}
  .card-desc{color:var(--soft); font-size:15px; flex:1}
  .chips{display:flex; flex-wrap:wrap; gap:6px}
  .card-foot{display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap; margin-top:2px}
  .card-foot .ok{font-size:12.5px; color:var(--live); font-weight:600}
  .card-foot .prov{font-size:12.5px; color:var(--stamp)}
  .credit{font-size:12px; color:var(--dim)}
  .legend{margin-top:30px; font-size:13px; color:var(--soft); background:var(--card); border:1px dashed var(--line);
    border-radius:11px; padding:14px 16px; line-height:2}
  .legend b{color:var(--ink)}
  .empty{display:none; padding:40px 4px; text-align:center; color:var(--dim); font-size:16px}

  /* kits */
  #kitbox{display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:18px; margin-top:26px}
  .kit{background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px; box-shadow:var(--shadow); min-width:0}
  .kit h4{font-size:17px; font-weight:700}
  .kit p{color:var(--soft); font-size:14.5px; margin:6px 0 12px}
  .kit .install{white-space:pre}
  .kit .pending{font-size:12.5px; color:var(--dim); margin-top:8px}

  /* trust */
  .trust-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:18px; margin-top:30px}
  .tcard{background:var(--card); border:1px solid var(--line); border-radius:14px; padding:22px; box-shadow:var(--shadow)}
  .tcard h3{font-size:16.5px; font-weight:700; color:var(--live)}
  .tcard p{color:var(--soft); font-size:14.5px; margin-top:8px}

  /* machine / telemetry */
  .theme{border:1.5px dashed var(--stamp); color:var(--stamp); padding:11px 16px; border-radius:11px;
    margin-top:26px; font-size:14px}
  .theme b{text-transform:uppercase; letter-spacing:.08em; font-size:12.5px}
  .stats{display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:24px}
  @media (max-width:560px){ .stats{grid-template-columns:repeat(2,1fr)} }
  .stat{background:var(--card); border:1px solid var(--line); border-radius:12px; padding:16px; text-align:center}
  .stat .n{display:block; font-size:30px; font-weight:800; letter-spacing:-.02em}
  .stat .s{display:block; font-size:11.5px; letter-spacing:.08em; text-transform:uppercase; color:var(--dim); margin-top:4px}
  .qstrip{font-family:var(--mono, ui-monospace, monospace); font-size:12.5px; color:var(--dim); border:1px dashed var(--line); border-radius:10px; padding:10px 14px; margin:6px 0 14px; overflow-wrap:anywhere}
  .qstrip b{color:var(--ink)}
  .replay{display:block; max-width:100%; height:auto; margin:0 0 14px; border-radius:12px}
  .dogfood{margin:0 0 14px; font-size:12.5px}
  .dfhead{color:var(--dim); margin-bottom:8px} .dfhead b{color:var(--ink)}
  .dfnote{font-size:11px}
  .dfchips{display:flex; flex-wrap:wrap; gap:6px}
  .dfchip{padding:3px 9px; border-radius:20px; font-size:11.5px; border:1px solid var(--line); cursor:help}
  .df-used{background:#2e6b34; color:#f6efe2; border-color:#2e6b34}
  .df-lightly-used{background:var(--card); color:var(--ink)}
  .df-not-yet{background:transparent; color:var(--dim); border-style:dashed}
  .tape{margin-top:22px; overflow:hidden; white-space:nowrap; padding:11px 0; border-top:1px solid var(--hair); border-bottom:1px solid var(--hair)}
  .tape .reel{display:inline-block; padding-left:100%}
  @media (prefers-reduced-motion:no-preference){
    .tape .reel{animation:reel 62s linear infinite}
    .tape:hover .reel{animation-play-state:paused}
    @keyframes reel{to{transform:translateX(-100%)}}}
  .tape span{color:var(--dim); font-size:13px; margin-right:36px; font-family:var(--mono)}
  .tape span b{color:var(--ink); font-weight:600}
  .tape span em{color:var(--stamp); font-style:normal}
  .streakwrap{display:flex; gap:16px; align-items:center; margin-top:20px; flex-wrap:wrap}
  .streak{display:grid; grid-auto-flow:column; grid-template-rows:repeat(7,11px); gap:3px}
  .day{width:11px; height:11px; border-radius:3px; background:var(--card); border:1px solid var(--hole)}
  .day.n1{background:#C9CDA4; border-color:#B5A683}
  .day.n2{background:#8FA86B; border-color:#7E9757}
  .day.n3{background:#4F7D3F; border-color:#3F6A31}
  @media (prefers-color-scheme: dark){
    .day.n1{background:#3E4A2C; border-color:#4A4232}
    .day.n2{background:#55703F; border-color:#4A5A34}
    .day.n3{background:#6FB07E; border-color:#5A9468}}
  .streaklabel{font-size:11.5px; color:var(--dim); letter-spacing:.04em; max-width:170px}
  .fuelrow{display:flex; gap:12px; align-items:center; flex-wrap:wrap; margin-top:18px; font-size:12.5px;
    letter-spacing:.04em; text-transform:uppercase; color:var(--dim)}
  .fuelrow b{color:var(--ink)}
  .fuelbar{flex:1; height:7px; background:var(--card); border:1px solid var(--line); border-radius:4px; position:relative; max-width:280px}
  .fuelbar i{position:absolute; inset:0 auto 0 0; background:var(--amber); border-radius:4px}
  .lanes{display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:16px}
  .col{border:1px solid var(--line); border-radius:12px; background:var(--card); overflow:hidden}
  .col h4{font-size:11px; letter-spacing:.1em; text-transform:uppercase; padding:11px 14px; border-bottom:1px solid var(--hair); color:var(--dim)}
  .col h4 b{color:var(--ink); font-weight:600}
  .col ul{list-style:none; padding:12px 14px; display:flex; flex-direction:column; gap:10px}
  .col li{font-size:13.5px}
  .col li em{color:var(--dim); font-style:normal; display:block; font-size:12px}
  .col li .cnum{color:var(--ember); font-size:11px; letter-spacing:.06em}
  .col .none{color:var(--dim); font-size:12.5px}
  .hall{display:none}
  .hall .hrow{display:flex; gap:14px; padding:11px 14px; border:1px solid var(--line); border-bottom:0;
    background:var(--card); font-size:13.5px; align-items:baseline}
  .hall .hrow:first-child{border-radius:12px 12px 0 0}
  .hall .hrow:last-child{border-bottom:1px solid var(--line); border-radius:0 0 12px 12px}
  .hall .hrow b{font-weight:600}
  .hall .hrow em{color:var(--dim); font-style:normal; font-size:12px}
  .more-links{margin-top:28px; display:flex; flex-wrap:wrap; gap:8px 22px; font-size:14px; font-weight:500}
  .alarms{display:none; margin-top:16px; font-size:12.5px; letter-spacing:.06em; text-transform:uppercase;
    color:var(--amber); border:1.5px solid var(--amber); border-radius:8px; padding:5px 12px}
  .nextshift{display:block; margin-top:16px; font-size:12px; color:var(--dim); font-family:var(--mono)}

  /* votes */
  .votes{display:flex; flex-direction:column; gap:10px; margin-top:24px}
  .vrow{display:grid; grid-template-columns:70px 1fr auto; gap:14px; align-items:center; padding:14px 16px;
    border:1px solid var(--line); border-radius:12px; background:var(--card); font-size:14.5px}
  .vcount{text-align:center; font-size:20px; font-weight:700}
  .vcount em{display:block; font-size:10px; font-style:normal; color:var(--dim); letter-spacing:.1em; text-transform:uppercase; font-weight:400}
  .vnone{color:var(--dim); font-size:14.5px}

  /* commission + install cols */
  .cols2{display:grid; grid-template-columns:1fr 1fr; gap:22px}
  @media (max-width:760px){ .cols2{grid-template-columns:1fr} }
  .cols2{align-items:start}
  .panel{background:var(--card); border:1px solid var(--line); border-radius:16px; padding:26px; box-shadow:var(--shadow); min-width:0}
  .panel h3{font-size:20px; font-weight:750}
  .panel-price{color:var(--ember); font-weight:700; font-size:15px; margin:6px 0 12px}
  .panel p{color:var(--soft); font-size:15px; margin-bottom:12px}
  .panel .fine{font-size:12.5px; color:var(--dim)}
  .cta.ghost, .panel .cta.ghost{display:inline-block; background:transparent; color:var(--dim);
    border:1.5px dashed var(--line); border-radius:9px; padding:11px 16px; font-size:14px}
  a.cta{display:inline-flex; align-items:center; gap:.5em; font-weight:600; background:var(--ember);
    color:var(--ember-ink); border:1.5px solid var(--ember); padding:12px 20px; border-radius:9px; text-decoration:none}
  a.cta:hover{text-decoration:none; filter:brightness(1.05)}

  /* footer */
  footer.site-foot{border-top:1px solid var(--hair); background:var(--card2); padding:40px 0; margin-top:10px}
  footer.site-foot p{font-size:14px; color:var(--soft)}
  footer.site-foot p b{color:var(--ink)}
  .foot-links{margin:10px 0; display:flex; flex-wrap:wrap; gap:6px 16px}
  .foot-fine{font-size:12px; color:var(--dim); margin-top:6px}

  @media (prefers-reduced-motion:reduce){
    .tape{white-space:normal} .tape .reel{padding-left:0}
    .card:hover{transform:none} html{scroll-behavior:auto}}
  @media (max-width:560px){
    .wrap{padding-left:16px; padding-right:16px}
    .bar{padding-left:16px; padding-right:16px}
    .brand{font-size:12px}
    .bar .btn{padding:8px 10px}
    .hero{padding-top:44px}
    .band{padding:44px 0}
    .cardgrid{grid-template-columns:1fr}
    .steps li{padding:18px; gap:12px}
    .hostbtn{flex:1 1 140px}
  }
</style>
</head>
<body>
<a class="skip" href="#shelf">Skip to the plugins</a>
<header class="site">
  <div class="bar">
    <a class="brand" href="#top"><span class="glyph">◱</span> NIGHTSHIFT <span class="mark2">FOUNDRY</span></a>
    <nav class="mainnav" aria-label="primary">
      <a href="#learn">What's this?</a>
      <a href="#shelf">Plugins</a>
      <a href="#how">Install</a>
      <a href="#machine">Watch it build</a>
    </nav>
    <a class="btn btn-sm" href="#shelf">Browse plugins</a>
  </div>
</header>
<span id="top"></span>
<main>
  <section class="wrap hero" aria-labelledby="h1">
    <p class="eyebrow"><span class="pulse"><span class="dot"></span><span id="lastshift">live</span></span> · an autonomous plugin workshop</p>
    <h1 id="h1">Small, sharp upgrades for your AI coding assistant — <span class="hot">built and tested while you sleep.</span></h1>
    <p class="lede"><b>Plugins</b> give your coding agent dependable new habits — write clean commits, catch missing tests, fix a broken dev environment. The Nightshift Foundry designs, tests, reviews, and packages them natively for the tools you already use. <b><span id="hero-count">10</span> plugins, all free, across five hosts.</b></p>
    <div class="cta-row">
      <a class="btn btn-lg" href="#shelf">Browse the plugins →</a>
      <a class="btn btn-ghost btn-lg" href="#learn">New here? Start with the basics</a>
    </div>
    <ul class="proof">
      <li><b id="proof-count">10</b> free plugins on the shelf</li>
      <li><b>3-tier</b> QA before anything ships</li>
      <li><b>5</b> native host packages per plugin</li>
      <li><b>$0</b> — open-source, remove anytime</li>
    </ul>
    <div class="hostline" aria-label="Supported coding-agent hosts">
      <span class="hostpill">Codex</span><span class="hostpill">Claude Code</span><span class="hostpill">Gemini CLI</span><span class="hostpill">Cursor</span><span class="hostpill">GitHub Copilot</span>
    </div>
  </section>

  <section id="learn" class="band">
    <div class="wrap">
      <h2 class="sec-title">New here? Here's the whole idea in 30 seconds</h2>
      <div class="learn-grid">
        <article class="explain"><span class="num">1</span><h3>What's a coding agent?</h3><p>Codex, Claude Code, Gemini CLI, Cursor, and Copilot help you read, write, fix, and ship code from your terminal or editor.</p></article>
        <article class="explain"><span class="num">2</span><h3>What's a plugin?</h3><p>A small add-on that teaches an agent one focused habit — a <b>skill</b> it can use, or a safe <b>hook</b> that runs at the right moment. One plugin, one job.</p></article>
        <article class="explain"><span class="num">3</span><h3>Why the Foundry?</h3><p>Every plugin here is scoped to a single job, kept tiny, tested against its own spec, and reviewed for safety before it reaches you. Free to install, easy to remove.</p></article>
      </div>
      <div class="ba">
        <p class="ba-h">A quick example — the <b>Commit Craft</b> plugin:</p>
        <div class="ba-row">
          <div class="ba-col before"><span class="tagl">Without it</span><code>git commit -m "fixed stuff"</code></div>
          <div class="ba-arrow" aria-hidden="true">→</div>
          <div class="ba-col after"><span class="tagl">With it installed</span><code>feat(auth): refresh token on 401</code><span class="ba-note">written from your staged diff, and the format is guarded automatically</span></div>
        </div>
      </div>
    </div>
  </section>

  <section id="how" class="band alt">
    <div class="wrap">
      <h2 class="sec-title">Pick your host. Get the native package.</h2>
      <p class="sec-lede">The behavior is shared; the manifest and lifecycle hooks are packaged for each host. Choose yours and every install control on this page updates with it.</p>
      <div class="host-picker">
        <p class="host-label">Your coding agent</p>
        <div class="hostbuttons" id="hostbuttons" role="group" aria-label="Choose a coding-agent host"></div>
        <p class="hoststatus" id="hoststatus" aria-live="polite"></p>
      </div>
      <div class="guide-head">
        <div><span class="guide-kicker">Native install guide</span><h3 id="host-title"></h3><p id="host-desc"></p></div>
        <a class="download" href="@@COMPAT_URL@@" id="compat-guide">Full compatibility guide →</a>
      </div>
      <ol class="steps" id="hoststeps"></ol>
    </div>
  </section>

  <section id="shelf" class="band">
    <div class="wrap">
      <h2 class="sec-title">The shelf — <span id="shelf-count">10</span> free plugins</h2>
      <p class="sec-lede">Search by name, or just describe what you're working on — the clerk points you to the right one. It never invents a plugin that isn't there.</p>
      <div class="tools">
        <input id="q" type="search" placeholder="Describe your task — e.g. “write better commit messages” or “my dev env is broken”" aria-label="Search plugins or describe your task">
      </div>
      <div id="clerkout" aria-live="polite"></div>
      <div class="chiprow" id="catchips" role="group" aria-label="filter by category"></div>
      <div class="chiprow tagrow" id="tagchips" role="group" aria-label="filter by tag"></div>
      <div id="grid"></div>
      <p class="empty" id="empty"></p>
      <p class="legend"><b>What the labels mean:</b> <span class="chip comp">skill</span> a capability your agent can use · <span class="chip comp">hook</span> a safe check that runs at a set moment · <span class="chip comp">agent</span> a focused sub-assistant · <span class="chip tok">~tok</span> the always-on context it costs (smaller is better) · <span class="chip comp" style="border-color:var(--live);color:var(--live)">✓ v1</span> tested &amp; reviewed, shipped.</p>
    </div>
  </section>

  <section id="kits" class="band alt">
    <div class="wrap">
      <h2 class="sec-title">Not sure where to start? Grab a kit</h2>
      <p class="sec-lede">Curated bundles for a job — paste each line in turn.</p>
      <div id="kitbox"></div>
    </div>
  </section>

  <section id="trust" class="band">
    <div class="wrap">
      <h2 class="sec-title">Why you can trust what installs</h2>
      <p class="sec-lede">A plugin is a guest in your session — it costs context and can run code on your machine. So the workshop holds every one to a hard bar before it ships.</p>
      <div class="trust-grid">
        <article class="tcard"><h3>✓ Tested before it ships</h3><p>Every plugin passes a three-tier check — structure, load, and its own behavioral spec run by a skeptic — before it's ever published.</p></article>
        <article class="tcard"><h3>✓ Reviewed line by line</h3><p>A reviewer reads every prompt and every hook for safety and clarity. Nothing ships on a rubber stamp.</p></article>
        <article class="tcard"><h3>✓ Hooks behave like guests</h3><p>Code that runs on your machine is held to strict rules: narrow triggers, never destructive, fails safe, never bricks your session.</p></article>
        <article class="tcard"><h3>✓ No telemetry or borrowed credentials</h3><p>The site uses no analytics, cookies, remote fonts, or third-party scripts. Plugin hooks make no network calls and never receive Foundry service credentials.</p></article>
        <article class="tcard"><h3>✓ A public paper trail</h3><p>Every plugin has a birth certificate — its spec, test log, review, and full version history, all in the open. <a id="trail-link" href="p/commit-craft.html">See one →</a></p></article>
      </div>
    </div>
  </section>

  <section id="machine" class="band alt">
    <div class="wrap">
      <h2 class="sec-title">Under the hood — the workshop, live</h2>
      <p class="sec-lede">Here's the part that's a little wild: <b>no human is on the line.</b> A PR-gated Codex workflow pitches, builds, tests, reviews, and publishes every plugin above — and this page updates when a green change lands.</p>
      <p class="qstrip" id="qstrip" aria-label="the running quality counter — every number substantiated by this repo"></p>
      <div class="dogfood" id="dogfood" aria-label="the dogfood report card — the factory grades its own use of what it ships"></div>
      <img class="replay" src="replay.svg" loading="lazy" width="720" height="200"
           alt="Replay of real iterations i89–i93: the review gate blocks a bad starter-kits build, the fix lands with a pinned regression, v0.1.0 ships." />
      <div id="themebox"></div>
      <div class="stats" id="stats"></div>
      <div class="tape" aria-label="latest shop-floor journal entries"><div class="reel" id="reel"></div></div>
      <div class="streakwrap" aria-label="iterations per day, last 12 weeks — real journal entries only">
        <div class="streak" id="streak"></div>
        <span class="streaklabel">shifts, last 12 weeks — quiet days stay blank</span>
      </div>
      <div class="fuelrow" id="fuelrow" aria-label="the fuel gauge — real ledger spend"></div>
      <h3 class="sub-title">The line, in lanes</h3>
      <div class="lanes" id="lanes"></div>
      <div id="hallwrap"><h3 class="sub-title" id="hall" style="display:none">Hall of prospectors &amp; patrons</h3><div class="hall" id="hallbox"></div></div>
      <div id="verifiedwrap"><h3 class="sub-title" id="verified" style="display:none">Verified externals — the doctor, run in their CI</h3><div class="hall" id="verifiedbox"></div></div>
      <div id="networkwrap"><h3 class="sub-title" id="network" style="display:none">Sister foundries — the network</h3><div class="hall" id="networkbox"></div></div>
      <p class="more-links"><a href="saga.html">The full saga →</a><a href="theater.html">Watch a live shift →</a><a href="desk.html">The owner's desk →</a><a href="almanac/index.html">Weekly shipnotes →</a><a href="queue.html">Commission queue →</a><a id="relchip" href="#" style="display:none">Releases →</a><a href="feed.xml">Follow the shelf (Atom) →</a></p>
      <span class="alarms" id="alarms"></span>
      <span class="nextshift" id="nextshift"></span>
    </div>
  </section>

  <section id="vote" class="band">
    <div class="wrap">
      <h2 class="sec-title">Shape what gets built next</h2>
      <p class="sec-lede">Vote an idea up with a 👍 on GitHub — counts are read live each shift, so the workshop can't inflate them. Or commission a build to jump the queue.</p>
      <div class="votes" id="votes"></div>
    </div>
  </section>

  <section id="request" class="band alt">
    <div class="wrap cols2">
      <section class="panel">
        <h3>Can't find the tool you need?</h3>
        <p class="panel-price">Commission the workshop — @@PRICE@@</p>
        <p>Tell it what to build. A commission opens a public GitHub issue, jumps the roadmap queue at the next shift, and gets a comment at every stage it moves — spec, build, QA, review, publish.</p>
        @@CTA@@
        <p class="fine">Honest terms: you're buying <b>priority and a serious attempt at the full quality bar</b> — not a guaranteed delivery. If it gets shelved, the issue says exactly why and what would revive it.</p>
        <p class="fine">Not ready to pay? @@SUGGEST@@ — votes decide its place in the pool.</p>
      </section>
      <section class="panel" id="install">
        <h3>Install anything on the shelf</h3>
        <p id="footer-host-copy">Choose a host above to get its native install path.</p>
        <div id="footer-install"></div>
        <p class="fine">Every host package carries a semver, SHA-256 digest, changelog, and public paper trail in @@REPO_LINK@@. The host choice stays only in this open page.</p>
      </section>
    </div>
  </section>
</main>
<footer class="site-foot">
  <div class="wrap">
    <p><b>@@TITLE@@</b> — the workshop that works while you sleep.</p>
    <p class="foot-links"><a href="#shelf">Plugins</a> · <a href="#how">Install</a> · <a href="#trust">Trust</a> · <a href="privacy.html">Privacy</a> · <a href="@@SECURITY_URL@@">Security</a> · <a href="saga.html">Saga</a> · <a href="feed.xml">Atom feed</a> · <a href="embed.html">Embed the ticker</a> · <a href="badge.json">Badge endpoint</a></p>
    <p class="foot-fine">Independent community project; product names belong to their respective owners. No analytics or tracking. · Generated <span id="stamp">@@STAMP@@</span> — this page rebuilds every time a green change ships.</p>
  </div>
</footer>
<script>
let DATA = @@DATA@@;
const MP = @@MP@@;
const grid = document.getElementById('grid');
const empty = document.getElementById('empty');
const q = document.getElementById('q');
let activeTag = null;
let activeCat = null;
let activeHost = 'codex';
const HOSTS = [
  {id:'codex', name:'Codex', detail:'Add the Foundry marketplace, then choose the plugin in the ChatGPT desktop app Plugins Directory.'},
  {id:'claude-code', name:'Claude Code', detail:'Install directly from the Foundry marketplace with Claude Code slash commands.'},
  {id:'gemini-cli', name:'Gemini CLI', detail:'Download the native extension ZIP, extract it, and install the local directory with Gemini CLI.'},
  {id:'cursor', name:'Cursor', detail:'Download the native ZIP and copy the extracted plugin into Cursor’s local plugin directory.'},
  {id:'github-copilot', name:'GitHub Copilot', detail:'Add the Foundry marketplace and install directly with Copilot CLI.'}
];
/*SHIFT-START*/
// shift schedule derived from .github/workflows/run-shift.yml cron at build time
const SHIFT_MIN = @@SHIFT_MIN@@;
const SHIFT_HOURS = @@SHIFT_HOURS@@;
function nextShift(now){
  const d = new Date(now.getTime());
  for (let add = 0; add <= 1; add++){
    for (const h of SHIFT_HOURS){
      const c = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() + add, h, SHIFT_MIN, 0));
      if (c > now) return c;
    }
  }
  const h0 = SHIFT_HOURS.length ? SHIFT_HOURS[0] : 0;
  return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() + 2, h0, SHIFT_MIN, 0));
}
/*SHIFT-END*/
function renderNextShift(){
  const el = document.getElementById('nextshift');
  if (!el) return;
  const n = nextShift(new Date());
  const ms = n - new Date();
  const h = Math.floor(ms / 3600000), m = Math.floor((ms % 3600000) / 60000);
  el.textContent = 'next shift in ~' + (h ? h + 'h ' : '') + m + 'm (' +
    String(n.getUTCHours()).padStart(2,'0') + ':' + String(SHIFT_MIN).padStart(2,'0') + ' UTC)';
}

function esc(s){ const d=document.createElement('span'); d.textContent=s??''; return d.innerHTML; }

function currentHost(){ return HOSTS.find(h => h.id === activeHost) || HOSTS[0]; }
function packageFor(name){
  const plugin = (DATA.packages || []).find(p => p.name === name);
  return plugin && plugin.packages ? plugin.packages[activeHost] : null;
}
function nativeDownload(name){
  const pkg = packageFor(name);
  if (!pkg) return '';
  const label = 'Download ' + currentHost().name + ' ZIP';
  return '<a class="download" download href="downloads/' + esc(pkg.file) + '" aria-label="' +
    esc(label + ' for ' + name) + '">' + esc(label) + '</a>';
}
function hostAction(name){
  if (activeHost === 'claude-code') return {text:'/plugin install ' + name + '@' + MP, note:false};
  if (activeHost === 'codex') return {text:'Plugins Directory → Nightshift Foundry → ' + name, note:true};
  if (activeHost === 'gemini-cli') return {text:'gemini extensions install ./' + name, note:false};
  if (activeHost === 'cursor') return {text:'Copy extracted ' + name + ' to %USERPROFILE%/.cursor/plugins/local/' + name, note:true};
  return {text:'copilot plugin install ' + name + '@' + MP, note:false};
}
function multiActionNote(){
  if (activeHost === 'claude-code' || activeHost === 'github-copilot') return 'run each command separately';
  if (activeHost === 'codex') return 'choose each plugin separately in the Plugins Directory';
  if (activeHost === 'gemini-cli') return 'install each extracted plugin directory separately';
  return 'copy each extracted plugin directory separately';
}
function hostSteps(){
  const repo = DATA.repo || '<owner/repository>';
  if (activeHost === 'claude-code') return [
    {title:'Add the marketplace once', text:'This registers the Foundry source.', cmd:'/plugin marketplace add ' + repo},
    {title:'Install the plugin you want', text:'Swap in any shelf name.', cmd:'/plugin install commit-craft@' + MP},
    {title:'Work normally', text:'Claude Code loads the plugin under its normal permission controls. Inspect or remove it whenever you like.', cmd:'/plugin uninstall commit-craft'}
  ];
  if (activeHost === 'codex') return [
    {title:'Add the marketplace once', text:'This registers the repo-native Codex catalog.', cmd:'codex plugin marketplace add ' + repo},
    {title:'Choose the plugin', text:'Open the ChatGPT desktop app Plugins Directory, select Nightshift Foundry, then choose Commit Craft.', cmd:'Plugins Directory → Nightshift Foundry → commit-craft', note:true},
    {title:'Review and enable', text:'Codex caches the selected plugin and applies its normal plugin and hook trust controls.', download:'commit-craft'}
  ];
  if (activeHost === 'gemini-cli') return [
    {title:'Download the native package', text:'Each ZIP contains Gemini’s manifest and lifecycle-event names.', download:'commit-craft'},
    {title:'Extract, then install', text:'Run this from the directory that contains the extracted plugin folder.', cmd:'gemini extensions install ./commit-craft'},
    {title:'Update deliberately', text:'Replace the local package with a newer download, then ask Gemini to update it.', cmd:'gemini extensions update commit-craft'}
  ];
  if (activeHost === 'cursor') return [
    {title:'Download the native package', text:'Each ZIP contains Cursor’s manifest and hook mapping.', download:'commit-craft'},
    {title:'Copy it to local plugins', text:'Extract first. On macOS or Linux use ~/.cursor/plugins/local instead.', cmd:'Copy commit-craft to %USERPROFILE%/.cursor/plugins/local/commit-craft', note:true},
    {title:'Reload Cursor', text:'Run Developer: Reload Window, then review it under Settings → Plugins → Installed.', cmd:'Developer: Reload Window', note:true}
  ];
  return [
    {title:'Add the marketplace once', text:'This registers the Foundry marketplace with Copilot CLI.', cmd:'copilot plugin marketplace add ' + repo},
    {title:'Install the plugin you want', text:'Swap in any shelf name.', cmd:'copilot plugin install commit-craft@' + MP},
    {title:'Work normally', text:'Copilot loads the native plugin under its own trust controls.', download:'commit-craft'}
  ];
}
function renderHostButtons(){
  const box = document.getElementById('hostbuttons');
  box.innerHTML = HOSTS.map(h => '<button class="hostbtn" data-host="' + h.id + '" aria-pressed="' +
    (h.id === activeHost) + '">' + esc(h.name) + '</button>').join('');
  for (const btn of box.querySelectorAll('.hostbtn')) btn.onclick = () => {
    activeHost = btn.dataset.host;
    renderHostExperience(); renderGrid(); renderClerk(); renderKits();
  };
}
function renderHostExperience(){
  const host = currentHost();
  renderHostButtons();
  document.body.dataset.host = host.id;
  document.getElementById('host-title').textContent = host.name;
  document.getElementById('host-desc').textContent = host.detail;
  document.getElementById('hoststatus').textContent = 'Showing ' + host.name + ' install paths and native downloads.';
  document.getElementById('hoststeps').innerHTML = hostSteps().map((step, i) =>
    '<li><span class="step-n">' + (i + 1) + '</span><div><h3>' + esc(step.title) + '</h3><p>' + esc(step.text) + '</p>' +
    (step.cmd ? '<div class="install' + (step.note ? ' note' : '') + '">' + esc(step.cmd) + '</div>' : '') +
    (step.download ? nativeDownload(step.download) : '') + '</div></li>').join('');
  const footer = document.getElementById('footer-install');
  const action = hostAction('<name>');
  footer.innerHTML = '<div class="install' + (action.note ? ' note' : '') + '">' + esc(action.text) + '</div>';
  document.getElementById('footer-host-copy').textContent = 'For ' + host.name + ':';
}

function badge(e){
  if (e.always_on_tokens) {
    const stale = e.verified && (Date.now() - Date.parse(e.verified)) > 60*86400000;
    const v = e.verified ? ' · ✓' + esc(e.verified) : '';
    const t = 'always-on context cost, estimated' + (stale ? ' — verification older than 60 days' : '');
    return '<span class="chip tok' + (stale ? ' stale' : '') + '" title="' + t + '">~' + esc(e.always_on_tokens) + ' tok · est' + v + '</span>';
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
function pubPlugins(){ return DATA.records.filter(e => e.stage === 'published' && e.kind === 'plugin'); }
function catInfo(id){ return (DATA.categories||[]).find(c => c.id === id) || {}; }
function catName(id){ return catInfo(id).name || id; }
function catOrder(){ return (DATA.categories||[]).map(c => c.id); }

function card(e){
  const el = document.createElement('article');
  el.className = 'card';
  const ver = e.version ? '<span class="ver">✓ v' + esc(e.version) + '</span>' : '';
  const comps = (e.components||[]).map(c => '<span class="chip comp">' + esc(c) + '</span>').join('');
  const credit = e.prospected_by
    ? '<p class="credit">idea by @' + esc(e.prospected_by) +
      (e.suggested_in && DATA.repo ? ' (<a href="https://github.com/' + DATA.repo + '/issues/' + esc(e.suggested_in) + '">#' + esc(e.suggested_in) + '</a>)' : '') + '</p>'
    : '';
  const action = hostAction(e.name);
  el.innerHTML =
    '<div class="card-top"><h3>' + esc(e.title) + '</h3>' + ver + '</div>' +
    '<p class="card-cat">' + esc(catName(e.category)) + '</p>' +
    '<p class="card-desc">' + esc(e.one_liner) + '</p>' +
    '<div class="chips">' + comps + badge(e) + '</div>' +
    '<div class="package-row"><span class="active-host">for ' + esc(currentHost().name) + '</span>' + nativeDownload(e.name) + '</div>' +
    '<div class="install' + (action.note ? ' note' : '') + '">' + esc(action.text) + '</div>' +
    '<div class="card-foot"><span class="ok">✓ tested &amp; reviewed</span>' +
    '<a class="prov" href="p/' + esc(e.name) + '.html">how it was built →</a></div>' + credit;
  return el;
}
function renderGrid(){
  grid.textContent = '';
  let base = pubPlugins();
  if (activeCat) base = base.filter(e => e.category === activeCat);
  const list = filterCards(q.value, activeTag, base);
  if (!list.length){
    empty.style.display = 'block';
    empty.innerHTML = DATA.repo
      ? 'No plugin on the shelf matches that yet — <a href="https://github.com/' + DATA.repo + '/issues/new?template=idea.yml">suggest it as an idea (free)</a>, or commission it below.'
      : 'Nothing matches — clear the filter and try again.';
    return;
  }
  empty.style.display = 'none';
  const ord = catOrder();
  const cats = [...new Set(list.map(e => e.category))].sort((a,b) => ord.indexOf(a) - ord.indexOf(b));
  for (const cat of cats){
    const items = list.filter(e => e.category === cat).sort((a,b) => a.name.localeCompare(b.name));
    const sec = document.createElement('div'); sec.className = 'catsec';
    sec.innerHTML = '<div class="cathead"><h3>' + esc(catName(cat)) + '</h3><span>' + esc(catInfo(cat).desc || '') + '</span></div>';
    const g = document.createElement('div'); g.className = 'cardgrid';
    for (const e of items) g.appendChild(card(e));
    sec.appendChild(g); grid.appendChild(sec);
  }
}
function renderCatChips(){
  const present = [...new Set(pubPlugins().map(e => e.category))];
  const ord = catOrder();
  present.sort((a,b) => ord.indexOf(a) - ord.indexOf(b));
  const box = document.getElementById('catchips');
  box.innerHTML =
    '<button class="chip cat' + (activeCat === null ? ' active' : '') + '" aria-pressed="' + (activeCat === null) + '" data-cat="">All</button>' +
    present.map(c => '<button class="chip cat' + (activeCat === c ? ' active' : '') + '" aria-pressed="' + (activeCat === c) + '" data-cat="' + esc(c) + '">' + esc(catName(c)) + '</button>').join('');
  for (const btn of box.querySelectorAll('.cat'))
    btn.onclick = () => { activeCat = btn.dataset.cat || null; renderCatChips(); renderGrid(); };
}
function renderTagChips(){
  const tags = [...new Set(pubPlugins().flatMap(e => e.tags || []))].sort();
  const box = document.getElementById('tagchips');
  box.innerHTML = tags.map(t =>
    '<button class="chip tagbtn' + (activeTag === t ? ' active' : '') + '" aria-pressed="' + (activeTag === t) + '" data-tag="' + esc(t) + '">' + esc(t) + '</button>'
  ).join('');
  for (const btn of box.querySelectorAll('.tagbtn'))
    btn.onclick = () => { activeTag = (activeTag === btn.dataset.tag) ? null : btn.dataset.tag; renderTagChips(); renderGrid(); };
}
/* the front desk — the night-clerk's matching for visitors who haven't installed
   anything yet. Task-shaped queries (2+ words) get the clerk's best-3 answer above
   the cards. Published only, nothing invented (same honesty rules as the shelf). */
function renderClerk(){
  const box = document.getElementById('clerkout');
  const raw = (q.value || '').toLowerCase().trim();
  const terms = raw.split(/[^a-z0-9]+/).filter(t => t.length > 2);
  if (terms.length < 2){ box.innerHTML = ''; return; }
  const score = hay => terms.reduce((s, t) => s + (hay.includes(t) ? 1 : 0), 0);
  const hits = DATA.records
    .filter(e => e.stage === 'published' && e.kind === 'plugin')
    .map(e => [score((e.name + ' ' + e.title + ' ' + e.one_liner + ' ' + (e.tags || []).join(' ')).toLowerCase()), e])
    .filter(([s]) => s > 0)
    .sort((a, b) => b[0] - a[0])
    .slice(0, 3);
  const kitHit = (DATA.kits || [])
    .map(k => [score((k.name + ' ' + k.desc).toLowerCase()), k])
    .filter(([s, k]) => s > 0 && k.members.some(m => m.published))
    .sort((a, b) => b[0] - a[0])[0];
  if (!hits.length && !kitHit){
    const idea = DATA.repo ? ' — <a href="https://github.com/' + DATA.repo + '/issues/new?template=idea.yml">suggest it as an idea, free</a>' : '';
    box.innerHTML = '<p class="vnone">Nothing on the shelf fits that task yet' + idea + '. The clerk never invents a plugin.</p>';
    return;
  }
  let out = '<p class="vnone">The front desk suggests —</p>' + hits.map(([s, e]) =>
    { const action = hostAction(e.name); return '<div class="kit"><h4>' + esc(e.title) + '</h4><p>' + esc(e.one_liner) + '</p>' +
    '<div class="package-row"><span class="active-host">for ' + esc(currentHost().name) + '</span>' + nativeDownload(e.name) + '</div>' +
    '<div class="install' + (action.note ? ' note' : '') + '">' + esc(action.text) + '</div></div>'; }).join('');
  if (kitHit){
    const k = kitHit[1];
    const ready = k.members.filter(m => m.published);
    const block = ready.map(m => esc(hostAction(m.name).text)).join('\\n');
    out += '<div class="kit"><h4>' + esc(k.name) + ' — the whole kit</h4><p>' + esc(k.desc) + '</p><div class="install' +
      (hostAction(ready[0].name).note ? ' note' : '') + '">' + block + '</div>' +
      (ready.length > 1 ? '<p class="pending">' + esc(multiActionNote()) + '</p>' : '') + '</div>';
  }
  box.innerHTML = out;
}
function renderKits(){
  const box = document.getElementById('kitbox');
  const kits = DATA.kits || [];
  box.innerHTML = kits.length ? kits.map(k => {
    const ready = k.members.filter(m => m.published);
    const pending = k.members.filter(m => !m.published);
    const block = ready.map(m => esc(hostAction(m.name).text)).join('\\n');
    return '<div class="kit"><h4>' + esc(k.name) + '</h4><p>' + esc(k.desc) + '</p>' +
      (ready.length ? '<div class="package-row"><span class="active-host">for ' + esc(currentHost().name) + '</span></div><div class="install' +
        (hostAction(ready[0].name).note ? ' note' : '') + '">' + block + '</div>' +
        (ready.length > 1 ? '<p class="pending">' + esc(multiActionNote()) + '</p>' : '')
        : '<p class="pending">nothing installable yet</p>') +
      (pending.length ? '<p class="pending">+ ' + pending.map(m => esc(m.title) + ' (' + esc(m.stage) + ')').join(', ') + ' — finishing on the line</p>' : '') +
      '</div>';
  }).join('') : '<p class="vnone">Kits open once the maintainer curates the first bundle.</p>';
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
    ? '<p class="theme"><b>This month — ' + esc(th.name) + '</b> · ' + esc(th.note || '') + '</p>'
    : '';
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
  // Feature the true numbers that best convey the product — every published plugin
  // cleared TEST VERDICT: pass + REVIEW: approved (validator law), so "100% tested
  // & reviewed" is substantiated, not marketing. No fabricated or inflated counts.
  const cats = new Set(pubPlugins().map(e => e.category)).size;
  // GAP-A: the quality number rides the hero — first-try QA is computed from
  // the records' own Test logs (site/quality.json is the badge endpoint).
  const Q = DATA.quality || {};
  const cells = [
    [pubPlugins().length, 'free plugins'],
    [DATA.iteration, 'autonomous shifts'],
    [Q.qa_first_try_pct === null || Q.qa_first_try_pct === undefined ? '—' : Q.qa_first_try_pct + '%', 'passed QA first try'],
    [cats, 'categories'],
    ['100%', 'tested &amp; reviewed'],
  ];
  document.getElementById('stats').innerHTML = cells.map(([n, label]) =>
    '<div class="stat"><span class="n">' + (n === null || n === undefined ? '—' : n) +
    '</span><span class="s">' + label + '</span></div>').join('');
}
function renderDogfood(){
  // P1.4: the factory grades its own dogfooding, honestly — 'not-yet' shown.
  const D = DATA.dogfood || {}, el = document.getElementById('dogfood');
  if (!el || !D.cards) return;
  const s = D.summary || {};
  const chip = (c) => '<span class="dfchip df-' + c.grade + '" title="'
    + esc((c.evidence || []).join('; ') || 'no evidence yet') + '">'
    + esc(c.plugin) + '</span>';
  el.innerHTML = '<div class="dfhead">Dogfood report card — '
    + '<b>' + (s.used || 0) + '</b> used · <b>' + (s['lightly-used'] || 0)
    + '</b> lightly · <b>' + (s['not-yet'] || 0) + '</b> not yet '
    + '<span class="dfnote">(the factory grades its own use of what it ships — hover a chip for the evidence)</span></div>'
    + '<div class="dfchips">' + D.cards.map(chip).join('') + '</div>';
}
function renderQuality(){
  // GAP-A2: the running counter — the return engine ("what did it ship today?").
  // Every figure comes from DATA.quality (records/journal/ledger — substantiated).
  const Q = DATA.quality || {}, el = document.getElementById('qstrip');
  if (!el) return;
  const pubs = pubPlugins().slice().sort((a, b) => String(b.updated).localeCompare(String(a.updated)));
  const latest = pubs[0];
  const bits = [
    '<b>' + (Q.plugins_shipped ?? '—') + '</b> plugins shipped',
    (Q.qa_first_try_pct ?? '—') + '% passed QA first try',
    '<b>' + (Q.bounces_total ?? '—') + '</b> builds bounced & fixed in public',
    (Q.iterations ?? '—') + ' iterations',
    '$' + (Q.api_spend_usd ?? 0).toFixed(2) + ' API spend',
  ];
  el.innerHTML = bits.join(' · ') +
    (latest ? ' — latest ship: <b>' + esc(latest.title) + '</b> v' + esc(latest.version || '?') +
              ' (' + esc(latest.updated || '') + ')' : '');
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
function renderVerified(){
  const V = DATA.verified || [];
  const head = document.getElementById('verified');
  const box = document.getElementById('verifiedbox');
  if (!V.length) { head.style.display = 'none'; box.style.display = 'none'; return; }
  head.style.display = 'block'; box.style.display = 'block';
  box.innerHTML = V.map(v => {
    const slug = (v.repo || '').replace(/[^A-Za-z0-9_-]/g, '-');
    const badge = (DATA.pages_url && v.run_url)
      ? '<div class="install">[![verified by the foundry](' + esc(DATA.pages_url) + '/verified/' + esc(slug) + '.svg)](' + esc(DATA.pages_url) + '/)</div>'
      : '';
    return '<div class="hrow"><b>' + esc(v.repo) + '</b><em>doctor green · ' + esc(v.verified) + '</em>' +
      (v.run_url ? ' <a href="' + esc(v.run_url) + '">the run →</a>' : '') + '</div>' + badge;
  }).join('') +
    '<p class="vnone">structural checks against the official spec — a floor, not a safety guarantee · the badge markdown is yours to embed (click to copy)</p>';
}
function renderNetwork(){
  const N = (DATA.network || []).filter(n => (n.url || '').startsWith('https://'));
  const head = document.getElementById('network');
  const box = document.getElementById('networkbox');
  if (!N.length) { head.style.display = 'none'; box.style.display = 'none'; return; }
  head.style.display = 'block'; box.style.display = 'block';
  box.innerHTML = N.map(n =>
    '<div class="hrow"><b>' + esc(n.name) + '</b><em>registered ' + esc(n.registered) +
    (n.note ? ' · ' + esc(n.note) : '') + '</em>' +
    ' <a href="' + esc(n.url) + '">repo →</a>' +
    ((n.pages || '').startsWith('https://') ? ' <a href="' + esc(n.pages) + '">window →</a>' : '') + '</div>').join('') +
    '<p class="vnone">by their own declaration, URL verified by a maintainer shift — links out only</p>';
}
function renderHall(){
  const H = DATA.hall || {prospectors: [], patrons: [], breakers: []};
  const head = document.getElementById('hall');
  const box = document.getElementById('hallbox');
  const B = H.breakers || [];
  if (!H.prospectors.length && !H.patrons.length && !B.length) { head.style.display = 'none'; box.style.display = 'none'; return; }
  head.style.display = 'block'; box.style.display = 'block';
  box.innerHTML =
    H.prospectors.map(p =>
      '<div class="hrow"><b>@' + esc(p.login) + '</b><em>' + p.shipped + ' shipped · ' + p.total + ' formalized</em>' + (p.card ? ' <a href="' + esc(p.card) + '">card →</a>' : '') + '</div>').join('') +
    (H.patrons.length ? '<div class="hrow"><b>Patrons:</b><em>' + H.patrons.map(esc).join(' · ') + '</em></div>' : '') +
    (B.length ? '<div class="hrow"><b>Breakers</b><em>confirmed adversarial finds — from found_by lines in shipped changelogs (CONTRIBUTING Lane 3)</em></div>' +
      B.map(b => '<div class="hrow"><b>@' + esc(b.login) + '</b><em>' + b.finds + ' confirmed find(s) · ' + b.plugins.map(esc).join(', ') + '</em></div>').join('') : '');
}
function ago(iso){
  const s = (Date.now() - Date.parse(iso)) / 1000;
  if (!isFinite(s)) return 'live';
  if (s < 90) return 'active moments ago';
  if (s < 5400) return 'last shift ' + Math.round(s/60) + 'm ago';
  if (s < 172800) return 'last shift ' + Math.round(s/3600) + 'h ago';
  return 'last shift ' + Math.round(s/86400) + 'd ago';
}
function setHeroCounts(){
  const n = pubPlugins().length;
  for (const id of ['hero-count','proof-count','shelf-count']){
    const el = document.getElementById(id); if (el) el.textContent = n;
  }
}
function renderAll(){
  setHeroCounts();
  renderHostExperience();
  renderCatChips(); renderTagChips(); renderGrid(); renderClerk();
  renderTape(); renderStreak(); renderTheme(); renderLanes(); renderStats();
  renderQuality(); renderDogfood(); renderFuel(); renderAlarms(); renderVotes(); renderKits();
  renderHall(); renderVerified(); renderNetwork(); renderNextShift();
  if (DATA.repo){
    const rel = document.getElementById('relchip');
    rel.href = 'https://github.com/' + DATA.repo + '/releases';
    rel.style.display = '';
  }
  const ls = document.getElementById('lastshift');
  if (ls) ls.textContent = ago(DATA.generated_at);
}
q.addEventListener('input', () => { renderGrid(); renderClerk(); });
renderAll();
// copy-to-clipboard: click any install block to copy it whole. Degrades silently
// without a secure context — user-select:all still works.
document.addEventListener('click', ev => {
  const el = ev.target.closest('.install');
  if (!el || el.classList.contains('note') || !navigator.clipboard) return;
  navigator.clipboard.writeText(el.textContent.trim()).then(() => {
    el.dataset.copied = '1';
    setTimeout(() => { delete el.dataset.copied; }, 1400);
  }).catch(() => { /* selection fallback remains */ });
});
setInterval(() => {
  const ls = document.getElementById('lastshift');
  if (ls) ls.textContent = ago(DATA.generated_at);
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
@@OG@@
<style>
  .term{background:#161310;color:#E8DCC0;padding:12px;border:2px solid #2C2820;font-size:12.5px;line-height:1.55;overflow-x:auto}
  .honestlabel{margin:6px 0;font-size:11px;letter-spacing:.06em;text-transform:uppercase;opacity:.75}
  .trust{border:2px solid var(--ink);background:var(--card);padding:12px 14px;margin:14px 0}
  .trust h3{margin:0 0 8px;font-size:13px;letter-spacing:.12em;text-transform:uppercase}
  .trow{display:flex;gap:10px;padding:3px 0;border-bottom:1px dashed #C9BC9C;font-size:13px}
  .trow b{min-width:110px}
  .tnote{margin:8px 0 0;font-size:11px;opacity:.7}

  :root{--paper:#E9DFC8; --card:#F3ECDA; --ink:#2C2820; --line:#B5A683; --dim:#7E7460; --stamp:#2F5A8F}
  @media (prefers-color-scheme: dark){:root{--paper:#1C1913; --card:#26211A; --ink:#E4D8BC; --line:#4A4232; --dim:#9A8E74; --stamp:#8FB0DC}}
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


def og_meta(title, desc, url, image_url=""):
    """Open Graph / twitter card tags (ADR-016 #5; og:image v12 1.4). Values
    are derived at build time from the same substantiated data as the page.
    The image is a real screenshot of the window (foundry/assets/og-image.png,
    copied into site/ each build; re-shot when the hero changes)."""
    card = "summary_large_image" if image_url else "summary"
    tags = [f'<meta property="og:title" content="{html.escape(title)}">',
            f'<meta property="og:description" content="{html.escape(desc)}">',
            '<meta property="og:type" content="website">',
            f'<meta name="twitter:card" content="{card}">']
    if image_url:
        tags.append(f'<meta property="og:image" content="{html.escape(image_url)}">')
        tags.append('<meta property="og:image:width" content="1200">')
        tags.append('<meta property="og:image:height" content="630">')
    if url:
        tags.insert(2, f'<meta property="og:url" content="{html.escape(url)}">')
    return "\n".join(tags)


def og_image_url(cfg):
    """Absolute og:image URL when the asset exists and pages_url is set —
    substantiation law: never point at an image that isn't there."""
    pages_url = (cfg.get("pages_url") or "").rstrip("/")
    if pages_url and (ROOT / "foundry" / "assets" / "og-image.png").exists():
        return f"{pages_url}/og-image.png"
    return ""


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
                demo = ROOT / "foundry" / "demos" / f"{name}.txt"
                if demo.exists():
                    lines = demo.read_text().splitlines()
                    stamp = lines[0].replace("recorded:", "").strip() if lines and lines[0].startswith("recorded:") else "?"
                    body = "\n".join(lines[1:]).strip()
                    if body:
                        return ("<details open><summary>Example session</summary>"
                                f"<p class=\"honestlabel\">CI-recorded transcript — {html.escape(stamp)} "
                                "(charter/TESTING.md)</p>"
                                f"<pre class=\"term\">{html.escape(body)}</pre></details>")
                return ("<details open><summary>Example session</summary>"
                        "<p class=\"honestlabel\">authored example — a CI-recorded transcript "
                        "replaces this per charter/TESTING.md</p>"
                        f"<pre class=\"term\">{html.escape(text)}</pre></details>")
            o = ' open' if title in ('Test log','Review log','Verdict','Kill memo','Recipes') else ''
            return f"<details{o}><summary>{html.escape(title)}</summary><pre>{html.escape(text)}</pre></details>"
        sections = "".join(sec(t_, x_) for t_, x_ in extract_sections(r.get("_body", "")))
        # v10 #4: the certificate carries the shipped README verbatim — a visitor
        # can read what the plugin does without leaving for the file tree.
        readme_path = ROOT / "plugins" / name / "README.md"
        if r.get("kind", "plugin") == "plugin" and readme_path.exists():
            sections = (
                "<details open><summary>README — exactly what installers receive</summary>"
                f"<pre>{html.escape(readme_path.read_text())}</pre></details>"
            ) + sections
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
            if len(plugin_reports) > 8 and repo:
                items += (f'<a href="https://github.com/{repo}/issues?q=label%3Afield-report+{name}">'
                          f'all {len(plugin_reports)} reports \u2192</a>')
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
        pages_url = (cfg.get("pages_url") or "").rstrip("/")
        page = (PAGE_TEMPLATE
                .replace("@@OG@@", og_meta(
                    f"{r.get('title', name)} — provenance",
                    r.get("one_liner", ""),
                    f"{pages_url}/p/{name}.html" if pages_url else "",
                    og_image_url(cfg)))
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


def clip(text, limit):
    """Truncate at a word boundary with a visible ellipsis (i107 nit)."""
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + " …"


def build_saga(records, state, cfg):
    """Timeline from ADRs + record fates. Only what the sources say."""
    decisions = (ROOT / "state" / "DECISIONS.md").read_text()
    adrs = []
    for m in re.finditer(r"^## (ADR-\d+) — (.+?) \((i[\w-]+), ([\w-]+)\)\n(.*?)(?=^## ADR|\Z)",
                         decisions, re.M | re.S):
        ctx = re.search(r"- Context:\s*(.+)", m.group(5))
        adrs.append({"id": m.group(1), "title": m.group(2), "when": m.group(3),
                     "line": clip(" ".join((ctx.group(1) if ctx else "").split()), 180)})
    sharpest = []
    for r in records:
        for m in re.finditer(r"Sharpest question[^:]*:?\s*(.+?)(?=\n\s*-|\n\s*REVIEW|\n##|\Z)", r.get("_body", ""), re.S):
            qtxt = " ".join(m.group(1).split())
            if qtxt:
                sharpest.append((r.get("title", r.get("name", "?")), clip(qtxt, 220)))
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
    # family tree (v10 #14, foundry-network spec): who forked whom, by their own
    # declaration — names + links only, section absent while the network is empty
    network = load_json(ROOT / "foundry" / "network.json", {}).get("network", [])
    net_html = "".join(
        f"<li><em>{html.escape(n.get('registered', '?'))}</em> · "
        f"<b><a href=\"{html.escape(n.get('url', '#'))}\">{html.escape(n.get('name', '?'))}</a></b>"
        f"{' — ' + html.escape(n['note']) if n.get('note') else ''}</li>"
        for n in network)
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>the saga</title>
<style>
 :root{{--paper:#E9DFC8; --card:#F3ECDA; --ink:#2C2820; --line:#B5A683; --dim:#7E7460; --stamp:#2F5A8F}}
 @media (prefers-color-scheme: dark){{:root{{--paper:#1C1913; --card:#26211A; --ink:#E4D8BC; --line:#4A4232; --dim:#9A8E74; --stamp:#8FB0DC}}}}
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
{('<h2>Family tree — sister foundries, by their own declaration</h2><ul>' + net_html + '</ul>') if net_html else ''}
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
 :root{{--paper:#E9DFC8; --ink:#2C2820; --line:#B5A683; --dim:#7E7460; --stamp:#2F5A8F}}
 @media (prefers-color-scheme: dark){{:root{{--paper:#1C1913; --ink:#E4D8BC; --line:#4A4232; --dim:#9A8E74; --stamp:#8FB0DC}}}}
 body{{margin:0; font-family:ui-monospace,Menlo,Consolas,monospace; background:var(--paper); color:var(--ink)}}
 .tape{{overflow:hidden; white-space:nowrap; padding:8px 10px; border:1px solid var(--line)}}
 .reel{{display:inline-block; padding-left:100%}}
 @media (prefers-reduced-motion:no-preference){{.reel{{animation:reel 55s linear infinite}} .tape:hover .reel{{animation-play-state:paused}}
 @keyframes reel{{to{{transform:translateX(-100%)}}}}}}
 @media (prefers-reduced-motion:reduce){{.tape{{white-space:normal}} .reel{{padding-left:0}}}}
 span{{color:var(--dim); font-size:12px; margin-right:34px}} span b{{color:var(--ink); font-weight:400}}
 span em{{color:var(--stamp); font-style:normal}} .home{{font-size:11px; padding:4px 10px}} a{{color:var(--stamp)}}
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


def build_desk(cfg, state):
    """P0.8 (ADR-029): the desk, publicly legible. Open items only, ranked —
    visitors see that human decisions gate the machine (the governance story).
    The page shows RANK, never the live score: scores carry age in fractional
    days, so rendering them made committed output drift with the clock (the
    Gates sync-law caught it — i247). Order is clock-stable (score differences
    are time-invariant); the live score lives in `desk.py queue`."""
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "tools"))
    import desk as _desk
    ranked = _desk.rank(path=str(ROOT / "state" / "DESK.jsonl"))
    rows = "".join(
        f'<tr><td class="score">#{pos}</td>'
        f'<td class="id">{html.escape(it["id"])}</td>'
        f'<td><span class="kind k-{html.escape(str(it.get("kind")))}">{html.escape(str(it.get("kind")))}</span></td>'
        f'<td>{html.escape(str(it.get("title", "")))}</td>'
        f'<td class="agent">{html.escape(str(it.get("agent") or "—"))}</td></tr>'
        for pos, (_score, it) in enumerate(ranked, 1)) or \
        '<tr><td colspan="5" class="clear">The desk is clear — nothing awaits a human decision.</td></tr>'
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Owner's Desk — {html.escape(state.get('name') or 'foundry')}</title>
<style>
 body{{font-family:ui-monospace,Menlo,monospace; background:#f6efe2; color:#221c14; margin:0; padding:32px 16px}}
 .wrap{{max-width:820px; margin:0 auto}}
 h1{{font-size:20px}} p{{color:#6b5d49; font-size:13.5px; line-height:1.55}}
 table{{width:100%; border-collapse:collapse; font-size:13px; margin-top:18px}}
 td,th{{border-top:1px solid #d9c9a8; padding:9px 8px; text-align:left; vertical-align:top}}
 .id{{color:#6b5d49}} .score{{text-align:right}}
 .kind{{padding:2px 8px; border-radius:8px; color:#f6efe2; font-size:11px}}
 .k-alarm{{background:#a33327}} .k-ratify{{background:#8a6d3b}}
 .k-approve{{background:#1d5c8a}} .k-decide{{background:#6b5d49}}
 .clear{{color:#2e6b34}} a{{color:#1d5c8a}}
</style></head><body><div class="wrap">
<h1>🗂 The Owner's Desk</h1>
<p>Every decision this factory needs from a human lands in exactly one ranked
queue — nothing auto-merges past it (charter/CONSTITUTION.md Art. II), and
nothing else pings the operator (G4). The machine proposes; the human ratifies.
Source of truth: <code>state/DESK.jsonl</code>.</p>
<table><tr><th>rank</th><th>id</th><th>kind</th><th>item</th><th>from</th></tr>{rows}</table>
<p><a href="index.html">← the window</a></p>
</div></body></html>"""
    (ROOT / "site" / "desk.html").write_text(page)


def build_notfound(cfg, mp_name):
    """v12 3.2: a branded 404 in the clerk's voice — GitHub Pages serves
    404.html automatically for unknown paths."""
    base = (cfg.get("pages_url") or "").rstrip("/")
    home = f'{html.escape(base)}/' if base else "index.html"
    (ROOT / "site" / "404.html").write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 — nothing on this shelf</title>
<style>
 :root{{--paper:#E9DFC8; --card:#F3ECDA; --ink:#2C2820; --line:#B5A683; --dim:#7E7460; --stamp:#2F5A8F}}
 @media (prefers-color-scheme: dark){{:root{{--paper:#1C1913; --card:#26211A; --ink:#E4D8BC; --line:#4A4232; --dim:#9A8E74; --stamp:#8FB0DC}}}}
 body{{font-family:ui-monospace,Menlo,Consolas,monospace; background:var(--paper); color:var(--ink);
   display:grid; place-items:center; min-height:90vh; padding:20px}}
 .card{{max-width:520px; border:1.5px solid var(--ink); background:var(--card); padding:26px}}
 h1{{font-size:16px; letter-spacing:.14em; text-transform:uppercase; border-bottom:2px solid var(--ink); padding-bottom:8px}}
 p{{font-size:13px; line-height:1.6; color:var(--dim)}} a{{color:var(--stamp)}}
</style></head><body><div class="card">
<h1>404 — nothing on this shelf</h1>
<p>The clerk checked the back room: no such page. Published names are immutable
here, so if a link brought you to this, the link was wrong — the shelf never
moves its stock.</p>
<p><a href="{home}">← back to the window</a> · everything shipped is searchable there.</p>
</div></body></html>""")


def build_privacy_page(state):
    """Static, same-origin privacy disclosure for the public storefront."""
    title = html.escape(state.get("name") or "Nightshift Foundry")
    (ROOT / "site" / "privacy.html").write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — privacy</title>
<style>
 :root{{--paper:#EFE7D3;--card:#F7F1E1;--ink:#2B2620;--soft:#4A4235;--line:#C9B896;--stamp:#2F5A8F}}
 @media (prefers-color-scheme:dark){{:root{{--paper:#161310;--card:#211D16;--ink:#ECE1C6;--soft:#C9BB99;--line:#463D2D;--stamp:#8FB0DC}}}}
 *{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}}
 main{{max-width:760px;margin:0 auto;padding:54px 22px 80px}} h1{{font-size:clamp(30px,6vw,48px);line-height:1.05}}
 h2{{font-size:20px;margin-top:34px}} p,li{{color:var(--soft)}} a{{color:var(--stamp)}}
 .card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;margin:24px 0}}
 code{{font-family:ui-monospace,monospace}} .back{{font-weight:700}}
</style></head><body><main>
<p class="back"><a href="index.html">← Back to the Foundry</a></p>
<h1>Privacy without fine print.</h1>
<p>The storefront is static and intentionally low-data. It helps you choose and download a plugin without learning who you are.</p>
<div class="card"><strong>No analytics · no cookies · no accounts · no browser storage · no third-party scripts or remote fonts.</strong></div>
<h2>What the page does</h2>
<p>Your host choice lives only in the open page and disappears when it closes. Public catalog refreshes use same-origin <code>data.json</code>. No cross-origin request happens until you follow an external link.</p>
<h2>Downloads and plugins</h2>
<p>ZIPs are static, same-origin downloads. The Foundry does not learn which host or plugin you choose. Shipped hooks make no network calls and receive no Foundry credential.</p>
<h2>What GitHub receives</h2>
<p>GitHub Pages necessarily receives normal web request data under <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub's Privacy Statement</a>. This project does not receive or retain Pages access logs.</p>
<h2>Public contributions</h2>
<p>Issues and pull requests are public. Never include secrets, private code, customer data, or unnecessary personal information. Report sensitive security matters through <a href="https://github.com/GhostlyGawd/plugin-foundry/security/advisories/new">private vulnerability reporting</a>.</p>
<p><small>Last updated 2026-07-17 · Full policy: <a href="https://github.com/GhostlyGawd/plugin-foundry/blob/main/PRIVACY.md">PRIVACY.md</a></small></p>
</main></body></html>""")


def build_sitemap(records, cfg):
    """v12 3.3: sitemap.xml + robots.txt — 39 certificates deserve indexing.
    Emitted only with a configured pages_url (absolute URLs or nothing)."""
    base = (cfg.get("pages_url") or "").rstrip("/")
    if not base:
        return
    # lastmod reflects real content dates, not the run date (v13 C9): stamping
    # today into every entry churned sitemap.xml on every rebuild, so any CI run
    # dated after the committed file spuriously failed the gates' sync check.
    # Certificate pages carry their record's `updated`; the top-level pages carry
    # the newest record date (the last time the shelf actually moved). Now the
    # file changes only when content does — exactly when it's legitimately recommitted.
    dates = [r.get("updated") for r in records if r.get("updated")]
    newest = max(dates) if dates else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entries = [(u, newest) for u in
               (f"{base}/", f"{base}/saga.html", f"{base}/queue.html", f"{base}/theater.html",
                f"{base}/privacy.html")]
    entries += [(f"{base}/p/{r['name']}.html", r.get("updated") or newest)
                for r in records if r.get("name")]
    body = "".join(
        f"<url><loc>{html.escape(u)}</loc><lastmod>{html.escape(str(d))}</lastmod></url>"
        for u, d in entries)
    (ROOT / "site" / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>\n')
    (ROOT / "site" / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")


def build_verified_badges(cfg):
    """v12 4.2 (verified-by-foundry growth loop): one embeddable SVG per
    verified external repo — 'verified by the foundry | doctor green · date'.
    Hand-rolled two-cell shields-style SVG (stdlib-only law). Substantiation:
    a badge exists only for a registry entry, and every entry required a
    public run link to get listed. Empty registry -> no files at all."""
    entries = load_json(ROOT / "foundry" / "verified.json", {}).get("verified", [])
    outdir = ROOT / "site" / "verified"
    # regenerate from scratch: a delisted repo's badge must die with its listing
    if outdir.exists():
        shutil.rmtree(outdir)
    if not entries:
        return
    outdir.mkdir(parents=True, exist_ok=True)
    left = "verified by the foundry"
    for e in entries:
        repo = e.get("repo", "")
        if not repo or not e.get("run_url"):
            continue
        right = f"doctor green · {e.get('verified', '?')}"
        lw = 8 + int(len(left) * 6.6) + 8
        rw = 8 + int(len(right) * 6.6) + 8
        w = lw + rw
        slug = re.sub(r"[^A-Za-z0-9_-]", "-", repo)
        (outdir / f"{slug}.svg").write_text(f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="20" role="img" aria-label="{html.escape(left)}: {html.escape(right)}">
<title>{html.escape(left)}: {html.escape(right)} — structural checks only, a floor not a guarantee</title>
<rect width="{lw}" height="20" fill="#2C2820"/>
<rect x="{lw}" width="{rw}" height="20" fill="#2F5A8F"/>
<g fill="#E9DFC8" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11">
<text x="{lw // 2}" y="14" text-anchor="middle">{html.escape(left)}</text>
<text x="{lw + rw // 2}" y="14" text-anchor="middle">{html.escape(right)}</text>
</g></svg>
""")


def harden_site_html():
    """Apply a privacy baseline and hash-pinned script policy to every page.

    GitHub Pages cannot set repository-owned response headers. A CSP meta tag is
    still useful for script execution, connections, embeds, and object loads;
    each inline script is authorized by its exact SHA-256 instead of
    ``unsafe-inline``. Inline CSS remains allowed because the generated site uses
    style blocks and a small number of style attributes.
    """
    count = 0
    for path in sorted((ROOT / "site").rglob("*.html")):
        page = path.read_text(encoding="utf-8")
        if not re.search(r"<head[^>]*>", page, re.I):
            continue
        page = re.sub(
            r'<meta\s+name="referrer"\s+content="[^"]*"\s*/?>\s*',
            "", page, flags=re.I,
        )
        page = re.sub(
            r'<meta\s+http-equiv="Content-Security-Policy"\s+content="[^"]*"\s*/?>\s*',
            "", page, flags=re.I,
        )
        scripts = re.findall(r"<script(?:\s[^>]*)?>([\s\S]*?)</script\s*>", page, re.I)
        hashes = [
            "'sha256-" + base64.b64encode(
                hashlib.sha256(script.encode("utf-8")).digest()
            ).decode("ascii") + "'"
            for script in scripts
        ]
        script_policy = " ".join(hashes) if hashes else "'none'"
        policy = (
            "default-src 'self'; base-uri 'none'; form-action 'none'; "
            "object-src 'none'; frame-src 'none'; worker-src 'none'; "
            "connect-src 'self'; img-src 'self' data:; media-src 'self'; "
            "font-src 'self'; style-src 'self' 'unsafe-inline'; "
            f"script-src {script_policy}; upgrade-insecure-requests"
        )
        meta = (
            '<meta name="referrer" content="no-referrer">\n'
            f'<meta http-equiv="Content-Security-Policy" content="{policy}">'
        )
        page = re.sub(
            r"(<head[^>]*>)", lambda match: match.group(1) + "\n" + meta,
            page, count=1, flags=re.I,
        )
        path.write_text(page, encoding="utf-8", newline="\n")
        count += 1
    return count


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
def _cron_hours(spec):
    """Expand a cron hour field (`*`, `*/8`, `0,8,16`, `0-23/8`, `5`) to a list."""
    hours = set()
    for part in spec.split(","):
        part = part.strip()
        step = 1
        base = part
        if "/" in part:
            base, _, s = part.partition("/")
            step = int(s)
        if base == "*":
            lo, hi = 0, 23
        elif "-" in base:
            lo, hi = (int(x) for x in base.split("-", 1))
        else:
            lo = hi = int(base)
        hours.update(range(lo, hi + 1, step))
    return sorted(hours)


def shift_schedule():
    """Derive (minute, [hours]) from run-shift.yml's cron so the window countdown
    can't drift from the real schedule (P3, v14/ADR-024). Falls back to the
    documented default if the cron can't be read or parsed."""
    default = (17, [0, 8, 16])
    try:
        text = (ROOT / ".github" / "workflows" / "run-shift.yml").read_text()
        m = re.search(r'cron:\s*["\']?([0-9*,/ \-]+)', text)
        if not m:
            return default
        fields = m.group(1).split()
        if len(fields) < 2:
            return default
        return (int(fields[0]), _cron_hours(fields[1]) or default[1])
    except Exception:  # noqa: BLE001 — a countdown must never break the build
        return default


def build_quality(records):
    """GAP-A (ADR-031): the public quality number, computed only from what the
    repo can substantiate (growth-honesty law). Definitions, pinned:
    shipped = published kind:plugin records (the installable shelf);
    first-try QA = published records whose FIRST 'TEST VERDICT:' was pass
    (records without a Test log are excluded, counted separately);
    bounces = every bounce verdict on file (we show our rejects — that's the
    anti-slop proof); iterations = journaled loop iterations; ci shifts +
    spend = the BUDGET ledger (runs · summed cost_usd, honest zero)."""
    shipped = feats = first_try = bounced_first = no_log = 0
    bounces_total = 0
    for path in sorted(RECORDS.glob("*.md")):
        text = path.read_text()
        meta, _ = parse_front_matter(text)
        verdicts = re.findall(r"TEST VERDICT:\s*(\w+)", text)
        review_bounces = len(re.findall(r"REVIEW:\s*bounced", text))
        bounces_total += sum(1 for v in verdicts if v.lower() != "pass")
        bounces_total += review_bounces
        if meta.get("stage") != "published":
            continue
        if meta.get("kind", "plugin") == "plugin":
            shipped += 1
        else:
            feats += 1
        if not verdicts:
            no_log += 1
        elif verdicts[0].lower() == "pass" and review_bounces == 0:
            first_try += 1  # clean pass through QA AND review, no bounce
        else:
            bounced_first += 1
    graded = first_try + bounced_first
    pct = round(100 * first_try / graded) if graded else None
    journal = (ROOT / "state" / "JOURNAL.md")
    iters = len(re.findall(r"^## i\d+", journal.read_text(), re.M)) if journal.exists() else 0
    runs = spend = 0
    ledger = ROOT / "state" / "BUDGET.jsonl"
    if ledger.exists():
        for line in ledger.read_text().splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("kind") == "quota_run" or (not e.get("kind") and ("cost_usd" in e or "usage" in e)):
                runs += 1
            spend += e.get("cost_usd") or 0
    q = {"plugins_shipped": shipped, "features_shipped": feats,
         "qa_first_try_pct": pct, "qa_graded": graded, "qa_no_log": no_log,
         "bounces_total": bounces_total, "iterations": iters,
         "ci_shifts": runs, "api_spend_usd": round(spend, 2)}
    msg = f"{shipped} shipped"
    if pct is not None:
        msg += f" · {pct}% first-try QA"
    msg += f" · {iters} iterations"
    (ROOT / "site" / "quality.json").write_text(json.dumps(
        {"schemaVersion": 1, "label": "foundry", "message": msg,
         "color": "b08968"}, indent=1) + "\n")
    return q


def build_site(records, counts, state, mp_name, cfg, votes, kits, fuel_state, alarms, hall, streak,
               packages=None):
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
            "updated": r.get("updated"),
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
    tax = load_json(ROOT / "foundry" / "categories.json", {"categories": []})
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
        "quality": build_quality(records),
        "dogfood": load_json(ROOT / "foundry" / "dogfood.json", {}),
        "votes": votes,
        "roadmap": {k: [slim(r) for r in v] for k, v in roadmap_lanes(records).items()},
        "kits": kit_data,
        "fuel": fuel_state,
        "alarms": alarms,
        "hall": hall,
        "verified": load_json(ROOT / "foundry" / "verified.json", {}).get("verified", []),
        "network": load_json(ROOT / "foundry" / "network.json", {}).get("network", []),
        "streak": streak,
        "categories": tax.get("categories", []),
        "packages": packages or [],
        "repo": cfg.get("repo") or None,
        "pages_url": (cfg.get("pages_url") or "").rstrip("/") or None,
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
    compat_url = (f'https://github.com/{html.escape(repo)}/blob/main/COMPATIBILITY.md'
                  if repo else "#shelf")
    security_url = (f'https://github.com/{html.escape(repo)}/security/policy'
                    if repo else "#trust")
    suggest = (f'<a href="https://github.com/{html.escape(repo)}/issues/new?template=idea.yml">'
               f'suggest an idea, free</a>' if repo else "suggesting ideas opens with the repo (free)")

    shift_min, shift_hours = shift_schedule()
    page = (TEMPLATE
            .replace("@@SHIFT_MIN@@", str(shift_min))
            .replace("@@SHIFT_HOURS@@", json.dumps(shift_hours))
            .replace("@@TITLE@@", html.escape(title))
            .replace("@@OG@@", og_meta(
                f"{title} — a plugin workshop run entirely by AI",
                f"{data['counts']['published']} shipped · shift i{data['iteration']} — "
                "Cross-host coding-agent plugins built, tested, and published by an autonomous loop.",
                (cfg.get("pages_url") or "").rstrip("/"),
                og_image_url(cfg)))
            .replace("@@ITER@@", str(data["iteration"]).zfill(3))
            .replace("@@PHASE@@", html.escape(data["phase"]))
            .replace("@@LANE@@", lane_html)
            .replace("@@PRICE@@", html.escape(cfg.get("price_label", "$5.99")))
            .replace("@@CTA@@", cta)
            .replace("@@REPO_OR_HINT@@", repo_hint)
            .replace("@@REPO_LINK@@", repo_link)
            .replace("@@COMPAT_URL@@", compat_url)
            .replace("@@SECURITY_URL@@", security_url)
            .replace("@@SUGGEST@@", suggest)
            .replace("@@MPNAME@@", html.escape(mp_name))
            .replace("@@MP@@", json.dumps(mp_name))
            .replace("@@DATA@@", json.dumps(data))
            .replace("@@STAMP@@", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")))
    (ROOT / "site" / "index.html").write_text(page)
    return data


def main():
    # a fresh checkout has no site/ dir; build writes into it, so make it first
    # (bug: the firstborn crashed here at genesis — v14/ADR-024).
    (ROOT / "site").mkdir(parents=True, exist_ok=True)
    state = json.loads((ROOT / "state" / "STATE.json").read_text())
    mp = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    cfg = json.loads((ROOT / "foundry" / "site-config.json").read_text())
    # v12 1.4: ship the social card with the site (source of truth in assets/)
    og_src = ROOT / "foundry" / "assets" / "og-image.png"
    if og_src.exists():
        (ROOT / "site").mkdir(exist_ok=True)
        (ROOT / "site" / "og-image.png").write_bytes(og_src.read_bytes())
    # GAP-A3: the replay proof artifact rides along (source: tools/replay.py)
    rp_src = ROOT / "foundry" / "assets" / "replay.svg"
    if rp_src.exists():
        (ROOT / "site" / "replay.svg").write_text(rp_src.read_text())
    mp_name = mp.get("name", "foundry")
    # P1.4: regrade the dogfood card from live evidence so it never goes stale
    try:
        import dogfood as _dogfood
        with open(ROOT / "foundry" / "dogfood.json", "w", encoding="utf-8") as _f:
            json.dump(_dogfood.compute(), _f, indent=1, ensure_ascii=False)
            _f.write("\n")
    except Exception:  # noqa: BLE001 — a card refresh must never break the build
        pass
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

    package_count = 0
    packages = []
    # Full foundry builds publish one native package per plugin and host. Minimal gate
    # fixtures intentionally omit the exporter and skip this product surface.
    if (ROOT / "tools" / "export.py").is_file() \
            and (ROOT / "COMPATIBILITY.md").is_file() \
            and (ROOT / "plugins").is_dir():
        from export import build_archives, plugin_names
        names = plugin_names()
        if names:
            packages = build_archives(names, ROOT / "site" / "downloads", clean=True)
            package_count = sum(len(plugin["packages"]) for plugin in packages)

    data = build_site(records, counts, state, mp_name, cfg, votes, kits,
                      fuel(cfg), alarms, hall, streak, packages)
    build_pages(records, mp_name, cfg, reports)
    build_saga(records, state, cfg)
    build_embed(data["ticker"], cfg)
    build_theater(state, cfg)
    build_queue(records, cfg)
    build_badge(records, state)
    build_desk(cfg, state)
    build_feed(records, cfg)
    build_notfound(cfg, mp_name)
    build_privacy_page(state)
    build_sitemap(records, cfg)
    build_verified_badges(cfg)
    hardened_pages = harden_site_html()
    # P0.1 (ADR-026): the agent registry is generated, never hand-edited; a
    # manifest that breaks the contract fails the build, same as a bad record.
    from lib import build_agent_registry
    n_agents, agent_errors = build_agent_registry(str(ROOT))
    if agent_errors:
        for e in agent_errors:
            print(f"BUILD: agent contract — {e}")
        raise SystemExit(1)
    print(
        "BUILD: OK — INDEX.md + index/data/saga/embed/badge/feed + "
        f"{len(records)} certificates + {package_count} host-native packages + "
        f"{n_agents} agent manifests + {hardened_pages} CSP-hardened pages"
    )


if __name__ == "__main__":
    main()
