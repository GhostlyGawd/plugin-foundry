#!/usr/bin/env python3
"""specdrift.py — spec-drift auditor (MASTER P3.1, ADR-031).

Ecosystem-aware self-correction: the plugin spec is Anthropic's, not ours
(LOOP.md: docs before invention). If the validator's ENCODED schema and the
last human-verified spec snapshot disagree, either the validator drifted or the
spec moved — and NO schema edit lands without approval (constitution Art. I §5).
This is the deterministic comparator; the agent fetches the live docs (fenced)
and refreshes the snapshot only via the desk.

  specdrift.py check     exit 0 in sync · 1 drift (would desk-queue)
Stdlib only. Deterministic.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import validate  # noqa: E402 — the encoded schema is the source of comparison

SNAP = os.path.join(ROOT, "foundry", "spec-snapshot.json")


def diff():
    """Return a dict of {field: {only_in_validator, only_in_snapshot}} drifts."""
    snap = json.load(open(SNAP, encoding="utf-8"))
    pairs = {
        "hook_events": (validate.HOOK_EVENTS, set(snap["hook_events"])),
        "hook_types": (validate.HOOK_TYPES, set(snap["hook_types"])),
        "plugin_components": (validate.PLUGIN_COMPONENTS, set(snap["plugin_components"])),
    }
    drifts = {}
    for field, (encoded, snapped) in pairs.items():
        only_v = sorted(encoded - snapped)
        only_s = sorted(snapped - encoded)
        if only_v or only_s:
            drifts[field] = {"only_in_validator": only_v, "only_in_snapshot": only_s}
    return drifts, snap


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else "check"
    if cmd != "check":
        print("usage: specdrift.py check")
        return 1
    drifts, snap = diff()
    if not drifts:
        print(f"specdrift: in sync with the spec snapshot "
              f"(verified {snap['verified']}, {snap['source']})")
        return 0
    print("specdrift: DRIFT — validator schema vs the verified spec snapshot:")
    for field, d in drifts.items():
        if d["only_in_validator"]:
            print(f"  {field}: validator has, snapshot lacks → {d['only_in_validator']}")
        if d["only_in_snapshot"]:
            print(f"  {field}: snapshot has, validator lacks → {d['only_in_snapshot']}")
    print("specdrift: this is a DESK item — a human ratifies any schema change "
          "(constitution Art. I §5); never a silent edit.")
    if "--emit" in argv:
        import desk
        desk.add("ratify", "spec-drift: validator schema vs verified spec snapshot",
                 json.dumps(drifts, indent=1), "spec-drift",
                 path=os.path.join(ROOT, "state", "DESK.jsonl"))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
