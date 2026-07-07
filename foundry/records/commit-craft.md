---
name: commit-craft
title: Commit Craft
category: workflow
stage: published
version: 0.3.1
always_on_tokens: 88
verified: 2026-07-06
components: [skills, hooks]
one_liner: Drafts conventional commits from the staged diff and guards message format at commit time.
tags: [git, conventional-commits, hooks]
created: 2026-07-04
updated: 2026-07-06
---

# Commit Craft

Commit messages are written in the worst possible moment — after the interesting work
is done. A skill that reads the staged diff and drafts a conventional commit, plus a
gentle hook that catches malformed messages before they land, turns history into
documentation.

## Pitch
- **Job:** every commit conventional, accurate, and effortless.
- **User:** anyone using Claude Code in a repo with commit standards.
- **Components:** one skill (draft the message), one PreToolUse hook (guard the format).
- **Why a plugin:** it pairs a prompt with an enforcement hook — exactly what plugins
  bundle and CLAUDE.md notes can't.

## Spec
- Name: `commit-craft` (forever).
- skills/commit/SKILL.md — description (verbatim): "Draft a conventional commit
  message from the currently staged changes. Use when committing, when asked to write
  a commit message, or after staging changes."
  Body must: run `git diff --staged --stat` then `git diff --staged`; infer type
  (feat|fix|docs|refactor|test|chore|perf) and scope from paths; produce
  `type(scope): imperative summary ≤72 chars` + wrapped body explaining why; never
  invent ticket numbers; if nothing is staged, say so and stop.
- hooks/hooks.json — PreToolUse, matcher `Bash`, type `command`, command
  `"${CLAUDE_PLUGIN_ROOT}"/scripts/check-commit-msg.sh`.
- scripts/check-commit-msg.sh — reads the hook JSON from stdin; acts ONLY if the
  Bash command is a `git commit` with an inline `-m` message; checks the message
  against `^(feat|fix|docs|refactor|test|chore|perf)(\(.+\))?: .{1,72}`; on mismatch
  exits 2 with a one-line reason (blocks with feedback); **exits 0 on any parsing
  doubt — fail open, never brick a commit**; no writes, no network.
- README: install lines, both components explained, how to disable the hook.
- Token budget: ≤200 always-on.
### Acceptance checks
1. With staged changes, the skill produces a valid conventional message that
   truthfully describes the diff.
2. With nothing staged, the skill says so and does not fabricate.
3. Hook script, fed a `git commit -m "bad message"` payload on stdin, exits 2 with a
   reason; fed a conforming message, exits 0.
4. Hook script, fed a non-commit Bash payload and a garbled payload, exits 0 both
   times (fail-open proven).
5. `bash tools/smoke.sh commit-craft` passes; always-on cost within budget.

## Build log
- i10: manifest, `commit` skill, hooks.json (PreToolUse, matcher Bash, quoted
  ${CLAUDE_PLUGIN_ROOT}), scripts/check-commit-msg.sh (fail-open guard), README
  with honest hook disclosure + recipes, CHANGELOG. Bootstrap B2+B3 complete.

## Test log
### Test pass — i11
- tier 1: pass — validate + build green; smoke: claude CLI absent locally, official
  --strict validate runs in the QA workflow (logged per protocol)
- tier 2: unavailable locally — always-on cost: 88 tok (est. via tools/tokencost.py;
  stamped into front matter with verified date)
- tier 3: executable suite foundry/tests/commit-craft green 4/4 — malformed message
  blocked with printed reason (exit 2), conforming message passes, non-commit
  command ignored, garbled payload fails open; hook safety audit: matcher is
  exactly "Bash", script read-only, no network, plugin-root quoted
- defects (this pass): none — i10's two build defects were fixed and journaled;
  probed additionally: single-quoted -m, multiline -m body (first line judged),   git commit --amend without -m (fail-open confirmed)
TEST VERDICT: pass

## Recipes
- "commit this" → skill reads the staged diff, writes `fix(auth): ...`
- "split this into two commits" → partition proposed before anything lands
- type `git commit -m "wip"` yourself → the guard blocks with the reason (try it)

## Example session
you> commit this
commit> staged: 2 files (+41 -6) — reading the diff, not guessing
commit> proposal: fix(intake): fence patron text before it reaches the backlog
commit> committed. (try `git commit -m "wip"` yourself — the guard will explain)

## Publish log
- i14 (maintainer): marketplace entry, version 0.1.0 synced, CHANGELOG dated,
  release tag commit-craft-v0.1.0. The workshop's own commits now pass through the
  guard it just shipped — dogfood law satisfied.

## Review log
### Review — i13 (reviewer)
- Skill: subject/type/body doctrine matches the spec; reads the staged diff before
  writing (no invented messages); refuses to stage secrets; offers commit splits.
- Hook: matcher exactly "Bash" (guest law), read-only, no network, plugin root
  quoted, blocks print a teachable stderr reason, and the fail-open posture is
  disclosed in the README in plain language — the user can see the leash.
- Cross-check: i10's defect story is in the journal, i12's gate fix landed via the
  two-iteration rule — the paper trail around this artifact is its best feature.
- Sharpest question: can the hook block anything but a malformed `git commit -m`?
  No — traced all four exits.
REVIEW: approved

## Maintenance log
- i155 (builder, v10 #2): v0.2.0 — `COMMIT_CRAFT_TYPES` replaces the guard's
  allowed type list; tokens restricted to lowercase letters (regex injection
  structurally impossible), empty/malformed → default. Fail-open unchanged;
  block message names the enforced list; suite +3 checks (override allows,
  injection dropped, default regression). Tag commit-craft-v0.2.0.
- i164 (builder, v10 #10): v0.3.0 — COMMIT_CRAFT_DEBUG=1 decision-trail log in
  TMPDIR; debug-off byte-identical (suite-proven). Tag commit-craft-v0.3.0.
- i182 (maintainer, v11 #2): v0.3.1 — README Manage section (docs sweep). Tag commit-craft-v0.3.1.
