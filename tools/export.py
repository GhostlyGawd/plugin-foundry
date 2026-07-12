#!/usr/bin/env python3
"""export.py — multi-harness portability (MASTER GAP-C, ADR-031).

Every breakout repo in this ecosystem is multi-harness; Claude-Code-only caps
the audience. This reads a shipped plugin and emits a HARNESS-NEUTRAL descriptor
(portable.json) plus adapter notes for other agent harnesses (Codex, Cursor,
Gemini CLI). It does NOT touch the published plugin (names/versions are forever —
no Version-law churn); the export is a derived artifact under dist/.

A skill is fundamentally a named instruction + a trigger description + a body —
that core is portable; only the packaging differs per harness. This extracts
that core so an adapter can repackage it.

  export.py <plugin-name> [--out DIR]
Writes dist/<plugin>/portable.json. Stdlib only. Deterministic.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from lib import parse_front_matter  # noqa: E402

# How each harness consumes a portable skill (adapter targets, documented).
ADAPTERS = {
    "claude-code": "native — skills/<name>/SKILL.md + .claude-plugin/plugin.json",
    "codex": "AGENTS.md instruction block per skill (name + when-to-use + body)",
    "cursor": ".cursor/rules/<name>.mdc (description + globs + body)",
    "gemini-cli": "GEMINI.md section per skill (name + trigger + body)",
}


def read_plugin(name):
    pdir = os.path.join(ROOT, "plugins", name)
    if not os.path.isdir(pdir):
        raise SystemExit(f"export: no plugin '{name}'")
    manifest = {}
    mp = os.path.join(pdir, ".claude-plugin", "plugin.json")
    if os.path.exists(mp):
        manifest = json.load(open(mp, encoding="utf-8"))
    skills = []
    sdir = os.path.join(pdir, "skills")
    if os.path.isdir(sdir):
        for s in sorted(os.listdir(sdir)):
            sf = os.path.join(sdir, s, "SKILL.md")
            if os.path.exists(sf):
                meta, body = parse_front_matter(open(sf, encoding="utf-8").read())
                skills.append({
                    "name": meta.get("name", s),
                    "when_to_use": meta.get("description", ""),
                    "body": body.strip(),
                })
    hooks = os.path.isdir(os.path.join(pdir, "hooks"))
    return manifest, skills, hooks


def portable(name):
    manifest, skills, has_hooks = read_plugin(name)
    return {
        "schema": "foundry.portable/1",
        "plugin": name,
        "version": manifest.get("version"),
        "description": manifest.get("description", ""),
        "skills": skills,
        "notes": {
            "hooks": ("this plugin has hooks — hooks are harness-specific "
                      "(lifecycle events differ); adapt per target, do not "
                      "auto-port destructive behavior") if has_hooks else "none",
            "adapters": ADAPTERS,
            "immutability": "the published Claude Code plugin is untouched; "
                            "this is a derived artifact (names are forever).",
        },
    }


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    out = os.path.join(ROOT, "dist")
    if "--out" in argv:
        i = argv.index("--out"); out = argv[i + 1]; argv = argv[:i] + argv[i + 2:]
    if not argv:
        print("usage: export.py <plugin-name> [--out DIR]")
        return 1
    name = argv[0]
    data = portable(name)
    d = os.path.join(out, name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "portable.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"export: {name} → {os.path.relpath(d, ROOT)}/portable.json "
          f"({len(data['skills'])} portable skill(s); adapters for "
          f"{', '.join(k for k in ADAPTERS if k != 'claude-code')})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
