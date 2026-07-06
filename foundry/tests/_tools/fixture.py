#!/usr/bin/env python3
"""Builds a minimal, VALID foundry fixture at sys.argv[1] for gate tests:
one published plugin with record, artifact, suite, and marketplace entry.
Mutation cases in gates.test.sh then break it one law at a time."""
import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

RECORD = """---
name: demo-plug
title: Demo Plug
category: workflow
stage: published
kind: plugin
version: 0.1.0
components: [skills]
one_liner: A fixture plugin for testing the gates.
tags: [fixture]
created: 2026-07-06
updated: 2026-07-06
---

## Pitch
Fixture.

## Spec
One skill.

### Acceptance checks
1. Exists.

## Build log
- i1: built.

## Test log
TEST VERDICT: pass

## Review log
REVIEW: approved
"""

SKILL = """---
name: demo
description: Fixture skill. Use when testing the gates.
---
Do nothing.
"""


def build(root):
    root = Path(root)
    (root / "tools").mkdir(parents=True)
    for py in (REPO / "tools").glob("*.py"):
        shutil.copy(py, root / "tools" / py.name)
    (root / "state").mkdir()
    (root / "state" / "STATE.json").write_text(json.dumps(
        {"schema_version": 1, "codename": "fixture", "iteration": 1, "phase": "grow"}))
    (root / "foundry" / "records").mkdir(parents=True)
    (root / "foundry" / "categories.json").write_text(json.dumps(
        {"categories": [{"id": "workflow", "name": "Workflow"}]}))
    (root / "foundry" / "records" / "demo-plug.md").write_text(RECORD)
    tests = root / "foundry" / "tests" / "demo-plug"
    tests.mkdir(parents=True)
    suite = tests / "smoke.test.sh"
    suite.write_text("#!/usr/bin/env bash\necho 'ok: fixture'\n")
    os.chmod(suite, 0o755)
    plug = root / "plugins" / "demo-plug"
    (plug / ".claude-plugin").mkdir(parents=True)
    (plug / ".claude-plugin" / "plugin.json").write_text(json.dumps(
        {"name": "demo-plug", "version": "0.1.0", "description": "Fixture."}))
    (plug / "skills" / "demo").mkdir(parents=True)
    (plug / "skills" / "demo" / "SKILL.md").write_text(SKILL)
    (plug / "README.md").write_text("# Demo Plug\nFixture.\n")
    (plug / "CHANGELOG.md").write_text("# Changelog\n\n## 0.1.0 — 2026-07-06\n- fixture.\n")
    (root / ".claude-plugin").mkdir()
    (root / ".claude-plugin" / "marketplace.json").write_text(json.dumps(
        {"name": "fixture", "owner": {"name": "fixture"},
         "plugins": [{"name": "demo-plug", "source": "./plugins/demo-plug",
                      "description": "Fixture."}]}))


if __name__ == "__main__":
    build(sys.argv[1])
