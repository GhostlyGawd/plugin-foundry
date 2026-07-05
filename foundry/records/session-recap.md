---
name: session-recap
title: Session Recap
category: context
stage: spec
version: null
components: [skills, hooks]
one_liner: Writes a structured recap when a session ends and recalls it when the next one starts.
tags: [memory, sessions, continuity]
created: 2026-07-04
updated: 2026-07-04
---

# Session Recap

Context evaporates between sessions; yesterday's decisions get re-derived today.

## Pitch
- **Job:** continuity across sessions without hand-written notes.
- **User:** anyone running multi-day work in one repo.
- **Components:** a Stop/SessionEnd hook appending a dated recap stub to a project
  log file, plus a `recall` skill that reads and summarizes recent entries on demand.
- **Why a plugin:** it's an event (hook) + a retrieval prompt (skill) — a natural
  bundle; also a clean exercise of hook-safety law (writes one project-local file,
  documented loudly).

## Spec
- Name: `session-recap` (forever). One skill, `recap`, description (verbatim):
  "Write a durable handoff recap of this working session into SESSION-RECAP.md.
  Use when ending a session, handing work to someone else, or the user says recap
  this session, write a handoff, or where did we leave off."
- Behavior: read the session's evidence (git status, git diff --stat, recent
  conversation decisions), then APPEND a dated section to SESSION-RECAP.md with:
  What changed · Decisions made · Open questions · Next steps (checkboxed). Never
  overwrite prior recaps; create the file if absent; no hooks, no network.
### Acceptance checks
1. Skill appends (never truncates) and dates each section.
2. Reads git evidence before writing — no invented changes.
3. Next steps render as actionable checkboxes.
