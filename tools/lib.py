"""lib.py — shared helpers for the gates (v10 #8, ADR-018). One front-matter
parser, one truth: validate.py consumes it strictly (errors reported),
build.py and clerkcat.py leniently. The _tools fixture suite guards it.

Also home to the agent-contract loader (MASTER.md P0.1, ADR-026,
charter/AGENTS.md): load_agent(), load_agents(), build_agent_registry().
Manifests live at foundry/agents/<id>/agent.json; the registry is generated,
never hand-edited. The loader enforces the schema AND the four hard rules —
a manifest that violates either never enters the registry."""

import json
import os

AGENTS_DIR = "foundry/agents"

_TRIGGERS = ("schedule", "dispatch", "event")
_TRUST_TIERS = ("trusted", "ingests_untrusted")
_QUOTA_TIERS = ("product", "high", "low")
_STATUSES = ("active", "dormant")
_REQUIRED = ("id", "role", "trigger", "trust_tier", "quota_tier",
             "capability", "outputs", "heartbeat")
_OPTIONAL = ("description", "prompt", "workflow", "gates", "lands_via",
             "fenced", "status")
# The direct writers hard rule 1 permits: the product loop (until P0.7
# subsumes it) and the orchestrator itself — the single writer everything
# else lands through (charter/AGENTS.md).
GRANDFATHERED_WRITERS = ("foundry-loop", "orchestrator")


def validate_agent_manifest(m, errors, label):
    """Schema + four-hard-rules check for one agent.json dict.

    Appends 'label: problem' strings to errors; returns True when clean."""
    n0 = len(errors)

    def err(msg):
        errors.append(f"{label}: {msg}")

    if not isinstance(m, dict):
        err("manifest is not a JSON object")
        return False
    for k in _REQUIRED:
        if k not in m:
            err(f"missing required field '{k}'")
    for k in m:
        if k not in _REQUIRED + _OPTIONAL:
            err(f"unknown field '{k}' (schema.json is closed)")
    if len(errors) > n0:
        return False

    aid = m["id"]
    if not isinstance(aid, str) or not aid or not all(
            c.islower() or c.isdigit() or c == "-" for c in aid) or aid[0] == "-":
        err(f"id {aid!r} is not a slug ([a-z0-9-], no leading dash)")
    if not isinstance(m["role"], str) or not m["role"].strip():
        err("role must be a non-empty string")
    if m["trigger"] not in _TRIGGERS:
        err(f"trigger {m['trigger']!r} not one of {_TRIGGERS}")
    if m["trust_tier"] not in _TRUST_TIERS:
        err(f"trust_tier {m['trust_tier']!r} not one of {_TRUST_TIERS}")
    if m["quota_tier"] not in _QUOTA_TIERS:
        err(f"quota_tier {m['quota_tier']!r} not one of {_QUOTA_TIERS}")
    cap = m["capability"]
    writes = isinstance(cap, str) and cap.startswith("writes:") and len(cap) > 7
    if not (cap in ("read_only", "proposes") or writes):
        err(f"capability {cap!r} must be read_only | proposes | writes:<glob>")
    if not isinstance(m["outputs"], list) or not m["outputs"] or not all(
            isinstance(o, str) and o for o in m["outputs"]):
        err("outputs must be a non-empty list of strings")
    hb = m["heartbeat"]
    if not (isinstance(hb, dict) and set(hb) == {"interval_hours"}
            and isinstance(hb.get("interval_hours"), (int, float))
            and hb["interval_hours"] > 0):
        err('heartbeat must be {"interval_hours": N>0}')
    if "status" in m and m["status"] not in _STATUSES:
        err(f"status {m['status']!r} not one of {_STATUSES}")
    if "gates" in m and (not isinstance(m["gates"], list) or not all(
            isinstance(g, str) for g in m["gates"])):
        err("gates must be a list of strings")
    if len(errors) > n0:
        return False

    # Hard rule 1 — single writer: writes: needs lands_via orchestrator,
    # except the grandfathered product loop.
    if writes and aid not in GRANDFATHERED_WRITERS and m.get("lands_via") != "orchestrator":
        err("hard rule 1: capability 'writes:' requires lands_via: "
            "\"orchestrator\" (no agent pushes to main directly)")
    # Hard rule 2 — read/act split: untrusted ingestion never holds a pen,
    # and must be fenced.
    if m["trust_tier"] == "ingests_untrusted":
        if writes:
            err("hard rule 2: ingests_untrusted agents may not hold 'writes:' "
                "capability (read/act split)")
        if m.get("fenced") is not True:
            err("hard rule 2: ingests_untrusted agents must declare "
                "fenced: true (tools/fence.py before any prompt)")
    # Hard rule 3 — writes pass the gates. The grandfathered product loop runs
    # the LOOP.md gates instead until P0.7 subsumes it (charter/AGENTS.md).
    if writes and aid not in GRANDFATHERED_WRITERS:
        gates = set(m.get("gates") or [])
        missing = {"guard", "validate_state"} - gates
        if missing:
            err(f"hard rule 3: 'writes:' capability requires gates "
                f"{sorted(missing)} (guard.py + validate_state.py)")
    return len(errors) == n0


def load_agent(path, errors, root="."):
    """Load + validate one foundry/agents/<id>/agent.json. Returns dict or None."""
    label = os.path.relpath(path, root)
    try:
        with open(path, encoding="utf-8") as f:
            m = json.load(f)
    except (OSError, ValueError) as e:
        errors.append(f"{label}: unreadable manifest ({e})")
        return None
    if validate_agent_manifest(m, errors, label):
        want = os.path.basename(os.path.dirname(path))
        if m["id"] != want:
            errors.append(f"{label}: id {m['id']!r} != directory {want!r}")
            return None
        return m
    return None


def load_agents(errors, root="."):
    """Load every agent manifest under foundry/agents/. Sorted by id."""
    base = os.path.join(root, AGENTS_DIR)
    agents = []
    if not os.path.isdir(base):
        return agents
    for name in sorted(os.listdir(base)):
        mf = os.path.join(base, name, "agent.json")
        if os.path.isfile(mf):
            m = load_agent(mf, errors, root)
            if m:
                agents.append(m)
    return agents


def build_agent_registry(root="."):
    """Regenerate foundry/agents/registry.json (deterministic — no timestamps).

    Returns (count, errors). Refuses to write a registry over errors."""
    errors = []
    agents = load_agents(errors, root)
    if errors:
        return 0, errors
    reg = {"schema": "foundry/agents/schema.json",
           "contract": "charter/AGENTS.md",
           "agents": agents}
    path = os.path.join(root, AGENTS_DIR, "registry.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return len(agents), errors


def parse_front_matter(text, errors=None, label=""):
    """Parse leading ``---`` front matter. Returns ``(meta, body)``.

    Pass ``errors`` (a list) for strict mode: malformed input appends
    ``f"{label}: <problem>"`` messages. Without it, parsing is lenient —
    problems are skipped and the function returns what it can.
    Values in ``[a, b]`` form become lists; inline ``  # comments`` after a
    value are stripped."""
    def err(msg):
        if errors is not None:
            errors.append(f"{label}: {msg}")

    if not text.startswith("---"):
        err("missing front matter")
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        err("unterminated front matter")
        return {}, text
    meta = {}
    for line in parts[1].strip().splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            err(f"bad front matter line: {line!r}")
            continue
        key, _, raw = line.partition(":")
        key, raw = key.strip(), raw.split(" #")[0].strip()
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            meta[key] = [v.strip() for v in inner.split(",") if v.strip()] if inner else []
        else:
            meta[key] = raw
    return meta, parts[2]
