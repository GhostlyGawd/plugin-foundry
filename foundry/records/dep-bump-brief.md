---
name: dep-bump-brief
title: Dep-Bump Brief
category: workflow
stage: building
version: null
kind: plugin
components: [skills]
one_liner: Turns a dependency-bump diff into a plain-language brief — what changed, what might break, what to check.
tags: [dependencies, review, changelogs]
created: 2026-07-06
updated: 2026-07-07
---

# Dep-Bump Brief

Dependabot and renovate branches pile up because reviewing them means opening three
changelogs and a diff of a lockfile nobody can read. The result is either rubber-stamp
merges or a stale queue — both worse than a two-minute honest brief.

## Pitch
- **Job:** given a branch or diff that bumps dependencies, produce a short brief per
  bump: old → new version, semver distance, breaking changes pulled from the
  package's changelog/release notes when reachable, and a concrete "what to check"
  list for this repo's usage of that package.
- **User:** anyone assigned dependency-update PRs; solo maintainers with a
  dependabot backlog.
- **Components:** one skill (`skills/dep-brief/`). Reads the lockfile/manifest diff
  from git, greps the repo for import/usage sites of each bumped package, and
  drafts the brief with an honesty rule: if the changelog is unreachable, say
  "changelog not checked" rather than guessing.
- **Why a plugin:** the workflow is identical every time and spans git, grep, and
  synthesis — a versioned skill beats a prompt retyped weekly, and the honesty
  rules (never invent changelog content) deserve review and a changelog of their own.

## Spec
- One skill, `dep-brief`, description (verbatim): "Summarize dependency bumps
  in the current branch or diff into an honest review brief. Use when the user
  asks to review a dependency PR, summarize dependabot or renovate changes, or
  asks what changed in this bump."
- Procedure: (1) find bumped packages from the manifest/lockfile diff against
  the base branch — package.json/package-lock, requirements*.txt/poetry/uv,
  Cargo.toml/Cargo.lock, go.mod/go.sum; (2) per bump: old → new, semver
  distance (major/minor/patch — flag major loudly); (3) grep the repo for
  usage sites of each bumped package and turn real call sites into a concrete
  "what to check" list; (4) changelog/release notes: read them only if
  reachable with available tools — otherwise the brief says exactly
  "changelog not checked" for that package.
- Honesty rules (review these hardest): **NEVER invent changelog content,
  breaking changes, or version facts**; unreachable sources are named as
  unchecked, not summarized from memory; usage sites quoted from this repo
  only.
- Output: one short brief per bump + a single risk line (highest semver
  distance × usage-site count), suitable for pasting into the PR review.

### Acceptance checks
1. SKILL.md frontmatter complete; description carries the invoke contract
   ("Use when") verbatim from this spec.
2. The honesty rules are present verbatim: "changelog not checked" path and
   the never-invent clause.
3. All four ecosystems named in the procedure (js, python, rust, go).
4. Suite green; always-on token estimate stamped; official validate passes.

## Build log
- i200: manifest, dep-brief skill (verbatim description; four ecosystems;
  MAJOR flagged loudly; usage-site grep; "changelog not checked" + never-invent
  verbatim; risk line), README with Manage section (v11 convention),
  CHANGELOG 0.1.0 Unreleased. Build complete per spec.
