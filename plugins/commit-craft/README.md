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

## Recipes
- "commit this" → skill stages nothing new, reads the diff, writes `fix(auth): …`
- "split this into two commits" → skill proposes the partition first
- Type `git commit -m "wip"` yourself → hook blocks with the reason (try it)

## Changelog
See [CHANGELOG.md](./CHANGELOG.md).
