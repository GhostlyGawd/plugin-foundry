---
name: scaffold
description: Scaffold a portable coding-agent plugin with host-native packages. Use when creating a plugin for Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, or several of those hosts.
---

# Scaffold a portable plugin

Create one minimal plugin source that can be packaged for the requested hosts. Take
the plugin name, components, and target hosts from the request (`$ARGUMENTS` when
available). Ask only when the name is missing; default the host set to Claude Code,
Codex, Gemini CLI, Cursor, and GitHub Copilot.

## Rules that are not optional

- Use a kebab-case name. Published names are immutable, so confirm it reads well in
  marketplace coordinates such as `name@marketplace`.
- Keep behavior once at the plugin root: `skills/`, `scripts/`, and documentation
  are shared source, not copied host forks.
- Emit a separate native package per host. Claude/Open Plugin and Gemini both reserve
  `hooks/hooks.json` but use different event names; a hook-enabled ZIP containing
  both schemas is invalid for at least one host.
- Use relative manifest paths beginning with `./` where the host format permits them.
- Prefer `skills/<skill-name>/SKILL.md` as the portable model-invoked component.

## Procedure

1. Create the shared root and a canonical `.claude-plugin/plugin.json` with `name`,
   a concrete one-sentence `description`, `version: "0.1.0"`, `author`, and
   `keywords`. Add only component paths that exist.
2. For each skill, create `skills/<skill-name>/SKILL.md` with frontmatter `name` and
   `description`. The description is the invocation contract: what it does plus
   “Use when …” with concrete triggers. The body defines inputs, procedure, output,
   and the missing-input path without assuming a particular model vendor.
3. Add host-native manifests from the same metadata:
   `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`,
   `.github/plugin/plugin.json`, and a Gemini `gemini-extension.json` adapter.
   When working inside Plugin Foundry, use `python3 tools/adapters.py --write`
   instead of editing derived files by hand.
4. If hooks are requested, make the Claude/Open Plugin `hooks/hooks.json` canonical.
   Use the narrowest matcher, quote
   `"${CLAUDE_PLUGIN_ROOT}"/scripts/<script>`, and put executable scripts under
   `scripts/`. Derive Gemini event names/root `${extensionPath}` and Cursor lower
   camel-case events/root `${CURSOR_PLUGIN_ROOT}`. Default scripts to read-only and
   fail-open; blocking behavior requires an explicit request and a one-line reason.
5. Package each host independently so its root contains only its native manifest and
   hook schema. In Plugin Foundry, run `python3 tools/export.py <plugin-name>`; do not
   hand-copy the source into five drifting implementations.
6. Create `README.md` covering each supported install path, every component, hook
   disable behavior, runtime requirements, and on-disk/network footprint. Create
   `CHANGELOG.md` with `## 0.1.0 — Unreleased`.
7. Print the shared tree, generated package list, and validation commands. In Plugin
   Foundry those are `python3 tools/adapters.py --check`,
   `python3 tools/validate.py`, and `python3 tools/export.py <plugin-name>`; also run
   any installed official host validator against its native package.

Do not invent fields or event names. When a target format is uncertain, consult its
official plugin or extension reference before writing it.
