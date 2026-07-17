---
name: test-gap-nudge
title: Test-Gap Nudge
category: quality
stage: published
version: 0.3.2
kind: plugin
components: [hooks]
one_liner: A polite Stop-hook that notices source changes with no matching test changes and says so once.
tags: [testing, hooks, discipline]
always_on_tokens: 33
verified: 2026-07-13
created: 2026-07-06
updated: 2026-07-17
---

# Test-Gap Nudge

Every team says "changes ship with tests"; every session ends with at least one
source file modified and zero test files touched. The gap is invisible exactly when
it matters — at the end of the session, before the commit. CLAUDE.md exhortations
don't fire at that moment; a hook can.

## Pitch
- **Job:** at session stop, if the working tree has modified source files but no
  modified test files, say so — once, briefly, with the file list.
- **User:** any developer using a supported coding agent in a repo with a test suite; teams that
  keep "add tests" rules in CLAUDE.md and watch them get ignored.
- **Components:** equivalent stop/after-agent hook maps for every supported host
  (`hooks/hooks.json` plus generated Codex, Copilot, Gemini, and Cursor maps) and one script. Reads
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
  - target hook maps — one stop/after-agent entry, no matcher
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

## Build log
- i100: full component inventory landed per spec — manifest (0.1.0), Stop hook
  (no matcher; quoted plugin root), nudge.sh (fail-open: trap→exit 0, git/repo
  guards, porcelain classifier handling renames and quoted paths, once-per-session
  TMPDIR marker with repo-cksum fallback, JSON-escaped systemMessage), README with
  an honest Limits section, CHANGELOG 0.1.0-Unreleased. Hand-smoked the three core
  paths (gap → nudge; same session → silent; test present → silent) before QA.

## Test log
### Test pass — i101
- tier 1: executable suite (foundry/tests/test-gap-nudge/acceptance.test.sh),
  11/11 across all 7 spec checks + a bonus (*.spec.* beside source): gap→nudge,
  once-per-session marker, tracked+untracked test silencing, clean-tree/non-repo/
  no-git-on-PATH silence, malformed & empty stdin exit 0, docs-only silence,
  structural (Stop event, quoted root, executable shebang script)
- tier 2: official `claude plugin validate --strict` PASS (smoke.sh)
- tier 3: hand-read the nudge copy as a user — names ≤3 files then "…", says what
  and why in one line, no imperative tone
- defects: none in product — one harness bug (env couldn't find bash after PATH
  cleared) fixed in the test itself
- always_on_tokens recorded: manifest description only
TEST VERDICT: pass

## Review log
### Review — i102
- Security read clean: stdin treated as data (single sanitized id extracted,
  [A-Za-z0-9_-] only — no traversal into the TMPDIR marker path); read-only on the
  repo; no network; every failure path lands on exit 0. Rename and quoted-path
  porcelain forms handled. Description honest; README's Limits section is the
  right kind of candor.
- DEFECT (core use case): `git status --porcelain` collapses untracked
  directories — a brand-new module (`?? newmod/` containing core.py) produces NO
  nudge. Reproduced. New-code-without-tests is the single most important case
  this plugin exists for; missing it silently is a docs-truth and scope failure.
  Symmetric risk: a new tests/ dir full of tests still matches by dir name, so
  the false-silence direction is the broken one. Fix: `-uall` (or
  `--untracked-files=all`) so untracked files list individually; pin with a
  regression test.
- Axes: scope 4 · prompt 5 (manifest desc is the auto-invoke surface; accurate) ·
  thrift 5 (33 tok) · hook-safety 5 · docs-truth 3 · structure 5.
REVIEW: bounced — untracked-directory blindness on the plugin's core case; add
-uall + regression test.

## Build log (post-bounce)
- i103: `-uall` on the porcelain call — untracked files inside new directories now
  classify individually; CHANGELOG credits the review catch. Re-ran the reviewer's
  reproduction: new module now nudges.

### Test pass — i104 (post-bounce re-test)
- tier 1: suite now 13/13 — i102 regression pinned both directions (new source
  dir nudges; new tests dir silences); all prior checks green
- tier 2: official strict validate PASS
- tier 3: reviewer's exact reproduction re-run by hand — nudges with the path
- defects: none found
TEST VERDICT: pass

### Review — i105 (post-bounce)
- One-flag fix, exactly as prescribed; regression pinned in both directions so
  the collapse can't quietly return. CHANGELOG credits the catch — version story
  stays honest for 0.1.0.
- Re-read the full script post-change: no new surface, contract unchanged.
- Axes: scope 5 · prompt 5 · thrift 5 (33 tok) · hook-safety 5 · docs-truth 5 ·
  structure 5.
REVIEW: approved — core case covered, both directions pinned.

### Published — i106 (maintainer)
Marketplace entry live (source ./plugins/test-gap-nudge), v0.1.0, CHANGELOG dated
2026-07-06, tag test-gap-nudge-v0.1.0. Install:
`/plugin install test-gap-nudge@foundry`. First everyday-utility ship of the v8
slate — bounced once on the core case, fixed, both directions pinned.

## Maintenance log
- i155 (builder, v10 #2): v0.2.0 — `TEST_GAP_NUDGE_EXTS` overrides the source
  extension list; value sanitized to `[A-Za-z0-9|]` (regex can't be broken or
  injected), empty → default. Fail-open contract unchanged; suite +3 checks
  (override respected, hostile value stripped, default regression). Tag
  test-gap-nudge-v0.2.0.
- i164 (builder, v10 #10): v0.3.0 — TEST_GAP_NUDGE_DEBUG=1 decision-trail log
  in TMPDIR; debug-off byte-identical (suite-proven). Tag test-gap-nudge-v0.3.0.
- i182 (maintainer, v11 #2): v0.3.1 — README Manage section (docs sweep). Tag test-gap-nudge-v0.3.1.
