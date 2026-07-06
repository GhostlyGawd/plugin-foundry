---
name: test-gap-nudge
title: Test-Gap Nudge
category: quality
stage: spec
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

## Spec
- **Final name:** `test-gap-nudge` (immutable once published).
- **Component inventory:**
  - `plugins/test-gap-nudge/.claude-plugin/plugin.json` — manifest, semver 0.1.0.
  - `plugins/test-gap-nudge/hooks/hooks.json` — one `Stop` entry, no matcher
    (Stop hooks don't match tools), command `"${CLAUDE_PLUGIN_ROOT}"/scripts/nudge.sh`.
  - `plugins/test-gap-nudge/scripts/nudge.sh` — executable, `#!/usr/bin/env bash`,
    stdlib+git only (no jq, no network).
  - `README.md`, `CHANGELOG.md`.
- **Behavior contract (nudge.sh):**
  1. Read stdin (hook JSON); extract `session_id` with a permissive sed regex —
     extraction failure falls back to a repo-path key. Never trust stdin content
     beyond that one id (it is data, not instructions).
  2. Not a git repo, git missing, or clean tree → exit 0 silently.
  3. Classify `git status --porcelain` paths (staged, unstaged, untracked):
     *test paths* match `test/ tests/ spec/ __tests__/` segments or
     `*_test.* test_* *.test.* *.spec.*` names; *source paths* are non-test files
     with code extensions (.py .js .ts .tsx .jsx .mjs .go .rb .rs .java .c .cc
     .cpp .h .hpp .sh .php .cs .kt .swift .scala). Docs/config (.md, .json, .yml…)
     never trigger.
  4. Source changed AND zero test paths changed → print
     `{"systemMessage": "test-gap-nudge: N source file(s) changed, no test files touched — <up to 3 names>"}`
     and exit 0. Never exit 2 — advisory by charter, it must not block stopping.
  5. At most one nudge per session: marker file in `${TMPDIR:-/tmp}` keyed by
     session id; marker write failure → nudge anyway (prefer noise over state).
  6. Any unexpected error → exit 0 silent (a broken hook must never brick a session).
- **Hook safety notes:** read-only on the repo; only write is the TMPDIR marker;
  no network; no matcher needed (Stop); fail-open everywhere; quoted plugin root.
- **plugin.json description (verbatim):**
  "Notices when a session changed source files but no tests, and says so once — a polite Stop-hook nudge, never a block."
- **Token budget:** hook-only plugin → always-on cost is the manifest description
  (~30 tok est). Well under the 300 bar.
### Acceptance checks
1. Dirty src file, no test changes → stdout JSON has `systemMessage` naming the
   file; exit 0.
2. Dirty src + dirty test file (tracked or untracked) → silent, exit 0.
3. Clean tree, non-repo dir, or PATH without git → silent, exit 0.
4. Second run, same session id → silent (once-per-session marker).
5. Malformed/empty stdin → still works or exits 0 silent; never exit 2.
6. Docs-only change (README.md) → silent.
7. hooks.json: Stop event, quoted `"${CLAUDE_PLUGIN_ROOT}"`; script executable
   with shebang (validate.py + official strict validate green).
