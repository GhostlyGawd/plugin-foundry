---
name: commit-craft
title: Commit Craft
category: workflow
stage: rc
version: null
always_on_tokens: 88
verified: 2026-07-05
components: [skills, hooks]
one_liner: Drafts conventional commits from the staged diff and guards message format at commit time.
tags: [git, conventional-commits, hooks]
created: 2026-07-04
updated: 2026-07-04
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
