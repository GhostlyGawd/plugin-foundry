#!/usr/bin/env bash
# env-doctor SessionStart hook: on a fresh session, do a FAST, read-only check of
# the repo's declared runtime versions (.nvmrc/.node-version, .python-version)
# against what's installed, and print ONE systemMessage line only on a clear
# mismatch. Contract (record spec): exit 0 ALWAYS; read-only; no network; silent
# when versions match, nothing is declared, or ENV_DOCTOR_SILENT=1. The full
# `envcheck` skill does the deep, comprehensive pass with copyable fixes — this
# is the early tripwire, deliberately conservative to never nag on a false match.
set -u
exec 2>/dev/null || true
trap 'exit 0' ERR

# opt-out: one env var silences the hook entirely (the skill still works).
[ "${ENV_DOCTOR_SILENT:-}" = "1" ] && exit 0

# opt-in debug trail: ENV_DOCTOR_DEBUG=1 appends the decision path to a temp log;
# unset, dbg is a no-op — behavior byte-identical.
DBGLOG="${TMPDIR:-/tmp}/env-doctor-debug.log"
dbg() { [ "${ENV_DOCTOR_DEBUG:-}" = "1" ] && printf '%s %s\n' "$(date -u +%FT%TZ 2>/dev/null)" "$*" >> "$DBGLOG" 2>/dev/null; true; }

# resolve the working root from the session cwd if the event provides it, else PWD.
STDIN_DATA=$(cat 2>/dev/null || true)
ROOT=$(printf '%s' "$STDIN_DATA" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
{ [ -n "$ROOT" ] && [ -d "$ROOT" ]; } || ROOT="$PWD"
dbg "root=$ROOT"

python3 - "$ROOT" << 'PY'
import os, re, subprocess, sys, json

root = sys.argv[1]

def read(name):
    try:
        with open(os.path.join(root, name)) as f:
            return f.read()
    except Exception:
        return None

def installed(cmd):
    """(major, minor) of an installed tool, or None if absent/unparseable."""
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=4).stdout
    except Exception:
        return None
    m = re.search(r'(\d+)\.(\d+)', out or "")
    return (int(m.group(1)), int(m.group(2))) if m else None

def declared(s):
    """(major, minor-or-None) parsed from a version file's first number."""
    if not s:
        return None
    m = re.search(r'(\d+)(?:\.(\d+))?', s)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)) if m.group(2) else None)

def mismatch(inst, dec):
    # clear mismatch only: different major, or (minor declared) and installed behind.
    if inst is None or dec is None:
        return False
    if inst[0] != dec[0]:
        return True
    return dec[1] is not None and inst < (dec[0], dec[1])

def fmt(tool, inst, dec):
    want = f"{dec[0]}" + (f".{dec[1]}" if dec[1] is not None else "")
    return f"{tool} {inst[0]}.{inst[1]} (repo wants {want})"

out = []
checks = [
    ("node",   read('.nvmrc') or read('.node-version'), ['node', '-v']),
    ("python", read('.python-version'),                 ['python3', '--version']),
]
for tool, decl_src, ver_cmd in checks:
    dec = declared(decl_src)
    if dec is None:
        continue
    inst = installed(ver_cmd)
    if mismatch(inst, dec):
        out.append(fmt(tool, inst, dec))

if out:
    msg = ("env-doctor: " + "; ".join(out) +
           ' — run "env doctor" for the full check and copyable fixes.')
    print(json.dumps({"systemMessage": msg}))
PY
exit 0
