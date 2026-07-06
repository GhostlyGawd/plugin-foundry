# Commit Craft

Conventional-commit discipline, both directions: a `commit` skill that reads your
staged diff and writes the message properly, and a PreToolUse guard hook that
blocks malformed `git commit -m` messages with a printed reason.

## Install

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
