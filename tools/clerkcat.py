#!/usr/bin/env python3
"""clerkcat — regenerate night-clerk's bundled catalog from the records.
Published plugins only. Run by the maintainer whenever the shelf changes;
each regeneration ships inside a night-clerk patch bump (version law)."""
import json, datetime, pathlib, sys

from lib import parse_front_matter  # one parser, one truth (v10 #8)

ROOT = pathlib.Path(__file__).resolve().parents[1]


def installs(name):
    """Host-native install path; no host inference or command invention at runtime."""
    return {
        "claude-code": f"/plugin install {name}@foundry",
        "codex": f"Install {name} from Nightshift Foundry in the Plugins Directory",
        "gemini-cli": f"gemini extensions install ./{name}",
        "cursor": f"Copy {name}/ to ~/.cursor/plugins/local/{name}/ and reload Cursor",
        "github-copilot": f"copilot plugin install {name}@foundry",
    }

def main():
    plugins = []
    for p in sorted((ROOT / "foundry" / "records").glob("*.md")):
        m, _ = parse_front_matter(p.read_text())
        if m.get("stage") == "published" and m.get("kind", "plugin") == "plugin":
            tags = m.get("tags", []) if isinstance(m.get("tags"), list) else []
            plugins.append({
                "name": m["name"],
                "version": m.get("version", ""),
                "one_liner": m.get("one_liner", ""),
                "tags": tags,
                "install": f"/plugin install {m['name']}@foundry",
                "installs": installs(m["name"]),
            })
    # kits (ADR-016 #8): the clerk may offer a curated bundle when the task maps
    # to one. Published members only — the clerk never recommends vaporware.
    published = {p["name"] for p in plugins}
    kits = []
    kits_path = ROOT / "foundry" / "kits.json"
    if kits_path.exists():
        for k in json.loads(kits_path.read_text()).get("kits", []):
            ready = [m for m in k.get("plugins", []) if m in published]
            if ready:
                kits.append({"id": k["id"], "name": k.get("name", k["id"]),
                             "desc": k.get("desc", ""),
                             "install": [f"/plugin install {m}@foundry" for m in ready],
                             "installs": {m: installs(m) for m in ready}})
    out = {
        "snapshot": datetime.date.today().isoformat(),
        "marketplace": "foundry",
        "idea_template": "issues/new?template=idea.yml",
        "plugins": plugins,
        "kits": kits,
    }
    dest = ROOT / "plugins" / "night-clerk" / "data" / "catalog.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=1) + "\n")
    print(f"clerkcat: {len(plugins)} published plugins → {dest.relative_to(ROOT)}")

if __name__ == "__main__":
    sys.exit(main())
