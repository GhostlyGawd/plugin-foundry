---
name: pr-narrator
title: PR Narrator
category: workflow
stage: idea
version: null
components: [agents]
one_liner: A subagent that turns a branch's commits and diff into a reviewer-ready PR description.
tags: [pull-requests, agents, writing]
created: 2026-07-04
updated: 2026-07-04
---

# PR Narrator

PR descriptions are either empty or novels; reviewers need the middle.

## Pitch
- **Job:** one invocation from branch to honest, skimmable PR description.
- **User:** anyone opening PRs from Claude Code.
- **Components:** one agent (`pr-narrator`) with a tight description so Claude
  invokes it when PRs come up; read-only git tools; template: what/why/how-to-review/
  risk notes.
- **Why a plugin:** first agent-component exercise for the line — different
  frontmatter schema, different review lens.
