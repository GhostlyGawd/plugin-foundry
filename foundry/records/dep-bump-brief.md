---
name: dep-bump-brief
title: Dep-Bump Brief
category: workflow
stage: idea
version: null
kind: plugin
components: [skills]
one_liner: Turns a dependency-bump diff into a plain-language brief — what changed, what might break, what to check.
tags: [dependencies, review, changelogs]
created: 2026-07-06
updated: 2026-07-06
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
