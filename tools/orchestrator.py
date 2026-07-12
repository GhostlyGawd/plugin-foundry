#!/usr/bin/env python3
"""orchestrator.py — the chief of staff (MASTER P0.7, ADR-026). Closes G1/G3.

Multi-agent intelligence, single-threaded writes. Agents never push; they
propose changesets into the outbox. Each run this pipeline:

  collect → order by precedence → guard → apply → gates → attributed commit

## The outbox changeset
foundry/agents/outbox/<agent>/<changeset-id>/
  changeset.json   {"id","agent","ts","rationale","changes":[{"path","action"}]}
  files/<path>     full new contents for every add/modify (deletes have none)
Full contents, not diffs: deterministic to apply, reviewable at cat speed.
Changesets enter the outbox inside the proposing agent's own run (workspace
state) or as committed deferrals; ONLY the orchestrator pushes product paths.

## Precedence (charter/AGENTS.md)
guard veto → product → safety/trust (high) → docs/comms/perception (low);
ties break by changeset ts. When two changesets touch the same path, the
higher-precedence one lands and the loser is DEFERRED in place — it re-queues
next run against the new state (G3: the factory never argues with itself in
one landing).

## Verdicts
guard block  → changeset moved to rejected-<id>/ with the verdict (loud).
guard desk   → changeset HELD (.held marker, desk item queued); an operator
               approval at the desk lands it next run; rejection retires it.
gate failure → applied paths restored byte-for-byte, changeset rejected with
               the gate output; the repo never stays red.
land         → one commit PER changeset, authored AS the proposing agent with
               its Agent: trailer (P0.3) — "single attributed commit" means
               one writer serializing per-changeset attributed commits.

CLI: orchestrator.py run [--root DIR] [--mode direct|pr] [--no-beat]
Exit 0 (a clean run, even if everything deferred); 1 on infrastructure errors.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import load_agents  # noqa: E402
import guard as guard_mod  # noqa: E402
import desk as desk_mod  # noqa: E402

OUTBOX = os.path.join("foundry", "agents", "outbox")
PRECEDENCE = {"product": 0, "high": 1, "low": 2}
GATES = (("validate", ["tools/validate.py"]),
         ("state", ["tools/validate_state.py"]),
         ("build", ["tools/build.py"]))


def _say(msg):
    print(f"orchestrate: {msg}")


def _run(root, args):
    return subprocess.run([sys.executable] + args, cwd=root,
                          capture_output=True, text=True)


def _git(root, *args, check=True):
    return subprocess.run(["git", "-C", root] + list(args),
                          capture_output=True, text=True, check=check)


def collect(root):
    """Yield (agent_id, cs_dir, meta) for every well-formed pending changeset."""
    base = os.path.join(root, OUTBOX)
    out = []
    if not os.path.isdir(base):
        return out
    for agent_id in sorted(os.listdir(base)):
        adir = os.path.join(base, agent_id)
        if not os.path.isdir(adir):
            continue
        for cid in sorted(os.listdir(adir)):
            if cid.startswith("rejected-") or cid.startswith("landed-"):
                continue
            cdir = os.path.join(adir, cid)
            mf = os.path.join(cdir, "changeset.json")
            if not os.path.isfile(mf):
                continue
            try:
                meta = json.load(open(mf, encoding="utf-8"))
            except (OSError, ValueError) as e:
                _say(f"SKIP {agent_id}/{cid} — unreadable changeset.json ({e})")
                continue
            if (not isinstance(meta, dict) or meta.get("agent") != agent_id
                    or not isinstance(meta.get("changes"), list) or not meta["changes"]):
                _say(f"SKIP {agent_id}/{cid} — malformed (agent mismatch or no changes)")
                continue
            out.append((agent_id, cdir, meta))
    return out


def _reject(root, cdir, why):
    dst = os.path.join(os.path.dirname(cdir),
                       f"rejected-{os.path.basename(cdir)}")
    shutil.move(cdir, dst)
    with open(os.path.join(dst, "verdict.txt"), "w", encoding="utf-8") as f:
        f.write(why + "\n")
    return dst


def _apply(root, cdir, changes):
    """Apply changes; return (applied, saved) for byte-exact revert."""
    applied, saved = [], {}
    for ch in changes:
        path, action = ch["path"], ch.get("action", "modify")
        dst = os.path.normpath(os.path.join(root, path))
        if not dst.startswith(os.path.normpath(root) + os.sep):
            raise ValueError(f"path escapes root: {path}")
        if os.path.isfile(dst):
            saved[path] = open(dst, "rb").read()
        else:
            saved[path] = None
        if action == "delete":
            if os.path.isfile(dst):
                os.remove(dst)
        else:
            src = os.path.join(cdir, "files", path)
            if not os.path.isfile(src):
                raise ValueError(f"changeset missing files/{path}")
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
        applied.append(path)
    return applied, saved


def _revert(root, saved):
    for path, blob in saved.items():
        dst = os.path.join(root, path)
        if blob is None:
            if os.path.isfile(dst):
                os.remove(dst)
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "wb") as f:
                f.write(blob)


def _gates(root):
    for name, args in GATES:
        r = _run(root, args)
        if r.returncode != 0:
            return name, (r.stdout + r.stderr)[-2000:]
    return None, ""


def _desk_state(root, title):
    items = desk_mod.read_items(os.path.join(root, "state", "DESK.jsonl"))
    for it in items.values():
        if it.get("title") == title:
            return it.get("status"), it.get("id")
    return None, None


def run(root, mode="direct", beat=True):
    errors = []
    agents = {a["id"]: a for a in load_agents(errors, root)}
    if errors:
        _say("registry unlawful — refusing to run (fail closed):")
        for e in errors:
            _say(f"  ✗ {e}")
        return 1

    pending = collect(root)
    order = sorted(pending, key=lambda t: (
        PRECEDENCE.get(agents.get(t[0], {}).get("quota_tier"), 9),
        str(t[2].get("ts", "~"))))

    claimed, landed, deferred = {}, 0, 0
    bookkeeping = False
    for agent_id, cdir, meta in order:
        cid = os.path.basename(cdir)
        label = f"{agent_id}/{cid}"
        changes = meta["changes"]
        paths = [c.get("path", "") for c in changes]

        # conflict: a higher-precedence changeset already claimed a path
        clash = [p for p in paths if p in claimed]
        if clash:
            _say(f"DEFER {label} — {clash[0]} claimed by {claimed[clash[0]]} "
                 f"(precedence); re-queues next run")
            deferred += 1
            continue

        verdict, verdicts = guard_mod.check(agent_id, changes, root)
        if verdict == guard_mod.BLOCK:
            why = "guard BLOCK:\n" + "\n".join(
                f"{v.upper()} {p} — {r}" for p, v, r in verdicts)
            _reject(root, cdir, why)
            _say(f"REJECT {label} — guard block ({verdicts[0][2]})")
            bookkeeping = True
            continue
        if verdict == guard_mod.DESK:
            desk_paths = [p for p, v, _ in verdicts if v == guard_mod.DESK]
            title = f"ratify: {agent_id} → {', '.join(desk_paths[:3])}" + (
                "…" if len(desk_paths) > 3 else "")
            status, iid = _desk_state(root, title)
            if status == "approved":
                _say(f"desk item {iid} approved — landing {label}")
            elif status == "rejected":
                _reject(root, cdir, f"desk item {iid} rejected by the operator")
                _say(f"REJECT {label} — desk rejected ({iid})")
                bookkeeping = True
                continue
            else:
                if status is None:
                    iid, _fresh = desk_mod.add(
                        "ratify", title,
                        "\n".join(f"{v.upper()} {p} — {r}" for p, v, r in verdicts),
                        agent_id,
                        path=os.path.join(root, "state", "DESK.jsonl"))
                open(os.path.join(cdir, ".held"), "w", encoding="utf-8").write(
                    f"desk:{iid}\n")
                _say(f"HOLD {label} — desk item {iid} awaits the operator")
                bookkeeping = True
                continue

        try:
            applied, saved = _apply(root, cdir, changes)
        except ValueError as e:
            _reject(root, cdir, f"apply error: {e}")
            _say(f"REJECT {label} — {e}")
            bookkeeping = True
            continue

        gate, output = _gates(root)
        if gate:
            _revert(root, saved)
            _reject(root, cdir, f"gate '{gate}' failed:\n{output}")
            _say(f"REJECT {label} — gate '{gate}' red; repo restored")
            bookkeeping = True
            continue

        # land: stage applied paths + the consumed changeset, commit AS the agent
        held = os.path.join(cdir, ".held")
        if os.path.isfile(held):
            os.remove(held)
        shutil.rmtree(cdir)
        # check=False: an untracked (never-committed) changeset dir leaves no
        # deletion to stage, and git add 128s on a pathspec matching nothing
        _git(root, "add", "-A", "--", *applied, check=False)
        _git(root, "add", "-A", "--", os.path.relpath(cdir, root), check=False)
        # build.py may have regenerated site/ + INDEX.md + registry — include
        _git(root, "add", "-A", "--", "site", "foundry/INDEX.md",
             "foundry/agents/registry.json", check=False)
        msg = (f"agent({agent_id}): {meta.get('rationale', cid)[:100]}\n\n"
               f"Landed by the orchestrator (P0.7); changeset {cid}.")
        r = _run(root, ["tools/commit.py", "--agent", agent_id, "-m", msg])
        if r.returncode != 0:
            _say(f"REJECT {label} — commit failed: {r.stdout}{r.stderr}")
            _revert(root, saved)
            continue
        for p in paths:
            claimed[p] = label
        landed += 1
        _say(f"LAND {label} — {len(paths)} path(s), committed as {agent_id}")

    if beat:
        _run(root, ["tools/heartbeat.py", "beat", "orchestrator",
                    "--note", f"landed {landed}, deferred {deferred}"])
        bookkeeping = True

    if bookkeeping:
        r = _git(root, "status", "--porcelain", check=False)
        if r.stdout.strip():
            _git(root, "add", "-A", check=False)
            _run(root, ["tools/commit.py", "--agent", "orchestrator",
                        "-m", f"orchestrate: bookkeeping — landed {landed}, "
                              f"deferred {deferred} (rejections/holds/beat)"])

    _say(f"done — landed {landed} · deferred {deferred} · mode {mode}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="orchestrator.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--root", default=".")
    r.add_argument("--mode", choices=["direct", "pr"], default="direct")
    r.add_argument("--no-beat", action="store_true")
    args = ap.parse_args(argv)
    return run(os.path.abspath(args.root), args.mode, beat=not args.no_beat)


if __name__ == "__main__":
    raise SystemExit(main())
