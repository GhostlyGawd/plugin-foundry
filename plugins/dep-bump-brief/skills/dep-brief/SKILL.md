---
name: dep-brief
description: Summarize dependency bumps in the current branch or diff into an honest review brief. Use when the user asks to review a dependency PR, summarize dependabot or renovate changes, or asks what changed in this bump.
---

# Write the brief

1. **Find the bumps.** Diff the manifest/lockfile against the base branch
   (`git diff <base>... -- <files>`; ask which base if ambiguous). Recognize:
   - js: `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - python: `requirements*.txt`, `pyproject.toml`, `poetry.lock`, `uv.lock`
   - rust: `Cargo.toml`, `Cargo.lock`
   - go: `go.mod`, `go.sum`
2. **Per bump, state the facts:** `name old → new`, and the semver distance —
   patch, minor, or **MAJOR** (flag majors loudly; they headline the brief).
3. **Find what this repo actually touches.** Grep the repo for import/require/
   use sites of each bumped package; quote the real files. Those sites become
   the "what to check" list — concrete places, not generic advice.
4. **Changelogs, honestly.** Read the package's changelog or release notes
   only if reachable with your available tools. If you cannot reach it, write
   exactly "changelog not checked" for that package. **NEVER invent changelog
   content, breaking changes, or version facts** — an unread source is named
   as unchecked, never summarized from memory.
5. **Close with one risk line:** highest semver distance × number of real
   usage sites (e.g. "risk: MAJOR bump used in 7 files — read before merge"),
   so the brief is pasteable into the PR review as-is.
