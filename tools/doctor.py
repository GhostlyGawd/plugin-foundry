#!/usr/bin/env python3
"""doctor.py — standalone structural health-check for ONE Claude Code plugin
directory (verified-by-foundry, v10 #13). No foundry-repo assumptions: no
records, no marketplace, no state — point it at any plugin checkout.

The law tables are imported from validate.py so there is exactly one law book
(hook events/types, kebab-case names, semver), per the official plugin spec:
https://code.claude.com/docs/en/plugins-reference

Usage: doctor.py <plugin-dir>     exit 0 "DOCTOR: OK" | exit 1 + violations
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import parse_front_matter          # noqa: E402
from validate import (                      # noqa: E402 — one law book
    HOOK_EVENTS, HOOK_TYPES, NAME_RE, SEMVER_RE,
)


def check(pdir):
    pdir = Path(pdir)
    errors = []
    if not pdir.is_dir():
        return [f"{pdir}: not a directory"]

    manifest_path = pdir / ".claude-plugin" / "plugin.json"
    manifest = None
    if not manifest_path.exists():
        errors.append(".claude-plugin/plugin.json: missing (the manifest is required)")
    else:
        try:
            manifest = json.loads(manifest_path.read_text())
        except Exception as exc:  # noqa: BLE001
            errors.append(f".claude-plugin/plugin.json: unreadable JSON ({exc})")

    if manifest is not None:
        name = manifest.get("name", "")
        if not NAME_RE.match(name):
            errors.append(f"plugin.json: name {name!r} must be kebab-case")
        ver = manifest.get("version")
        if ver is not None and not SEMVER_RE.match(str(ver)):
            errors.append(f"plugin.json: version {ver!r} is not semver")
        if not manifest.get("description"):
            errors.append("plugin.json: description missing (installers see this)")
        for field in ("skills", "commands", "agents", "hooks", "mcpServers",
                      "outputStyles", "lspServers"):
            val = manifest.get(field)
            paths = val if isinstance(val, list) else [val] if isinstance(val, str) else []
            for p in paths:
                if isinstance(p, str) and not p.startswith("./"):
                    errors.append(f"plugin.json: {field} path {p!r} must start with ./")
        for stray in sorted((pdir / ".claude-plugin").iterdir()):
            if stray.name != "plugin.json":
                errors.append(f".claude-plugin/{stray.name}: only plugin.json belongs here")

    for skill_md in sorted(pdir.glob("skills/*/SKILL.md")):
        meta, _ = parse_front_matter(skill_md.read_text(), errors,
                                     str(skill_md.relative_to(pdir)))
        for key in ("name", "description"):
            if not meta.get(key):
                errors.append(f"{skill_md.relative_to(pdir)}: frontmatter missing {key!r}")
    for cmd_md in sorted(pdir.glob("commands/*.md")):
        meta, _ = parse_front_matter(cmd_md.read_text(), errors,
                                     str(cmd_md.relative_to(pdir)))
        if not meta.get("description"):
            errors.append(f"{cmd_md.relative_to(pdir)}: frontmatter missing 'description'")
    for agent_md in sorted(pdir.glob("agents/*.md")):
        meta, _ = parse_front_matter(agent_md.read_text(), errors,
                                     str(agent_md.relative_to(pdir)))
        for key in ("name", "description"):
            if not meta.get(key):
                errors.append(f"{agent_md.relative_to(pdir)}: frontmatter missing {key!r}")

    hooks_path = pdir / "hooks" / "hooks.json"
    if hooks_path.exists():
        try:
            hooks_cfg = json.loads(hooks_path.read_text())
        except Exception as exc:  # noqa: BLE001
            hooks_cfg = None
            errors.append(f"hooks/hooks.json: unreadable JSON ({exc})")
        if hooks_cfg is not None:
            for event, entries in (hooks_cfg.get("hooks") or {}).items():
                if event not in HOOK_EVENTS:
                    errors.append(f"hooks.json: unknown hook event {event!r} (case-sensitive)")
                for entry in entries or []:
                    if entry.get("matcher") == ".*":
                        errors.append("hooks.json: matcher '.*' — hooks are guests, match narrowly")
                    for h in entry.get("hooks", []):
                        if h.get("type") not in HOOK_TYPES:
                            errors.append(f"hooks.json: unknown hook type {h.get('type')!r}")
                        cmd = h.get("command", "")
                        if "${CLAUDE_PLUGIN_ROOT}" in cmd and '"${CLAUDE_PLUGIN_ROOT}' not in cmd:
                            errors.append("hooks.json: unquoted ${CLAUDE_PLUGIN_ROOT} in command")

    for script in sorted(pdir.glob("scripts/*")):
        if script.is_file():
            rel = script.relative_to(pdir)
            if not os.access(script, os.X_OK):
                errors.append(f"{rel}: not executable (chmod +x)")
            first = script.read_text(errors="replace").splitlines()[:1]
            if not first or not first[0].startswith("#!"):
                errors.append(f"{rel}: missing shebang")

    return errors


def main():
    if len(sys.argv) != 2:
        print("usage: doctor.py <plugin-dir>", file=sys.stderr)
        return 2
    errors = check(sys.argv[1])
    if errors:
        print(f"DOCTOR: {len(errors)} problem(s) in {sys.argv[1]}")
        for err in errors:
            print(f"  ✗ {err}")
        return 1
    print(f"DOCTOR: OK — {sys.argv[1]} passes the foundry's structural laws")
    return 0


if __name__ == "__main__":
    sys.exit(main())
