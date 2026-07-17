#!/usr/bin/env bash
# Native packaging tests: each host gets only the manifest/hook schema it owns;
# every archive is deterministic and derived without mutating shared source.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

# 1 — exporting a plugin yields five versioned archives and a per-host index.
out=$(cd "$REPO" && python3 tools/export.py commit-craft --out "$WORK/one")
count=$(find "$WORK/one" -maxdepth 1 -name 'commit-craft-*.zip' | wc -l | tr -d ' ')
if [ "$count" = 5 ] && python3 - "$WORK/one/index.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
assert d["schema"] == "foundry.packages/2", d
assert d["format"] == "host-native-plugin-zips", d
assert len(d["hosts"]) == 5 and len(d["plugins"]) == 1, d
p = d["plugins"][0]
assert p["name"] == "commit-craft", p
assert set(p["packages"]) == set(d["hosts"]), p
PY
then echo "ok: exports five indexed host-native packages"
else echo "fail: native export — $out"; fi

# 2 — each archive carries only its native manifest/hook map plus shared code.
python3 - "$WORK/one" <<'PY' \
  && echo "ok: archives isolate native manifests and share behavior" \
  || echo "fail: native archive inventory"
import glob, json, os, sys, zipfile

out = sys.argv[1]
root = "commit-craft/"
expectations = {
    "claude-code": (".claude-plugin/plugin.json", "hooks/hooks.json", "PreToolUse", "CLAUDE_PLUGIN_ROOT"),
    "codex": (".codex-plugin/plugin.json", "hooks/codex.json", "PreToolUse", "PLUGIN_ROOT"),
    "gemini-cli": ("gemini-extension.json", "hooks/hooks.json", "BeforeTool", "extensionPath"),
    "cursor": (".cursor-plugin/plugin.json", "hooks/cursor.json", "preToolUse", "CURSOR_PLUGIN_ROOT"),
    "github-copilot": (".github/plugin/plugin.json", "hooks/copilot.json", "PreToolUse", "PLUGIN_ROOT"),
}
all_manifests = {
    ".claude-plugin/plugin.json", ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json", ".github/plugin/plugin.json",
    "gemini-extension.json",
}
for host, (manifest, hooks, event, root_var) in expectations.items():
    matches = glob.glob(os.path.join(out, f"commit-craft-*-{host}.zip"))
    assert len(matches) == 1, (host, matches)
    with zipfile.ZipFile(matches[0]) as archive:
        names = set(archive.namelist())
        assert root + manifest in names, (host, manifest)
        assert root + "skills/commit/SKILL.md" in names, host
        assert root + "scripts/check-commit-msg.sh" in names, host
        script_mode = archive.getinfo(root + "scripts/check-commit-msg.sh").external_attr >> 16
        assert script_mode & 0o111, (host, oct(script_mode))
        assert {root + item for item in all_manifests - {manifest}}.isdisjoint(names), host
        hook_data = json.loads(archive.read(root + hooks))
        assert event in hook_data["hooks"], (host, hook_data)
        assert root_var in archive.read(root + hooks).decode(), host
PY

# 3 — checked-in manifests, hook adapters, and marketplaces cannot drift.
(cd "$REPO" && python3 tools/adapters.py --check >/dev/null) \
  && echo "ok: cross-host adapters are in sync" \
  || echo "fail: adapter drift"

# 4 — export is read-only with respect to the published plugin source.
before=$(cd "$REPO" && git status --porcelain plugins/commit-craft | sort)
(cd "$REPO" && python3 tools/export.py commit-craft --out "$WORK/two" >/dev/null)
after=$(cd "$REPO" && git status --porcelain plugins/commit-craft | sort)
[ "$before" = "$after" ] && echo "ok: export never mutates the plugin source" \
                         || echo "fail: export mutated the plugin"

# 5 — identical source produces byte-identical archives for every host.
python3 - "$WORK/one" "$WORK/two" <<'PY' \
  && echo "ok: host-native archives are deterministic" \
  || echo "fail: archive churns"
import glob, hashlib, os, sys
def hashes(directory):
    return {
        os.path.basename(path): hashlib.sha256(open(path, "rb").read()).hexdigest()
        for path in glob.glob(os.path.join(directory, "*.zip"))
    }
assert hashes(sys.argv[1]) == hashes(sys.argv[2])
PY

# 6 — ZIP text is newline-canonical across Windows and POSIX checkouts.
python3 - "$REPO" "$WORK" <<'PY' \
  && echo "ok: archive text newlines are cross-platform deterministic" \
  || echo "fail: archive newline canonicalization"
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(sys.argv[1]) / "tools"))
from export import archive_payload
sample = pathlib.Path(sys.argv[2]) / "sample.md"
sample.write_bytes(b"one\r\ntwo\rthree\n")
assert archive_payload(sample) == b"one\ntwo\nthree\n"
PY

# 7 — scratch exports remain ignored; public build artifacts live under site/.
grep -q "^dist/" "$REPO/.gitignore" && echo "ok: dist/ remains gitignored" \
                                      || echo "fail: dist/ not ignored"
