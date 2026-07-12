#!/usr/bin/env python3
"""evals.py — merge-blocking agent evals (MASTER P5.2, ADR-030).

The highest-risk agents must never regress silently. Two layers:

1. DETERMINISTIC golden evals (this file runs them, merge-blocking now):
   foundry/evals/<tool>.jsonl — one case per line: an input + the expected
   verdict for a safety tool whose behavior is a pure function today —
   guard.py (constitution) and fence.py (injection scan). A drift in either
   is caught here before it reaches main.

2. LLM-GRADED evals (config-ready; runs when an API key is present):
   foundry/evals/promptfoo.yaml — golden prompts for the agents that reason
   with Claude (red-team, spec-drift, reviewer). Left as a ready config with
   a desk item; the graders bill the API pool, so the operator arms it
   (ADR-031 boundary).

  evals.py run [--root DIR]     exit 0 all pass · 1 any regression
  evals.py list                 show the fixture inventory
Stdlib only. Deterministic.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

EVAL_DIR = os.path.join("foundry", "evals")


def _load_cases(path):
    cases = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            cases.append((n, json.loads(line)))
    return cases


def eval_guard(root):
    """Each case: {changes:[{path,action}], agent, expect: allow|desk|block}."""
    import guard
    results = []
    path = os.path.join(root, EVAL_DIR, "guard.jsonl")
    if not os.path.exists(path):
        return results
    for n, c in _load_cases(path):
        verdict, _ = guard.check(c.get("agent", "foundry-loop"), c["changes"], root)
        ok = verdict == c["expect"]
        results.append((ok, f"guard#{n} {c.get('note', '')}: "
                            f"expected {c['expect']}, got {verdict}"))
    return results


def eval_fence(root):
    """Each case: {text, expect_risk: none|high}."""
    import fence
    results = []
    path = os.path.join(root, EVAL_DIR, "fence.jsonl")
    if not os.path.exists(path):
        return results
    for n, c in _load_cases(path):
        risk, findings = fence.scan(c["text"])
        ok = risk == c["expect_risk"]
        results.append((ok, f"fence#{n} {c.get('note', '')}: "
                            f"expected {c['expect_risk']}, got {risk} "
                            f"({','.join(findings) or 'clean'})"))
    return results


EVALUATORS = {"guard": eval_guard, "fence": eval_fence}


def run(root):
    total = passed = 0
    failures = []
    for name, fn in EVALUATORS.items():
        results = fn(root)
        for ok, msg in results:
            total += 1
            if ok:
                passed += 1
            else:
                failures.append(msg)
    print(f"evals: {passed}/{total} golden cases pass")
    for f in failures:
        print(f"evals:   ✗ {f}")
    # LLM-graded layer: report readiness, never fail the gate on it. Auth is
    # asked of the single surface (auth.py), never read from the env directly.
    pf = os.path.join(root, EVAL_DIR, "promptfoo.yaml")
    if os.path.exists(pf):
        import auth
        armed = auth.mode() == "api"
        print(f"evals: llm-graded suite {'ARMED (run: npx promptfoo eval)' if armed else 'config-ready (needs ANTHROPIC_API_KEY — desk-gated)'}")
    return 0 if not failures else 1


def main(argv=None):
    ap = argparse.ArgumentParser(prog="evals.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--root", default=".")
    lst = sub.add_parser("list")
    lst.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    if args.cmd == "list":
        for name in EVALUATORS:
            p = os.path.join(args.root, EVAL_DIR, f"{name}.jsonl")
            n = len(_load_cases(p)) if os.path.exists(p) else 0
            print(f"evals: {name} — {n} golden cases")
        return 0
    return run(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
