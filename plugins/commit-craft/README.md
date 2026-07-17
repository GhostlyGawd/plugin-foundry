# Commit Craft

Conventional-commit discipline, both directions: a `commit` skill that reads your
staged diff and writes the message properly, and a PreToolUse guard hook that
blocks malformed `git commit -m` messages with a printed reason.

## Install

One shared source ships native packages for Claude Code, Codex, Gemini CLI, Cursor, and
GitHub Copilot. See [host-specific install paths](https://github.com/GhostlyGawd/plugin-foundry/blob/main/COMPATIBILITY.md).

```
/plugin marketplace add GhostlyGawd/plugin-foundry
/plugin install commit-craft@foundry
```

## The hook, honestly
Narrow matcher (`Bash` only), read-only, no network, **fails open**: garbled input,
interactive commits, and non-commit commands always pass. It only ever blocks a
`git commit -m` whose subject isn't `type(scope): subject` — and it tells you why
on stderr. Remove the plugin, the hook is gone.

## Configuration

`COMMIT_CRAFT_TYPES` — replace the allowed type list (pipe/comma/space-separated),
e.g. to adopt the full conventional-commits set:

```
export COMMIT_CRAFT_TYPES="feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert"
```

Tokens must be lowercase letters; anything else is dropped (so the value can
never inject regex), and an empty result falls back to the default
`feat|fix|docs|refactor|test|chore|perf`. The guard's block message always names
the list it enforced.

## Recipes
- "commit this" → skill stages nothing new, reads the diff, writes `fix(auth): …`
- "split this into two commits" → skill proposes the partition first
- Type `git commit -m "wip"` yourself → hook blocks with the reason (try it)

## Changelog
See [CHANGELOG.md](./CHANGELOG.md).

## Debugging the guard

Set `COMMIT_CRAFT_DEBUG=1` and the guard appends every decision (pass reason,
or BLOCK with the enforced type list) to `$TMPDIR/commit-craft-debug.log`.
Off by default; behavior is identical with it unset.

## Manage

- **Update:** `/plugin marketplace update`, then `claude plugin update commit-craft`
- **Disable / re-enable:** `claude plugin disable commit-craft` / `claude plugin enable commit-craft` (or the `/plugin` menu — no uninstall needed)
- **Uninstall:** `claude plugin uninstall commit-craft` — removes everything the plugin added
- **On disk:** nothing, unless `COMMIT_CRAFT_DEBUG=1` is set — then a decision log at `$TMPDIR/commit-craft-debug.log` (see Debugging the guard). Uninstalling removes the guard hook with everything else.
