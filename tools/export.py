#!/usr/bin/env python3
"""Build deterministic, host-native plugin packages from one shared source.

Claude/Open Plugin and Gemini reserve the same hooks/hooks.json path but use
different event names. Publishing one ZIP for both would make one host reject
the other's schema, so the foundry emits a small native archive per host:

  python3 tools/export.py <plugin-name> [--out DIR]
  python3 tools/export.py --all [--out DIR]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import stat
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / "plugins"
HOSTS = ["claude-code", "codex", "gemini-cli", "cursor", "github-copilot"]
HOST_MANIFESTS = {
    "claude-code": (".claude-plugin/plugin.json", ".claude-plugin/plugin.json"),
    "codex": (".codex-plugin/plugin.json", ".codex-plugin/plugin.json"),
    "gemini-cli": (".gemini-adapter/gemini-extension.json", "gemini-extension.json"),
    "cursor": (".cursor-plugin/plugin.json", ".cursor-plugin/plugin.json"),
    "github-copilot": (".github/plugin/plugin.json", ".github/plugin/plugin.json"),
}
HOST_HOOKS = {
    "claude-code": ("hooks/hooks.json", "hooks/hooks.json"),
    "codex": ("hooks/codex.json", "hooks/codex.json"),
    "gemini-cli": ("hooks/gemini.json", "hooks/hooks.json"),
    "cursor": ("hooks/cursor.json", "hooks/cursor.json"),
    "github-copilot": ("hooks/copilot.json", "hooks/copilot.json"),
}
MANIFEST_DIRS = {".claude-plugin", ".codex-plugin", ".cursor-plugin", ".gemini-adapter", ".github"}
ADAPTER_HOOKS = {source for source, _ in HOST_HOOKS.values()}
SKIP_NAMES = {".DS_Store", "Thumbs.db"}
SKIP_PARTS = {"__pycache__"}
TEXT_SUFFIXES = {
    ".css", ".html", ".js", ".json", ".md", ".py", ".sh", ".toml",
    ".txt", ".xml", ".yaml", ".yml",
}


def read_manifest(plugin: Path) -> dict:
    return json.loads(
        (plugin / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )


def plugin_names() -> list[str]:
    return sorted(
        path.name for path in PLUGINS.iterdir()
        if path.is_dir() and (path / ".claude-plugin" / "plugin.json").is_file()
    )


def shared_files(plugin: Path) -> list[tuple[Path, str]]:
    """Return host-neutral files, excluding generated manifests/hook maps."""
    files: list[tuple[Path, str]] = []
    for path in plugin.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(plugin)
        rel_posix = rel.as_posix()
        if path.name in SKIP_NAMES or any(part in SKIP_PARTS for part in rel.parts):
            continue
        if rel.parts[0] in MANIFEST_DIRS or rel_posix in ADAPTER_HOOKS:
            continue
        files.append((path, rel_posix))
    return sorted(files, key=lambda item: item[1])


def package_files(plugin: Path, host: str) -> list[tuple[Path, str]]:
    source_manifest, archive_manifest = HOST_MANIFESTS[host]
    files = shared_files(plugin)
    files.append((plugin / source_manifest, archive_manifest))
    canonical_hooks = plugin / "hooks" / "hooks.json"
    if canonical_hooks.is_file():
        source_hooks, archive_hooks = HOST_HOOKS[host]
        files.append((plugin / source_hooks, archive_hooks))
    return sorted(files, key=lambda item: item[1])


def validate_adapters(plugin: Path) -> None:
    missing = [source for source, _ in HOST_MANIFESTS.values() if not (plugin / source).is_file()]
    canonical_hooks = plugin / "hooks" / "hooks.json"
    if canonical_hooks.is_file():
        missing.extend(
            source for source, _ in HOST_HOOKS.values()
            if not (plugin / source).is_file()
        )
    if missing:
        raise SystemExit(
            f"export: {plugin.name} is missing generated adapters: {', '.join(sorted(set(missing)))}"
        )


def zip_info(archive_name: str, executable: bool) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    mode = 0o755 if executable else 0o644
    info.external_attr = (stat.S_IFREG | mode) << 16
    return info


def archive_payload(path: Path) -> bytes:
    """Canonicalize text newlines so Windows and POSIX builds are identical."""
    payload = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES:
        payload = payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return payload


def build_archive(name: str, host: str, out: Path) -> dict:
    plugin = PLUGINS / name
    if not plugin.is_dir():
        raise SystemExit(f"export: no plugin '{name}'")
    if host not in HOSTS:
        raise SystemExit(f"export: unsupported host '{host}'")
    validate_adapters(plugin)
    manifest = read_manifest(plugin)
    version = manifest["version"]
    filename = f"{name}-{version}-{host}.zip"
    destination = out / filename
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w") as archive:
        for path, rel in package_files(plugin, host):
            executable = bool(path.stat().st_mode & stat.S_IXUSR)
            archive.writestr(
                zip_info(f"{name}/{rel}", executable),
                archive_payload(path),
                compresslevel=9,
            )
        compatibility = ROOT / "COMPATIBILITY.md"
        if compatibility.is_file():
            archive.writestr(
                zip_info(f"{name}/COMPATIBILITY.md", False),
                archive_payload(compatibility),
                compresslevel=9,
            )
    payload = destination.read_bytes()
    return {
        "file": filename,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
    }


def build_plugin(name: str, out: Path) -> dict:
    plugin = PLUGINS / name
    if not plugin.is_dir():
        raise SystemExit(f"export: no plugin '{name}'")
    validate_adapters(plugin)
    manifest = read_manifest(plugin)
    return {
        "name": name,
        "version": manifest["version"],
        "skills": (plugin / "skills").is_dir(),
        "hooks": (plugin / "hooks" / "hooks.json").is_file(),
        "packages": {host: build_archive(name, host, out) for host in HOSTS},
    }


def build_archives(names: list[str], out: Path, clean: bool = False) -> list[dict]:
    out.mkdir(parents=True, exist_ok=True)
    if clean:
        for stale in out.glob("*.zip"):
            stale.unlink()
    plugins = [build_plugin(name, out) for name in names]
    index = {
        "schema": "foundry.packages/2",
        "format": "host-native-plugin-zips",
        "hosts": HOSTS,
        "plugins": plugins,
    }
    (out / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return plugins


def display_path(path: Path) -> Path:
    return path.relative_to(ROOT) if path.is_relative_to(ROOT) else path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plugin", nargs="?")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    args = parser.parse_args(argv)
    if args.all == bool(args.plugin):
        parser.error("choose exactly one plugin name or --all")
    names = plugin_names() if args.all else [args.plugin]
    plugins = build_archives(names, args.out, clean=args.all)
    for plugin in plugins:
        for host, package in plugin["packages"].items():
            print(
                f"export: {plugin['name']} v{plugin['version']} [{host}] -> "
                f"{display_path(args.out / package['file'])} ({package['bytes']} bytes)"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
