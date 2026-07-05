#!/usr/bin/env python3
"""clerkcat — regenerate night-clerk's bundled catalog from the records.
Published plugins only. Run by the maintainer whenever the shelf changes;
each regeneration ships inside a night-clerk patch bump (version law)."""
import json, re, datetime, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

def front(path):
    t = path.read_text()
    m = re.match(r"---\n(.*?)\n---", t, re.S)
    meta = {}
    for line in (m.group(1) if m else "").splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta

def main():
    plugins = []
    for p in sorted((ROOT / "foundry" / "records").glob("*.md")):
        m = front(p)
        if m.get("stage") == "published" and m.get("kind", "plugin") == "plugin":
            tags = [t.strip() for t in m.get("tags", "").strip("[]").split(",") if t.strip()]
            plugins.append({
                "name": m["name"],
                "one_liner": m.get("one_liner", ""),
                "tags": tags,
                "install": f"/plugin install {m['name']}@foundry",
            })
    out = {
        "snapshot": datetime.date.today().isoformat(),
        "marketplace": "foundry",
        "idea_template": "issues/new?template=idea.yml",
        "plugins": plugins,
    }
    dest = ROOT / "plugins" / "night-clerk" / "data" / "catalog.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=1) + "\n")
    print(f"clerkcat: {len(plugins)} published plugins → {dest.relative_to(ROOT)}")

if __name__ == "__main__":
    sys.exit(main())
