---
name: pr-narrator
title: PR Narrator
category: workflow
stage: published
version: 0.1.4
always_on_tokens: 88
verified: 2026-07-13
components: [skills]
one_liner: A skill that turns a branch's commits and diff into a reviewer-ready PR description.
tags: [pull-requests, skills, writing]
created: 2026-07-04
updated: 2026-07-17
---

# PR Narrator

PR descriptions are either empty or novels; reviewers need the middle.

## Pitch
- **Job:** one invocation from branch to honest, skimmable PR description.
- **User:** anyone opening PRs from a supported coding agent.
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

## Test log
### Test pass — i27
- tier 1: pass; smoke: CLI absent locally, official --strict runs in CI (logged)
- tier 2: unavailable locally — always-on cost: 88 tok (est., stamped)
- tier 3: suite 6/6 — evidence-first, honest test notes, risk section, consent-
  gated gh, invoke contract, manifest; acceptance checks 1–3 traced
- defects: none found — probed: base-branch detection order (main→master→ask),
  no push/force verbs anywhere in the skill
TEST VERDICT: pass

## Recipes
- "write the PR" on a finished branch → full draft from commit evidence
- pair with commit-craft: clean commits in, clean narrative out
- "describe this branch for the changelog" → same evidence, changelog voice

## Example session
you> write the PR
pr> base detected: main · evidence: git log main..HEAD (4 commits), diff --stat
pr> title: feat(queue): sanitized public commission board
pr> Test notes: unit suite 5/5; no browser pass — "none" would also be an honest answer
pr> Risk & rollback: additive page; revert the single commit to remove
pr> gh found — run `gh pr create --title ... --body-file /tmp/pr.md`? (y/N)

## Publish log
- i29 (maintainer): marketplace entry, version synced, CHANGELOG dated, tag
  pr-narrator-v0.1.0; curated the git-flow starter kit (commit-craft +
  pr-narrator) per the reviewer's pairing note.

## Review log
### Review — i28 (reviewer)
- Test-notes honesty clause is the differentiator — a PR tool that refuses to
  launder untested work protects reviewers, not just authors.
- Evidence chain airtight: log + stat before any prose; gh is offer-then-consent
  with the literal command shown; zero push verbs.
- Pairs cleanly with commit-craft (clean commits → clean narrative) — kit-worthy.
REVIEW: approved
- i182 (maintainer, v11 #2): v0.1.2 — README Manage section (docs sweep). Tag pr-narrator-v0.1.2.

## Maintenance log
- v13 A1 (relabel, no version bump): this record's front matter called
  pr-narrator an "agent"/"subagent" (`components: [agents]`, `tags:
  [...agents...]`), but it ships one **skill** (`skills/pr/SKILL.md`) — the
  Spec and Build log above always said "one skill". Front matter corrected to
  `components: [skills]`, one-liner and tags to "skill". No file under
  `plugins/pr-narrator/` changed and the installer-facing `plugin.json`
  description was already accurate, so no semver bump is owed; the fix reaches
  the catalog via the B7 clerkcat regeneration. The historical Pitch prose
  (an aspirational "agent-component exercise") is left as written — the line
  never grew a real agent, and that gap is noted for a future idea, not
  rewritten here.
- v13 B6: v0.1.2 → v0.1.3 — README + `pr` skill now pair with dep-bump-brief:
  on a dependency PR, the brief's risk line drops straight into Risk & rollback.
  Docs-only; Tag pr-narrator-v0.1.3.
