#!/usr/bin/env python3
"""Generate and verify the foundry's cross-host plugin packaging.

The Claude manifest remains the canonical product metadata. This tool derives
native Codex, Cursor, Copilot, and Gemini manifests, target-specific hook maps,
and repository marketplace indexes without duplicating plugin behavior.

Usage:
  python3 tools/adapters.py --write
  python3 tools/adapters.py --check
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / "plugins"
REPOSITORY = "https://github.com/GhostlyGawd/plugin-foundry"
PAGES = "https://ghostlygawd.github.io/plugin-foundry"

CURSOR_EVENTS = {
    "SessionStart": "sessionStart",
    "Stop": "stop",
    "PreToolUse": "preToolUse",
}
GEMINI_EVENTS = {
    "SessionStart": "SessionStart",
    "Stop": "AfterAgent",
    "PreToolUse": "BeforeTool",
}
GEMINI_MATCHERS = {"Bash": "run_shell_command"}


def encode(data: object) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def plugin_dirs() -> list[Path]:
    return sorted(
        path for path in PLUGINS.iterdir()
        if path.is_dir() and (path / ".claude-plugin" / "plugin.json").is_file()
    )


def canonical_manifest(plugin: Path) -> dict:
    manifest = read_json(plugin / ".claude-plugin" / "plugin.json")
    name = manifest["name"]
    manifest.setdefault("homepage", f"{PAGES}/p/{name}.html")
    manifest.setdefault("repository", REPOSITORY)
    if (plugin / "skills").is_dir():
        manifest["skills"] = "./skills/"
    if (plugin / "hooks" / "hooks.json").is_file():
        manifest["hooks"] = "./hooks/hooks.json"
    return manifest


def select(manifest: dict, fields: tuple[str, ...]) -> dict:
    return {field: manifest[field] for field in fields if field in manifest}


def codex_manifest(manifest: dict, has_hooks: bool) -> dict:
    data = select(manifest, (
        "name", "version", "description", "author", "homepage", "repository",
        "license", "keywords", "skills",
    ))
    if has_hooks:
        data["hooks"] = "./hooks/codex.json"
    return data


def cursor_manifest(manifest: dict, has_hooks: bool) -> dict:
    data = select(manifest, (
        "name", "displayName", "version", "description", "author", "homepage",
        "repository", "license", "keywords",
    ))
    if "skills" in manifest:
        data["skills"] = "./skills/"
    if has_hooks:
        data["hooks"] = "./hooks/cursor.json"
    return data


def copilot_manifest(manifest: dict, has_hooks: bool) -> dict:
    data = select(manifest, (
        "name", "version", "description", "author", "homepage", "repository",
        "license", "keywords",
    ))
    if "skills" in manifest:
        data["skills"] = "./skills/"
    if has_hooks:
        # Copilot supports the Open Plugin nested matcher contract.
        data["hooks"] = "./hooks/copilot.json"
    return data


def gemini_manifest(manifest: dict) -> dict:
    return select(manifest, ("name", "version", "description"))


def open_plugin_hooks(plugin: Path) -> dict | None:
    path = plugin / "hooks" / "hooks.json"
    return read_json(path) if path.is_file() else None


def replace_root(command: str, variable: str) -> str:
    return command.replace("${CLAUDE_PLUGIN_ROOT}", variable)


def open_plugin_target_hooks(source: dict) -> dict:
    """Keep Open Plugin events/nesting but use the host-native root variable."""
    data = json.loads(json.dumps(source))
    for groups in data.get("hooks", {}).values():
        for group in groups:
            for handler in group.get("hooks", []):
                handler["command"] = replace_root(
                    handler["command"], "${PLUGIN_ROOT}"
                )
    return data


def cursor_hooks(source: dict) -> dict:
    hooks: dict[str, list[dict]] = {}
    for event, groups in source.get("hooks", {}).items():
        target = CURSOR_EVENTS[event]
        entries: list[dict] = []
        for group in groups:
            for handler in group.get("hooks", []):
                entries.append({
                    "command": replace_root(
                        handler["command"], "${CURSOR_PLUGIN_ROOT}"
                    )
                })
        hooks[target] = entries
    return {"version": 1, "hooks": hooks}


def gemini_hooks(source: dict) -> dict:
    hooks: dict[str, list[dict]] = {}
    for event, groups in source.get("hooks", {}).items():
        target = GEMINI_EVENTS[event]
        entries: list[dict] = []
        for group in groups:
            entry: dict = {}
            matcher = group.get("matcher")
            if matcher:
                entry["matcher"] = GEMINI_MATCHERS.get(matcher, matcher)
            entry["hooks"] = []
            for handler in group.get("hooks", []):
                adapted = dict(handler)
                adapted["command"] = replace_root(
                    adapted["command"], "${extensionPath}"
                )
                entry["hooks"].append(adapted)
            entries.append(entry)
        hooks[target] = entries
    return {"hooks": hooks}


def marketplace_entries(manifests: list[dict]) -> tuple[dict, dict, dict]:
    descriptions = {
        entry["name"]: entry.get("description", "")
        for entry in read_json(ROOT / ".claude-plugin" / "marketplace.json")["plugins"]
    }
    codex = {
        "name": "foundry",
        "interface": {"displayName": "Nightshift Foundry"},
        "plugins": [],
    }
    cursor = {
        "name": "foundry",
        "owner": {"name": "Nightshift Foundry"},
        "metadata": {
            "description": "Portable, inspectable developer-workflow plugins."
        },
        "plugins": [],
    }
    copilot = {
        "name": "foundry",
        "owner": {"name": "Nightshift Foundry"},
        "metadata": {
            "description": "Portable, inspectable developer-workflow plugins.",
            "version": "1.0.0",
        },
        "plugins": [],
    }
    for manifest in manifests:
        name = manifest["name"]
        description = descriptions.get(name, manifest.get("description", ""))
        codex["plugins"].append({
            "name": name,
            "source": {"source": "local", "path": f"./plugins/{name}"},
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Developer Tools",
        })
        cursor["plugins"].append({
            "name": name,
            "source": f"plugins/{name}",
            "description": description,
        })
        copilot["plugins"].append({
            "name": name,
            "description": description,
            "version": manifest["version"],
            "source": f"./plugins/{name}",
        })
    return codex, cursor, copilot


def expected_files() -> dict[Path, str]:
    expected: dict[Path, str] = {}
    manifests: list[dict] = []
    for plugin in plugin_dirs():
        manifest = canonical_manifest(plugin)
        manifests.append(manifest)
        source_hooks = open_plugin_hooks(plugin)
        expected[plugin / ".claude-plugin" / "plugin.json"] = encode(manifest)
        expected[plugin / ".codex-plugin" / "plugin.json"] = encode(
            codex_manifest(manifest, source_hooks is not None)
        )
        expected[plugin / ".cursor-plugin" / "plugin.json"] = encode(
            cursor_manifest(manifest, source_hooks is not None)
        )
        expected[plugin / ".github" / "plugin" / "plugin.json"] = encode(
            copilot_manifest(manifest, source_hooks is not None)
        )
        expected[plugin / ".gemini-adapter" / "gemini-extension.json"] = encode(
            gemini_manifest(manifest)
        )
        if source_hooks is not None:
            expected[plugin / "hooks" / "codex.json"] = encode(
                open_plugin_target_hooks(source_hooks)
            )
            expected[plugin / "hooks" / "copilot.json"] = encode(
                open_plugin_target_hooks(source_hooks)
            )
            expected[plugin / "hooks" / "cursor.json"] = encode(
                cursor_hooks(source_hooks)
            )
            # The exporter places this adapter at hooks/hooks.json in Gemini ZIPs.
            expected[plugin / "hooks" / "gemini.json"] = encode(
                gemini_hooks(source_hooks)
            )

    codex, cursor, copilot = marketplace_entries(manifests)
    expected[ROOT / ".agents" / "plugins" / "marketplace.json"] = encode(codex)
    expected[ROOT / ".cursor-plugin" / "marketplace.json"] = encode(cursor)
    expected[ROOT / ".github" / "plugin" / "marketplace.json"] = encode(copilot)
    return expected


def obsolete_files() -> list[Path]:
    obsolete = []
    for plugin in plugin_dirs():
        obsolete.extend([
            plugin / "gemini-extension.json",
            plugin / "hooks" / "claude.json",
        ])
    return obsolete


def write_all(expected: dict[Path, str]) -> None:
    changed = 0
    removed = 0
    for path in obsolete_files():
        if path.is_file():
            path.unlink()
            removed += 1
    for path, content in expected.items():
        if path.is_file() and path.read_text(encoding="utf-8") == content:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        changed += 1
    print(
        f"adapters: wrote {changed} changed file(s), removed {removed} obsolete; "
        f"{len(expected)} tracked"
    )


def check_all(expected: dict[Path, str]) -> int:
    drift = []
    for path, content in expected.items():
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            drift.append(path.relative_to(ROOT).as_posix())
    for path in obsolete_files():
        if path.is_file():
            drift.append(path.relative_to(ROOT).as_posix() + " (obsolete)")
    if drift:
        for path in drift:
            print(f"adapters: drift — {path}")
        print("adapters: FAIL — run python3 tools/adapters.py --write")
        return 1
    print(
        f"adapters: OK — {len(plugin_dirs())} shared plugin sources, "
        "Claude/Codex/Cursor/Gemini/Copilot adapters in sync"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = expected_files()
    if args.write:
        write_all(expected)
        return 0
    return check_all(expected)


if __name__ == "__main__":
    raise SystemExit(main())
