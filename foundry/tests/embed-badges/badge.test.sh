#!/usr/bin/env bash
# embed-badges acceptance checks (record: foundry/records/embed-badges.md)
set -uo pipefail
cd "${REPO_ROOT:-$(pwd)}"

python3 - << 'PY'
import json, re

# check 1 — shields endpoint schema, values substantiated by the repo
b = json.load(open("site/badge.json"))
ok = (b.get("schemaVersion") == 1 and isinstance(b.get("label"), str) and b["label"]
      and isinstance(b.get("message"), str) and re.fullmatch(r"[0-9A-Fa-f]{6}", b.get("color", "")))
data = json.load(open("site/data.json"))
shipped = sum(1 for r in data["records"] if r["stage"] == "published")
m = re.match(r"(\d+) shipped · i(\d+)", b.get("message", ""))
substantiated = bool(m) and int(m.group(1)) == shipped and int(m.group(2)) == data["iteration"]
print("ok: badge.json shields schema + substantiated counts" if ok and substantiated
      else f"fail: badge.json — schema_ok={ok} substantiated={substantiated} msg={b.get('message')!r} shipped={shipped} iter={data['iteration']}")

# check 2 — embed.html script-free, viewport meta, reduced-motion, ticker present
e = open("site/embed.html").read()
checks = ("<script" not in e.lower(), 'name="viewport"' in e,
          "prefers-reduced-motion" in e, 'class="reel"' in e)
print("ok: embed.html static ticker, iframe-safe" if all(checks)
      else f"fail: embed.html — script_free={checks[0]} viewport={checks[1]} motion={checks[2]} reel={checks[3]}")

# check 3 — i114 bounce regression: config set → README carries the REAL url, no placeholders
cfg = json.load(open("foundry/site-config.json"))
rd = open("README.md").read()
if cfg.get("pages_url"):
    from urllib.parse import quote
    enc = quote(cfg["pages_url"], safe="")
    good = ("<pages_url>" not in rd
            and (cfg["pages_url"] + "/embed.html") in rd
            and (enc + "%2Fbadge.json") in rd)
    print("ok: README snippet works as pasted (real url, no placeholders)" if good
          else "fail: README snippet — placeholder remains or url mismatch with site-config")
else:
    print("skip: pages_url unset — placeholder snippet acceptable until go-live")
PY
