---
name: test-gap-nudge
title: Test-Gap Nudge
category: quality
stage: idea
version: null
kind: plugin
components: [hooks]
one_liner: A polite Stop-hook that notices source changes with no matching test changes and says so once.
tags: [testing, hooks, discipline]
created: 2026-07-06
updated: 2026-07-06
---

# Test-Gap Nudge

Every team says "changes ship with tests"; every session ends with at least one
source file modified and zero test files touched. The gap is invisible exactly when
it matters — at the end of the session, before the commit. CLAUDE.md exhortations
don't fire at that moment; a hook can.

## Pitch
- **Job:** at session stop, if the working tree has modified source files but no
  modified test files, say so — once, briefly, with the file list.
- **User:** any developer using Claude Code in a repo with a test suite; teams that
  keep "add tests" rules in CLAUDE.md and watch them get ignored.
- **Components:** one `Stop` hook (`hooks/hooks.json` + script). Reads
  `git status --porcelain`, classifies paths by common test conventions
  (`test/`, `tests/`, `spec/`, `*_test.*`, `*.test.*`, `*.spec.*`), prints one
  advisory line when source moved and tests didn't. Exit 0 always — advisory,
  never blocking; silent outside a git repo or when the tree is clean.
- **Why a plugin:** the check must run at Stop time on every session without
  spending always-on context; a CLAUDE.md rule costs tokens every turn and still
  depends on the model remembering at the right moment. A hook fires exactly once,
  exactly then, for zero context cost.
