#!/usr/bin/env python3
"""tokencost.py — deterministic estimator of a plugin's ALWAYS-ON context cost:
the frontmatter descriptions Claude Code loads every session (skills, agents,
commands, manifest). chars/4, rounded up — labeled "est." everywhere it appears,
because honest instruments say what they are. Usage: tokencost.py <plugin-name>"""
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def desc_of(md_path):
    text = md_path.read_text()
    chars = 0
    for key in ("name", "description"):
        m = re.search(rf"^{key}:\s*(.+)$", text.split("---")[1] if text.startswith("---") else "", re.M)
        if m:
            chars += len(m.group(1))
    return chars


def estimate(name):
    p = ROOT / "plugins" / name
    if not p.is_dir():
        return None
    chars = 0
    try:
        manifest = json.loads((p / ".claude-plugin" / "plugin.json").read_text())
        chars += len(manifest.get("description", "")) + len(manifest.get("name", ""))
    except Exception:  # noqa: BLE001
        pass
    for md in list(p.glob("skills/*/SKILL.md")) + list(p.glob("agents/*.md")) + list(p.glob("commands/*.md")):
        chars += desc_of(md)
    return math.ceil(chars / 4)


if __name__ == "__main__":
    name = sys.argv[1]
    est = estimate(name)
    print(json.dumps({"plugin": name, "always_on_tokens_est": est}))
