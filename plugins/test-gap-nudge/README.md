# Test-Gap Nudge

A Stop hook that notices when your session changed source files but never touched a
test, and says so — once, politely, with the file names. It never blocks anything.

## Install

```
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install test-gap-nudge@foundry
```

## What it does

When Claude finishes responding, the hook runs `git status --porcelain` and
classifies changed paths:

- **tests**: anything under `test/`, `tests/`, `spec/`, `__tests__/`, or named
  `test_*`, `*_test.*`, `*.test.*`, `*.spec.*`
- **source**: other changed files with common code extensions (`.py .js .ts .go
  .rb .rs .java .c .sh …`)

If source moved and tests didn't, you get one line:

```
test-gap-nudge: 2 source file(s) changed, no test files touched — src/auth.py, src/db.py
```

Docs and config changes (`.md`, `.json`, `.yml`, …) never trigger it.

## Configuration

`TEST_GAP_NUDGE_EXTS` — override which extensions count as "source"
(pipe/comma/space-separated), e.g. in your shell profile:

```
export TEST_GAP_NUDGE_EXTS="py|rs|zig"
```

Anything outside `[A-Za-z0-9|]` is stripped before use, so a malformed value can
never break the hook; an empty result falls back to the default list. Unset it
to get the defaults back.

## The hook, honestly

- **Advisory only.** Always exits 0; it cannot block Claude from stopping, ever.
- **Once per session.** A marker file in your temp dir keyed by session id keeps it
  from nagging; delete the marker (or start a new session) to re-arm.
- **Read-only** on your repo. Its only write is that temp marker.
- **No network. No jq. Fails open** — no git, not a repo, weird input: it stays
  silent and exits 0.
- Remove the plugin and the hook is gone.

## Limits, honestly

Path conventions are heuristics. A repo that keeps tests beside sources with
unusual names (e.g. `checks.py`) will get a false nudge; a change that edits a test
file cosmetically counts as "tests touched." It's a nudge, not a gate — pair it
with real CI for enforcement.

## Debugging a silent hook

The hook fails open by design, so "it never fires" has no visible error. Set
`TEST_GAP_NUDGE_DEBUG=1` and it appends its decision trail (why it stayed
silent, or why it nudged) to `$TMPDIR/test-gap-nudge-debug.log`. Unset the
variable and behavior is exactly as before — the log is the only difference.

## Manage

- **Update:** `/plugin marketplace update`, then `claude plugin update test-gap-nudge`
- **Disable / re-enable:** `claude plugin disable test-gap-nudge` / `claude plugin enable test-gap-nudge` (or the `/plugin` menu — no uninstall needed)
- **Uninstall:** `claude plugin uninstall test-gap-nudge` — removes everything the plugin added
- **On disk:** a once-per-session marker in your temp dir, plus `$TMPDIR/test-gap-nudge-debug.log` when `TEST_GAP_NUDGE_DEBUG=1` (see Debugging a silent hook). Uninstalling removes the hook with everything else.
