---
name: doctor
description: Audit a coding-agent plugin and its host-native packages. Use when the user says doctor my plugin, audit cross-host compatibility, check a plugin against the spec, diagnose a hook or skill that will not load, or prepare a plugin for publishing.
---

# Plugin doctor

Audit the requested plugin directory (`$ARGUMENTS`, otherwise ask). Detect its target
hosts from the manifests, read every relevant file, and report numbered findings.
Each finding includes severity (`BLOCKER`, `WARN`, or `NIT`), host, file, cause, and
exact fix. End with `DOCTOR VERDICT: clean | issues found ({n})`.

## Checks, in order

**Shared source and packages (BLOCKERs)**

1. A canonical manifest exists, parses, and has a kebab-case name. Each advertised
   target has its native manifest: `.claude-plugin/plugin.json`,
   `.codex-plugin/plugin.json`, `gemini-extension.json`,
   `.cursor-plugin/plugin.json`, or `.github/plugin/plugin.json`.
2. Name, version, and description agree across generated manifests. Components stay
   at the package root; manifest paths are relative, do not escape with `../`, and
   point to existing files.
3. Each distributable contains only its host's manifest and hook contract. Flag a
   hook-enabled “universal” ZIP that combines Claude/Open Plugin and Gemini metadata:
   both reserve `hooks/hooks.json` but accept different lifecycle events.
4. A version is semver. Remind the author that installed users receive a change only
   when the version and published native packages advance together.

**Components**

5. Every `skills/*/SKILL.md` has `name` and a concrete `description` with invocation
   triggers. Flag vendor-specific body assumptions when the skill claims portability.
6. Host-specific agents/commands declare their supported host and least-privilege
   tools. Never imply a proprietary component will load elsewhere unchanged.
7. For hooks, validate event spelling, nesting, matcher shape, and plugin-root variable
   against that host. Matchers must be narrow. Referenced scripts need a shebang and
   executable bit. Undocumented destructive effects, network calls, credential reads,
   or writes outside the project are BLOCKERs.

**Fit and finish**

8. README covers every supported install/update path, components, hook disable steps,
   runtime requirements, network behavior, and on-disk footprint. The changelog's top
   entry matches the manifest version.
9. Verify deterministic archives and their published SHA-256 digests when an index is
   present. Confirm regenerated adapters do not drift from shared metadata/behavior.
10. Warn when always-loaded descriptions exceed roughly 300 tokens or when the plugin
    visibly does more than one job; name the heaviest text or proposed split.

When a schema is uncertain, verify it in the relevant official Claude Code, Codex,
Gemini CLI, Cursor, or GitHub Copilot plugin reference rather than guessing.
