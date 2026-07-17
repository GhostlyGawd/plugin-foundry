#!/usr/bin/env python3
"""validate.py — the gate. Enforces the sync laws between foundry/records/,
plugins/<name>/, and .claude-plugin/marketplace.json, plus structural checks on the
shipping artifacts and the generated cross-host manifests. Stdlib only,
legible at cat speed."""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "foundry" / "records"
PLUGINS = ROOT / "plugins"

REQUIRED_KEYS = ["name", "title", "category", "stage", "version", "components",
                 "one_liner", "tags", "created", "updated"]
STAGES = ["idea", "spec", "building", "rc", "published", "deprecated", "shelved"]
PLUGIN_COMPONENTS = {"skills", "agents", "hooks", "mcp", "lsp", "output-styles"}
FEATURE_COMPONENTS = {"site", "workflow", "template", "worker", "docs"}
# Cumulative record sections down the line.
STAGE_SECTIONS = {
    "idea":      ["## Pitch"],
    "spec":      ["## Spec", "### Acceptance checks"],
    "building":  ["## Build log"],
    "rc":        ["## Test log"],
    "published": ["## Review log"],
}
STAGE_ORDER = ["idea", "spec", "building", "rc", "published"]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HOOK_EVENTS = {
    "SessionStart", "Setup", "UserPromptSubmit", "UserPromptExpansion", "PreToolUse",
    "PermissionRequest", "PermissionDenied", "PostToolUse", "PostToolUseFailure",
    "PostToolBatch", "Notification", "MessageDisplay", "SubagentStart", "SubagentStop",
    "TaskCreated", "TaskCompleted", "Stop", "StopFailure", "TeammateIdle",
    "InstructionsLoaded", "ConfigChange", "CwdChanged", "FileChanged",
    "WorktreeCreate", "WorktreeRemove", "PreCompact", "PostCompact",
    "Elicitation", "ElicitationResult", "SessionEnd",
}
HOOK_TYPES = {"command", "http", "mcp_tool", "prompt", "agent"}
SENSITIVE_ARTIFACT_RE = re.compile(
    r"(^|/)(\.env($|\.)|id_(rsa|dsa|ecdsa|ed25519)$|credentials\.json$|"
    r"service-account\.json$|[^/]+\.(pem|key|p12|pfx|jks)$)", re.I
)
NETWORK_SCRIPT_RE = re.compile(
    r"https?://|\b(curl|wget|nc|ncat|ssh|scp|sftp)\b|"
    r"\b(urllib|requests)\b|\bfetch\s*\(", re.I
)


from lib import parse_front_matter  # noqa: E402 — one parser, one truth (v10 #8)


def cumulative_sections(stage):
    out = []
    for s in STAGE_ORDER:
        out += STAGE_SECTIONS[s]
        if s == stage:
            break
    return out


def load_json(path, errors, label):
    try:
        return json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{label}: unreadable JSON ({exc})")
        return None


def check_plugin_artifact(name, record, errors):
    """Structural checks on plugins/<name>/ for stage building and beyond."""
    pdir = PLUGINS / name
    label = f"plugins/{name}"
    if not pdir.is_dir():
        errors.append(f"{label}: directory missing (record stage requires a build)")
        return None
    # Package inputs must be ordinary, inspectable files. Symlinks can point the
    # exporter outside the plugin tree; credential-shaped filenames are never a
    # legitimate shipping surface.
    for artifact in sorted(pdir.rglob("*")):
        rel = artifact.relative_to(pdir).as_posix()
        if artifact.is_symlink():
            errors.append(f"{label}/{rel}: symlinks are forbidden in shipped plugins")
        if artifact.is_file() and SENSITIVE_ARTIFACT_RE.search(rel):
            errors.append(f"{label}/{rel}: credential-shaped file must not ship")
    manifest_path = pdir / ".claude-plugin" / "plugin.json"
    manifest = load_json(manifest_path, errors, f"{label}/.claude-plugin/plugin.json")
    if manifest is None:
        return None
    if manifest.get("name") != name:
        errors.append(f"{label}: manifest name {manifest.get('name')!r} != record/dir name {name!r}")
    if not NAME_RE.match(manifest.get("name", "")):
        errors.append(f"{label}: manifest name must be kebab-case")
    ver = manifest.get("version")
    if ver is not None and not SEMVER_RE.match(str(ver)):
        errors.append(f"{label}: version {ver!r} is not semver")
    # Only plugin.json belongs inside .claude-plugin/.
    for stray in (pdir / ".claude-plugin").iterdir():
        if stray.name != "plugin.json":
            errors.append(f"{label}/.claude-plugin/{stray.name}: only plugin.json belongs here")
    # Manifest paths must be relative ./
    for field in ("skills", "commands", "agents", "hooks", "mcpServers", "outputStyles", "lspServers"):
        val = manifest.get(field)
        paths = val if isinstance(val, list) else [val] if isinstance(val, str) else []
        for p in paths:
            if isinstance(p, str) and not p.startswith("./"):
                errors.append(f"{label}: manifest {field} path {p!r} must start with ./")
    # Skills / commands frontmatter.
    for skill_md in sorted(pdir.glob("skills/*/SKILL.md")):
        meta, _ = parse_front_matter(skill_md.read_text(), errors, str(skill_md.relative_to(ROOT)))
        for key in ("name", "description"):
            if not meta.get(key):
                errors.append(f"{skill_md.relative_to(ROOT)}: frontmatter missing {key!r}")
    for cmd_md in sorted(pdir.glob("commands/*.md")):
        meta, _ = parse_front_matter(cmd_md.read_text(), errors, str(cmd_md.relative_to(ROOT)))
        if not meta.get("description"):
            errors.append(f"{cmd_md.relative_to(ROOT)}: frontmatter missing 'description'")
    for agent_md in sorted(pdir.glob("agents/*.md")):
        meta, _ = parse_front_matter(agent_md.read_text(), errors, str(agent_md.relative_to(ROOT)))
        for key in ("name", "description"):
            if not meta.get(key):
                errors.append(f"{agent_md.relative_to(ROOT)}: frontmatter missing {key!r}")
    # Claude/Open Plugin hooks. A manifest path overrides hooks/hooks.json; the
    # latter may intentionally hold Gemini's native lifecycle map.
    hook_ref = manifest.get("hooks")
    hooks_path = (pdir / hook_ref[2:]) if isinstance(hook_ref, str) \
        and hook_ref.startswith("./") else pdir / "hooks" / "hooks.json"
    if hooks_path.exists():
        hooks_cfg = load_json(hooks_path, errors, str(hooks_path.relative_to(ROOT)))
        if hooks_cfg is not None:
            for event, entries in (hooks_cfg.get("hooks") or {}).items():
                if event not in HOOK_EVENTS:
                    errors.append(f"{label}: unknown hook event {event!r} (case-sensitive)")
                for entry in entries or []:
                    if entry.get("matcher") == ".*":
                        errors.append(f"{label}: hook matcher '.*' is banned (QUALITY.md)")
                    for h in entry.get("hooks", []):
                        if h.get("type") not in HOOK_TYPES:
                            errors.append(f"{label}: unknown hook type {h.get('type')!r}")
                        cmd = h.get("command", "")
                        if "${CLAUDE_PLUGIN_ROOT}" in cmd and '"${CLAUDE_PLUGIN_ROOT}' not in cmd:
                            errors.append(f"{label}: unquoted ${{CLAUDE_PLUGIN_ROOT}} in hook command")
    # Scripts must be executable with shebangs.
    for script in sorted(pdir.glob("scripts/*")):
        if script.is_file():
            rel = script.relative_to(ROOT)
            if not os.access(script, os.X_OK):
                errors.append(f"{rel}: not executable (chmod +x)")
            first = script.read_text(errors="replace").splitlines()[:1]
            if not first or not first[0].startswith("#!"):
                errors.append(f"{rel}: missing shebang")
            if NETWORK_SCRIPT_RE.search(script.read_text(errors="replace")):
                errors.append(f"{rel}: network-capable code is forbidden in shipped scripts")
    # Never ship process files.
    for junk in ("FOUNDRY.md", "record.md", "TESTLOG.md"):
        if (pdir / junk).exists():
            errors.append(f"{label}/{junk}: process files must not ship inside the plugin")
    return manifest


def check_record(path, tax, seen, errors):
    label = str(path.relative_to(ROOT))
    meta, body = parse_front_matter(path.read_text(), errors, label)
    for key in REQUIRED_KEYS:
        if key not in meta:
            errors.append(f"{label}: front matter missing {key!r}")
    name, stage = meta.get("name", ""), meta.get("stage", "")
    if name:
        if not NAME_RE.match(name):
            errors.append(f"{label}: name {name!r} must be kebab-case")
        if path.stem != name:
            errors.append(f"{label}: filename must be {name}.md")
        if name in seen:
            errors.append(f"{label}: duplicate record for {name}")
        seen[name] = meta
    if meta.get("category") not in {c["id"] for c in tax["categories"]}:
        errors.append(f"{label}: category {meta.get('category')!r} not in taxonomy")
    if stage not in STAGES:
        errors.append(f"{label}: stage {stage!r} not in {STAGES}")
    kind = meta.get("kind", "plugin")
    if kind not in ("plugin", "feature"):
        errors.append(f"{label}: kind must be plugin|feature")
    allowed = PLUGIN_COMPONENTS if kind == "plugin" else FEATURE_COMPONENTS
    for comp in meta.get("components", []):
        if comp not in allowed:
            errors.append(f"{label}: unknown {kind} component {comp!r}")
    for key in ("created", "updated"):
        if meta.get(key) and not DATE_RE.match(meta[key]):
            errors.append(f"{label}: {key} must be YYYY-MM-DD")
    if meta.get("verified") and not DATE_RE.match(str(meta["verified"])):
        errors.append(f"{label}: verified must be YYYY-MM-DD")
    if meta.get("always_on_tokens") and not str(meta["always_on_tokens"]).isdigit():
        errors.append(f"{label}: always_on_tokens must be an integer")

    # Section gates.
    if stage in STAGE_ORDER:
        needed = cumulative_sections(stage)
    elif stage == "deprecated":
        needed = cumulative_sections("published") + ["## Deprecation"]
    elif stage == "shelved":
        needed = ["## Pitch", "## Shelf note"]
    else:
        needed = []
    for section in needed:
        if section not in body:
            errors.append(f"{label}: stage {stage!r} requires section {section!r}")
    if stage == "shelved" and "Revival trigger" not in body:
        errors.append(f"{label}: Shelf note must name a Revival trigger")
    if stage in ("rc", "published") and "TEST VERDICT: pass" not in body:
        errors.append(f"{label}: stage {stage} requires 'TEST VERDICT: pass' in Test log")
    if stage == "published" and "REVIEW: approved" not in body:
        errors.append(f"{label}: published requires 'REVIEW: approved' in Review log")

    # Feature experiment gates (charter/GROWTH.md).
    if kind == "feature":
        order = STAGE_ORDER.index(stage) if stage in STAGE_ORDER else 99
        if stage == "deprecated" or order >= STAGE_ORDER.index("spec"):
            if "## Experiment" not in body:
                errors.append(f"{label}: kind:feature requires '## Experiment' from spec onward")
            elif "Hypothesis" not in body:
                errors.append(f"{label}: Experiment section must state a Hypothesis")
        if "VERDICT: kill" in body and stage != "deprecated":
            errors.append(f"{label}: killed experiment must move to stage deprecated")

    # Artifact gates (plugins only).
    if kind == "feature":
        return
    if stage in ("building", "rc", "published"):
        manifest = check_plugin_artifact(name, meta, errors)
        if stage in ("rc", "published"):
            for req in ("README.md", "CHANGELOG.md"):
                if not (PLUGINS / name / req).exists():
                    errors.append(f"plugins/{name}: missing {req} (required at {stage})")
            tests = ROOT / "foundry" / "tests" / name
            has_exec = tests.is_dir() and any(
                p.suffix == ".sh" and os.access(p, os.X_OK) for p in tests.glob("*.test.sh"))
            if not has_exec:
                errors.append(
                    f"foundry/tests/{name}: {stage} requires at least one executable "
                    f"*.test.sh (run: bash tools/qa.sh {name})")
        if stage == "published" and manifest is not None:
            ver = str(manifest.get("version", ""))
            if not SEMVER_RE.match(ver):
                errors.append(f"plugins/{name}: published requires a semver version in plugin.json")
            if meta.get("version") != ver:
                errors.append(f"{label}: record version {meta.get('version')!r} != plugin.json {ver!r}")
            changelog = (PLUGINS / name / "CHANGELOG.md")
            if changelog.exists() and ver and ver not in changelog.read_text().split("\n## ")[0] + \
                    ("".join(changelog.read_text().split("\n## ")[1:2])):
                errors.append(f"plugins/{name}: CHANGELOG top entry doesn't mention version {ver}")


def check_kits(seen, errors):
    path = ROOT / "foundry" / "kits.json"
    if not path.exists():
        return
    try:
        kits = json.loads(path.read_text()).get("kits", [])
    except Exception as exc:  # noqa: BLE001
        errors.append(f"kits.json: unreadable ({exc})")
        return
    for kit in kits:
        for member in kit.get("plugins", []):
            if member not in seen:
                errors.append(f"kits.json: kit {kit.get('id')!r} references unknown plugin {member!r}")


def check_clerk_snapshot(seen, errors):
    """ADR-016 #2: night-clerk's bundled catalog may never trail the shelf.
    Every published plugin must appear in the snapshot (and no ghosts), or the
    front desk recommends from a stale shelf. Skips cleanly if night-clerk is
    absent or no longer published."""
    clerk = seen.get("night-clerk")
    if not clerk or clerk.get("stage") != "published":
        return
    path = ROOT / "plugins" / "night-clerk" / "data" / "catalog.json"
    try:
        snap = {p["name"] for p in json.loads(path.read_text()).get("plugins", [])}
    except Exception as exc:  # noqa: BLE001
        errors.append(f"night-clerk catalog: unreadable ({exc})")
        return
    shelf = {n for n, m in seen.items()
             if m.get("stage") == "published" and m.get("kind", "plugin") == "plugin"}
    for name in sorted(shelf - snap):
        errors.append(f"night-clerk catalog: stale — published plugin {name!r} missing "
                      f"(run tools/clerkcat.py inside a night-clerk version bump)")
    for name in sorted(snap - shelf):
        errors.append(f"night-clerk catalog: ghost — {name!r} in snapshot but not published")


def check_marketplace(seen, errors):
    mp = load_json(ROOT / ".claude-plugin" / "marketplace.json", errors, "marketplace.json")
    if mp is None:
        return
    for key in ("name", "owner", "plugins"):
        if key not in mp:
            errors.append(f"marketplace.json: missing {key!r}")
    listed = {}
    for entry in mp.get("plugins", []):
        n = entry.get("name", "")
        listed[n] = entry
        if entry.get("source") != f"./plugins/{n}":
            errors.append(f"marketplace.json: {n} source should be ./plugins/{n}")
        if n not in seen:
            errors.append(f"marketplace.json: {n} listed but has no foundry record")
        elif seen[n].get("stage") != "published":
            errors.append(f"marketplace.json: {n} listed but record stage is {seen[n].get('stage')!r}")
    for name, meta in seen.items():
        if meta.get("stage") == "published" and meta.get("kind", "plugin") == "plugin" \
                and name not in listed:
            errors.append(f"{name}: record says published but missing from marketplace.json")
        if meta.get("stage") in ("deprecated", "shelved") and name in listed:
            errors.append(f"{name}: stage {meta['stage']} must not be in marketplace.json")


def check_agent_trailer(errors):
    """P0.3 (ADR-026): a commit authored under a registered agent identity must
    carry a matching `Agent: <id>` trailer — attribution never collapses (G7).
    Checks HEAD only; human/operator commits and repos without git are exempt."""
    import subprocess
    id_path = ROOT / "foundry" / "agents" / "identities.json"
    if not id_path.exists():
        return
    try:
        identities = json.loads(id_path.read_text())
        by_email = {v["email"]: k for k, v in identities.items()
                    if isinstance(v, dict) and v.get("email")}
        r = subprocess.run(["git", "-C", str(ROOT), "log", "-1",
                            "--format=%ae%n%B"],
                           capture_output=True, text=True, timeout=10)
        if r.returncode != 0 or not r.stdout.strip():
            return
        email, _, body = r.stdout.partition("\n")
        agent = by_email.get(email.strip())
        if agent is None:
            return
        trailers = [ln.strip() for ln in body.splitlines()
                    if ln.strip().startswith("Agent:")]
        if f"Agent: {agent}" not in trailers:
            errors.append(f"HEAD commit authored as agent '{agent}' "
                          f"({email.strip()}) lacks its 'Agent: {agent}' trailer "
                          f"— commit via tools/commit.py")
    except Exception:  # noqa: BLE001 — no git, shallow clone, etc.: not our gate
        return


def check_cross_host_adapters(errors):
    """Keep full-repo adapters strict without burdening minimal gate fixtures."""
    if not (ROOT / "tools" / "adapters.py").is_file() \
            or not (ROOT / "COMPATIBILITY.md").is_file():
        return
    try:
        import adapters
        for path, expected in adapters.expected_files().items():
            if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                rel = path.relative_to(ROOT).as_posix()
                errors.append(
                    f"{rel}: cross-host adapter drift "
                    "(run python3 tools/adapters.py --write)"
                )
    except Exception as exc:  # noqa: BLE001 — malformed adapter data is a gate failure
        errors.append(f"cross-host adapter validation failed: {exc}")


def main():
    errors = []
    state = load_json(ROOT / "state" / "STATE.json", errors, "STATE.json")
    if state and state.get("phase") not in ("bootstrap", "grow"):
        errors.append("STATE.json: phase must be bootstrap|grow")
    tax = load_json(ROOT / "foundry" / "categories.json", errors, "categories.json")
    if tax is None:
        print("VALIDATE: FAIL — taxonomy unreadable")
        sys.exit(1)

    records = sorted(RECORDS.glob("*.md"))
    if not records:
        errors.append("foundry/records: no records found")
    seen = {}
    for path in records:
        check_record(path, tax, seen, errors)
    # Orphan plugins (artifact with no record).
    if PLUGINS.is_dir():
        for pdir in sorted(PLUGINS.iterdir()):
            if pdir.is_dir() and pdir.name not in seen:
                errors.append(f"plugins/{pdir.name}: no foundry record (every artifact needs its traveler)")
    check_marketplace(seen, errors)
    check_kits(seen, errors)
    check_clerk_snapshot(seen, errors)
    check_cross_host_adapters(errors)
    check_agent_trailer(errors)

    if errors:
        print(f"VALIDATE: FAIL — {len(errors)} problem(s)")
        for err in errors:
            print(f"  ✗ {err}")
        sys.exit(1)
    published = sum(1 for m in seen.values() if m.get("stage") == "published")
    print(f"VALIDATE: OK — {len(records)} records, {published} published, sync laws hold")


if __name__ == "__main__":
    main()
