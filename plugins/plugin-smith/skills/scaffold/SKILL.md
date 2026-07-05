---
name: scaffold
description: Scaffold a new Claude Code plugin directory with the official layout. Use when creating a new plugin, starting a plugin skeleton, or converting loose commands into a plugin.
---

# Scaffold a plugin

Create a correct, minimal Claude Code plugin skeleton. Take the plugin name and the
component list from the request (`$ARGUMENTS` if provided); ask only if the name is
missing.

## Rules that are not optional
- The name is kebab-case, no spaces. Published names are immutable — confirm the name
  reads well after an `@` (`name@marketplace`) before creating anything.
- Only `plugin.json` goes inside `.claude-plugin/`. Every component directory
  (`skills/`, `agents/`, `hooks/`, `scripts/`) sits at the plugin root.
- All manifest paths are relative and start with `./`.
- Prefer `skills/<skill-name>/SKILL.md` over flat `commands/*.md` for new plugins.

## Procedure
1. Create `<plugin-name>/.claude-plugin/plugin.json` containing exactly: `name`,
   `description` (one sentence, concrete), `version: "0.1.0"`, `author`, and
   `keywords`. Nothing speculative.
2. For each requested skill: `skills/<skill-name>/SKILL.md` with frontmatter `name`
   and `description`. Write the description as the auto-invoke contract: what it does
   + "Use when …" with 2–3 concrete triggers. Body: a concrete procedure, expected
   inputs/outputs, and what to do when inputs are missing.
3. For each requested agent: `agents/<agent-name>.md` with frontmatter `name`,
   `description` (same contract discipline), and the narrowest `tools`/
   `disallowedTools` that still work. Body: role, procedure, output format.
4. If hooks are requested: `hooks/hooks.json` with the narrowest matcher that works
   (never `.*`), commands referencing `"${CLAUDE_PLUGIN_ROOT}"/scripts/<script>` in
   quotes, plus the script in `scripts/` with a shebang, made executable
   (`chmod +x`). Default every script to read-only and fail-open (exit 0 on any
   parsing doubt) unless the user explicitly wants blocking behavior — then exit 2
   with a one-line reason on stderr.
5. Always create `README.md` (what it does, install lines, each component, how to
   disable any hook) and `CHANGELOG.md` (`## 0.1.0 — Unreleased`).
6. Finish by printing the tree and the two test commands:
   `claude plugin validate ./<plugin-name> --strict` and
   `claude --plugin-dir ./<plugin-name>`.

Do not invent manifest fields. If a field or event is uncertain, check
https://code.claude.com/docs/en/plugins-reference before writing it.
