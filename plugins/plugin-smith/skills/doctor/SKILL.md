---
name: doctor
description: Audit a Claude Code plugin directory against the official schema and this marketplace's quality bar. Use when the user says doctor my plugin, audit my plugin, check my plugin against the spec, why won't my hook or skill load, or before publishing a plugin.
---

# Plugin doctor

Audit the plugin directory given in the request (`$ARGUMENTS`, else ask). Read every
file before judging. Report findings as a numbered list — each finding: severity
(BLOCKER / WARN / NIT), the file, what's wrong, and the exact fix. End with
`DOCTOR VERDICT: clean | issues found ({n})`.

## Checks, in order

**Structure (BLOCKERs)**
1. `.claude-plugin/plugin.json` exists, parses, and contains a kebab-case `name`.
2. Components live at the plugin root — anything besides `plugin.json` inside
   `.claude-plugin/` is misplaced.
3. Every path in the manifest is relative and starts with `./`; no `../` escapes.
4. If `version` exists it is semver — and remind: bumping it is the ONLY way
   installed users receive changes.

**Components**
5. Each `skills/*/SKILL.md` and `commands/*.md` has frontmatter with a `description`;
   skills also need `name`. Flag any description that couldn't tell Claude *when* to
   fire ("Helps with code" = WARN, it's the invocation contract).
6. Each `agents/*.md` has `name` + `description`; flag missing tool restriction on
   agents that only need to read.
7. `hooks/hooks.json`: parses; event names match the official table (case-sensitive);
   hook types are command|http|mcp_tool|prompt|agent; matchers are narrow (`.*` =
   BLOCKER); `${CLAUDE_PLUGIN_ROOT}` is quoted; each referenced script exists, has a
   shebang, and is executable. Read each script: destructive effects, network calls,
   or writes outside the project are BLOCKERs unless the README documents them loudly.

**Fit and finish**
8. README covers install, every component, and hook-disable instructions; CHANGELOG's
   top entry matches the manifest version.
9. Token thrift: sum the rough size of all always-loaded descriptions; over ~300
   tokens = WARN with the heaviest offenders named (move detail into skill bodies or
   supporting files — those load on invoke).
10. Scope: if the plugin visibly does more than one job, say so and propose the split.

When the official schema is in doubt, verify at
https://code.claude.com/docs/en/plugins-reference rather than guessing.
