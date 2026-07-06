# Security Policy

The plugins this marketplace ships run on **your** machine — hooks execute during
your Claude Code sessions. That's why this policy exists and why it's strict.

## Reporting a vulnerability

**Please do not open a public issue for anything exploitable.** Use GitHub's
private vulnerability reporting instead: **Security → Report a vulnerability** on
this repository (or `https://github.com/GhostlyGawd/plugin-foundry/security/advisories/new`).
The operator reads every report; you'll get an acknowledgment on the advisory
thread and credit in the fix's changelog (`found_by`) unless you ask otherwise.

For non-exploitable defects — a hook misfiring, a wrong recommendation, a broken
install line — the public bug lane is faster:
[open a bug issue](https://github.com/GhostlyGawd/plugin-foundry/issues/new?template=bug.yml).
Bug fixes on published plugins outrank all new work here by protocol (`LOOP.md`
priority 3), and every fix ships with a regression test.

## Supported versions

Only the **latest published version** of each plugin on the shelf
(`.claude-plugin/marketplace.json`) is supported. Claude Code keys updates on the
version string, so any fix arrives as a semver bump + changelog entry — run
`/plugin marketplace update`, then `claude plugin update <name>`.

## What the shipped plugins may and may not do

Every plugin here ships under the workshop's hook-safety law
(`charter/QUALITY.md`, `charter/SECURITY.md`, enforced by `tools/validate.py`
and a line-by-line human-style review before publish):

- Hooks are **fail-open**: parse trouble or missing tools mean silent exit,
  never a blocked session (the one deliberate exception: commit-craft's guard
  blocks a malformed `git commit -m` with a printed reason — that's its job).
- **No network calls** from any shipped script without loud README disclosure —
  today, none make any.
- **Narrow matchers** (never `.*`), quoted `"${CLAUDE_PLUGIN_ROOT}"`, no writes
  outside your temp dir, no undocumented file access.
- The repo holds **zero secrets**, and shipped artifacts contain only what an
  installer should receive.

If you observe a shipped plugin violating any of the above, that's a
vulnerability report — use the private channel above.
