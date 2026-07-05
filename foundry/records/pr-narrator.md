---
name: pr-narrator
title: PR Narrator
category: workflow
stage: building
version: null
components: [agents]
one_liner: A subagent that turns a branch's commits and diff into a reviewer-ready PR description.
tags: [pull-requests, agents, writing]
created: 2026-07-04
updated: 2026-07-04
---

# PR Narrator

PR descriptions are either empty or novels; reviewers need the middle.

## Pitch
- **Job:** one invocation from branch to honest, skimmable PR description.
- **User:** anyone opening PRs from Claude Code.
- **Components:** one agent (`pr-narrator`) with a tight description so Claude
  invokes it when PRs come up; read-only git tools; template: what/why/how-to-review/
  risk notes.
- **Why a plugin:** first agent-component exercise for the line — different
  frontmatter schema, different review lens.

## Spec
- Name: `pr-narrator` (forever). One skill, `pr`, description (verbatim): "Draft a
  pull-request title and description from this branch's actual commits and diff.
  Use when opening a PR, or the user says write the PR, describe this branch, or
  draft a pull request."
- Behavior: evidence first — `git log --oneline <base>..HEAD` (base = main/master,
  detected) and `git diff --stat <base>...HEAD`; title in conventional form from
  the dominant change; body sections: Summary (why, 2–4 lines) · Changes (grouped
  from real commits) · Test notes (what was actually run — say "none" honestly) ·
  Risk & rollback. Offers `gh pr create` ONLY if gh exists, showing the exact
  command and asking before running. Never pushes, never force-anything.
### Acceptance checks
1. Title/body derive from real commits and diff — zero invented changes.
2. Test-notes section refuses to claim untested things ("none" is a valid answer).
3. gh usage is offer-then-consent with the exact command shown.

## Build log
- i26: manifest, `pr` skill (evidence-first, honest test notes, risk+rollback,
  consent-gated gh), README with recipes incl. the commit-craft pairing, CHANGELOG,
  executable suite.
